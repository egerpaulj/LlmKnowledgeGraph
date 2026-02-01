"""Elasticsearch index settings and mapping configuration for structured logging"""
from datetime import datetime


# Index settings for optimal log storage and performance
INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "refresh_interval": "30s",
        "index": {
            "codec": "best_compression",
            "lifecycle": {
                "name": "policy-python-apps",
                "rollover_alias": "python-apps-logs"
            }
        }
    },
    "mappings": {
        "properties": {
            "@timestamp": {
                "type": "date",
                "format": "strict_date_time"
            },
            "level": {
                "type": "keyword"
            },
            "logger": {
                "type": "keyword"
            },
            "message": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "app_name": {
                "type": "keyword"
            },
            "module": {
                "type": "keyword"
            },
            "function": {
                "type": "keyword"
            },
            "line": {
                "type": "integer"
            },
            "exception": {
                "type": "text"
            },
            "thread": {
                "type": "keyword"
            },
            "process": {
                "type": "keyword"
            }
        }
    }
}

# Index lifecycle management policy for automatic rollover and deletion
ILM_POLICY = {
    "policy": {
        "phases": {
            "hot": {
                "min_age": "0d",
                "actions": {
                    "rollover": {
                        "max_primary_shard_size": "50gb",
                        "max_age": "1d"
                    }
                }
            },
            "warm": {
                "min_age": "7d",
                "actions": {
                    "set_priority": {
                        "priority": 50
                    }
                }
            },
            "delete": {
                "min_age": "8d",
                "actions": {
                    "delete": {}
                }
            }
        }
    }
}


def create_index_if_not_exists(es_client, index_name):
    """
    Create Elasticsearch index with predefined settings and mapping if it doesn't exist
    
    Args:
        es_client: Elasticsearch client instance
        index_name: Base name of the index (will be appended with date)
    
    Returns:
        bool: True if index was created or already exists, False if error occurred
    """
    # Create index with today's date suffix
    today = datetime.utcnow().strftime('%Y.%m.%d')
    full_index_name = f"{index_name}-{today}"
    
    try:        
        # Check if index already exists
        if es_client.indices.exists(index=full_index_name):
            print(f"Index '{full_index_name}' already exists")
            return True
        
        # Update settings to link the ILM policy
        settings = INDEX_SETTINGS.copy()
        settings["settings"]["index"]["lifecycle"]["rollover_alias"] = index_name
        
        # Create index with settings and mapping
        es_client.indices.create(
            index=full_index_name,
            body=settings,
            ignore=400
        )
        
        # Create write alias pointing to the index (for ILM rollover)
        es_client.indices.put_alias(
            index=full_index_name,
            name=f"{index_name}-write"
        )
        
        print(f"Index '{full_index_name}' created successfully with ILM policy 'logs-policy'")
        return True
        
    except Exception as e:
        print(f"Error creating index '{full_index_name}': {e}")
        return False


def setup_ilm_policy(es_client):
    """
    Setup Index Lifecycle Management policy for automatic log retention
    
    Args:
        es_client: Elasticsearch client instance
    
    Returns:
        bool: True if policy was created or already exists, False if error occurred
    """
    try:
        policy_name = 'policy-python-apps'
        
        # Try to get existing policy
        try:
            existing_policy = es_client.ilm.get_lifecycle(policy=policy_name)
            if existing_policy:
                print(f"ILM policy '{policy_name}' already exists")
                return True
        except:
            pass  # Policy doesn't exist, continue to create it
        
        es_client.ilm.put_lifecycle(name=policy_name, body=ILM_POLICY)
        
        print(f"ILM policy '{policy_name}' created successfully")
        return True
        
    except Exception as e:
        print(f"Error setting up ILM policy: {e}")
        return False


def get_index_stats(es_client, index_name_pattern):
    """
    Get statistics for indexes matching the pattern
    
    Args:
        es_client: Elasticsearch client instance
        index_name_pattern: Pattern to match indexes (e.g., 'logs-python-apps*')
    
    Returns:
        dict: Index statistics or empty dict if error occurs
    """
    try:
        stats = es_client.indices.stats(index=index_name_pattern)
        return stats
    except Exception as e:
        print(f"Error retrieving index stats: {e}")
        return {}
