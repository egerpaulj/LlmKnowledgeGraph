"""Ranker for models using F1, precision, recall and latency.

Usage:
  python3 evaluation/ranker.py --top_k 5

The script reads these CSVs (relative to repo root):
  evaluation/eval_f1.csv
  evaluation/eval_precision.csv
  evaluation/eval_recall.csv
  evaluation/eval_latency_ms.csv

It normalizes metrics (min-max), inverts latency (lower is better),
computes a weighted composite score and prints the top-k models.
"""
from __future__ import annotations
import argparse
from typing import Dict, Optional
import pandas as pd


def load_metrics(f1_path: str, precision_path: str, recall_path: str, latency_path: str) -> pd.DataFrame:
    """Load CSVs and return a DataFrame with one row per `Run` containing f1, precision, recall, latency_ms_mean."""
    f1 = pd.read_csv(f1_path)
    precision = pd.read_csv(precision_path)
    recall = pd.read_csv(recall_path)
    latency = pd.read_csv(latency_path)

    # compute mean latency per Run (value column)
    if "value" in latency.columns:
        latency["value"] = pd.to_numeric(latency["value"], errors="coerce")
        latency_mean = latency.groupby("Run")["value"].mean().reset_index()
        latency_mean = latency_mean.rename(columns={"value": "latency_ms"})
    else:
        raise ValueError("latency CSV missing 'value' column")

    # reduce each metric df to Run and metric column (last column name may vary)
    df = f1[["Run", "f1"]].merge(precision[["Run", "precision"]], on="Run", how="inner")
    df = df.merge(recall[["Run", "recall"]], on="Run", how="inner")
    df = df.merge(latency_mean, on="Run", how="inner")
    # ensure numeric
    df["f1"] = pd.to_numeric(df["f1"], errors="coerce")
    df["precision"] = pd.to_numeric(df["precision"], errors="coerce")
    df["recall"] = pd.to_numeric(df["recall"], errors="coerce")
    df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
    return df


def minmax_normalize(series: pd.Series) -> pd.Series:
    """Min-max normalize a pandas Series to [0,1]. If constant, returns zeros."""
    lo = series.min()
    hi = series.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        return pd.Series(0.0, index=series.index)
    return (series - lo) / (hi - lo)


def rank_models(df: pd.DataFrame, weights: Optional[Dict[str, float]] = None, top_k: int = 5) -> pd.DataFrame:
    """Compute normalized scores and return top_k rows sorted by composite score.

    weights dict keys: 'f1','precision','recall','latency' (latency weight applies to inverted latency)
    If weights is None, equal weights are used.
    """
    if weights is None:
        weights = {"f1": 1.0, "precision": 1.0, "recall": 1.0, "latency": 1.0}

    # normalize metrics
    df = df.copy()
    df["f1_n"] = minmax_normalize(df["f1"]) 
    df["precision_n"] = minmax_normalize(df["precision"]) 
    df["recall_n"] = minmax_normalize(df["recall"]) 
    # latency: lower is better -> invert after normalization
    latency_n = minmax_normalize(df["latency_ms"]) 
    df["latency_inv_n"] = 1.0 - latency_n

    # normalize weights to sum to 1
    w = weights.copy()
    total = sum(w.values()) if w else 1.0
    if total == 0:
        total = 1.0
    for k in w:
        w[k] = float(w[k]) / total

    df["score"] = (
        w.get("f1", 0.0) * df["f1_n"]
        + w.get("precision", 0.0) * df["precision_n"]
        + w.get("recall", 0.0) * df["recall_n"]
        + w.get("latency", 0.0) * df["latency_inv_n"]
    )

    cols_to_show = ["Run", "f1", "precision", "recall", "latency_ms", "score"]
    ranked = df.sort_values("score", ascending=False)
    return ranked[cols_to_show].head(top_k)


def parse_weights(weight_str: str) -> Dict[str, float]:
    """Parse weights from a comma-separated k=v string, e.g. f1=2,latency=1"""
    out: Dict[str, float] = {}
    if not weight_str:
        return out
    parts = weight_str.split(",")
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            try:
                out[k.strip()] = float(v)
            except ValueError:
                raise ValueError(f"Invalid weight value for {k}: {v}")
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--f1", default="evaluation/eval_f1.csv")
    p.add_argument("--precision", default="evaluation/eval_precision.csv")
    p.add_argument("--recall", default="evaluation/eval_recall.csv")
    p.add_argument("--latency", default="evaluation/eval_latency_ms.csv")
    p.add_argument("--top_k", type=int, default=5)
    p.add_argument(
        "--weights",
        help="Comma-separated weights, e.g. f1=2,precision=1,recall=1,latency=0.5",
        default="",
    )
    args = p.parse_args()

    df = load_metrics(args.f1, args.precision, args.recall, args.latency)
    weights = parse_weights(args.weights)
    if weights:
        ranked = rank_models(df, weights=weights, top_k=args.top_k)
    else:
        ranked = rank_models(df, top_k=args.top_k)

    pd.set_option("display.max_colwidth", 200)
    print(ranked.to_string(index=False))


if __name__ == "__main__":
    main()
