import requests
from src.logger import get_logger

logger = get_logger(__name__)

def execute_dax_query(access_token, dataset_id, dax_query):
    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    dax_query = {
            "queries": [{"query": dax_query}],
        "serializerSettings": {
            "includeNulls": True}
        }
    
    response = requests.post(url, json=dax_query, headers=headers)

    if response.status_code != 200:
        logger.error(f"Query failed with status code {response.status_code}. Response: {response.text}")
        raise Exception("Query failed")

    result = response.json()

    return result