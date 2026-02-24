import pandas as pd
import time
from src.execute_dax import execute_dax_query
from src.parse_pandas import parse_to_pandas
from src.logger import get_logger

logger = get_logger(__name__)

def multiple_execute_dax_query(access_token, dataset_id, query_dict, export=True, export_format="csv"):
    results = {}
    for query_name, query_dax in query_dict.items():
        logger.info("Starting query '%s' (len=%d chars)", query_name, len(query_dax or ""))
        start = time.perf_counter()
        try:
            raw_result = execute_dax_query(access_token, dataset_id, query_dax)
            df = parse_to_pandas(raw_result)
            results[query_name] = df

            duration = time.perf_counter() - start
            if df.empty:
                logger.warning("Query '%s' completed in %.3fs but returned no rows", query_name, duration)
            else:
                logger.info("Query '%s' completed in %.3fs; rows=%d", query_name, duration, len(df))

            # Export individual query result if export is True and DataFrame is not empty
            if export and not df.empty:
                if export_format == "csv":
                    df.to_csv(f'output/{query_name}.csv', index=False)
                    logger.info("Exported '%s' to %s.csv", query_name, query_name)
                elif export_format == "excel":
                    df.to_excel(f"output/{query_name}.xlsx", index=False)
                    logger.info("Exported '%s' to %s.xlsx", query_name, query_name)

        except Exception as e:
            duration = time.perf_counter() - start
            logger.exception("Query '%s' failed after %.3fs: %s", query_name, duration, e)
            results[query_name] = pd.DataFrame()

    return results