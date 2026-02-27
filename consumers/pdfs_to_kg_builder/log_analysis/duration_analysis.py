import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from elasticsearch import Elasticsearch


def fetch_data(index_pattern: str,
               es_url: str = "http://localhost:9200",
               size: int = 5000,
               search_text: str = ""):

    es = Elasticsearch(es_url)

    # Build query
    if search_text:
        query_body = {
            "query": {
                "match_phrase": {
                    "message": search_text  
                }
            },
            "sort": [{"@timestamp": {"order": "asc"}}],
            "_source": ["message", "@timestamp"]
        }
    else:
        query_body = {
            "query": {"match_all": {}},
            "sort": [{"@timestamp": {"order": "asc"}}],
            "_source": ["message", "@timestamp"]
        }

    response = es.search(
        index=index_pattern,   
        body=query_body,
        size=size
    )

    records = []
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        message = source.get("message")
        timestamp = source.get("@timestamp")

        if message:
            file_name = message.split(":")[1].strip()  # File name comes after ":"
        else:
            file_name = "Unknown"  # Handle cases where message format is unexpected

        records.append({
            "file_name": file_name,
            "@timestamp": timestamp
        })

    df = pd.DataFrame(records)
    df["@timestamp"] = pd.to_datetime(df["@timestamp"])
    df = df.sort_values("@timestamp").reset_index(drop=True)

    return df


def calculate_durations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate duration based on next timestamp.
    """

    # Shift timestamp column to get next event
    df["next_timestamp"] = df["@timestamp"].shift(-1)

    # Duration = next - current
    df["duration"] = df["next_timestamp"] - df["@timestamp"]

    # Drop last row (no next timestamp)
    df = df.dropna(subset=["duration"])

    df["start_time"] = df["@timestamp"]
    df["end_time"] = df["next_timestamp"]

    return df[["file_name", "start_time", "end_time", "duration"]]


def plot_gantt(df: pd.DataFrame):
    """
    Plot Gantt chart from dataframe.
    """

    fig, ax = plt.subplots(figsize=(12, 6))

    for _, row in df.iterrows():
        ax.barh(
            row["file_name"],
            (row["end_time"] - row["start_time"]).total_seconds(),
            left=row["start_time"]
        )

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax.set_xlabel("Time")
    ax.set_ylabel("File Name")
    ax.set_title("File Processing Gantt Chart")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    index_pattern = "python-apps-*"   
    es_url = "http://localhost:9200"

    df = fetch_data(
        index_pattern=index_pattern,
        es_url=es_url,
        search_text="reading file" 
    )

    if df.empty:
        print("No data found.")
        return
    

    df_gantt = calculate_durations(df)
    
    df_gantt.to_csv("logs.csv")
    plot_gantt(df_gantt)


if __name__ == "__main__":
    main()