import os
from dotenv import load_dotenv
from src.authenticate import authentication
from src.import_from_dir import load_queries_from_dir
from src.import_from_yaml import load_query_from_yaml
from src.multiple_execute_query import multiple_execute_dax_query
from src.export_to_excel import export_to_excel_multisheet
from src.logger import configure_basic_logging, get_logger
from datetime import datetime
import time



# Configuration
load_dotenv()
client_id = os.getenv("client_id")
tenant_id = os.getenv("tenant_id")
dataset_id = os.getenv("dataset_id")
client_secret = os.getenv("client_secret")
AUTHORITY = f"https://login.microsoftonline.com/{tenant_id}"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]


def start_process():
	# Set up logging
	configure_basic_logging(logfile="logs/project.log")
	logger = get_logger(__name__)

	logger.info("Starting the process to execute DAX queries and export results.")
	start_ts = datetime.now().isoformat()
	start = time.perf_counter()

	logger.info("Loading DAX queries from .dax or .yaml files in the 'queries' directory.")
	# First way of import dax query using dax format files.
	project_root = os.path.dirname(os.path.abspath(__file__))
	queries_dir = os.path.join(project_root, "queries")
	file_fdax_queries = load_queries_from_dir(queries_dir, ext=".dax")

	# Second way of import dax query using yaml file.
	file_yaml_queries = load_query_from_yaml(path="queries/queries.yaml")
	
	# If there are queries loaded from .dax files, use them. Otherwise, use the queries from the YAML file.
	if file_fdax_queries: 
		query_dict = file_fdax_queries
	else:
		query_dict = file_yaml_queries

	logger.info(f"Successfully loaded {len(query_dict)} queries. Proceeding with authentication and execution.")

	logger.info("Authenticating with Azure AD to obtain access token.")
	# authentication process
	access_token = authentication(client_id, AUTHORITY, client_secret, SCOPE)
	logger.info("Authentication successful. Access token obtained.")

	logger.info("Executing DAX queries against the Power BI dataset.")
	# Execute Query
	all_results = multiple_execute_dax_query(
		access_token=access_token,
		dataset_id=dataset_id,
		query_dict=query_dict,
		export=True,
		export_format="csv"
	)
	logger.info("Query execution completed. Results obtained for all queries.")

	logger.info("Exporting results to Excel file 'output/all_output.xlsx'.")
	# Export Output
	export_to_excel_multisheet(all_results, filename="output/all_output.xlsx")
	logger.info("Export completed successfully into output/all_output.xlsx.")

	# Preview Output
	print("\nPreview output:")
	for name, df in all_results.items():
		print(f"\n[{name}]")
		print(df.head(3))
	
	end = time.perf_counter()
	end_ts = datetime.now().isoformat()
	duration = end - start
	logger.info(f"Process completed. Duration: {duration:.2f} seconds. Start: {start_ts}, End: {end_ts}.")
	
start_process()