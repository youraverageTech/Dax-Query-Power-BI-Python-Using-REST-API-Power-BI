import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

def parse_to_pandas(result):
    if result and "error" not in result:
        data = result['results'][0]['tables'][0]['rows']
        return pd.DataFrame(data)
    else:
        logger.error(f"Invalid result format: {result}")
        return pd.DataFrame()