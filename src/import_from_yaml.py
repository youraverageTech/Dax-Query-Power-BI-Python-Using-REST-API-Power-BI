import os 
import yaml
from src.logger import get_logger

logger = get_logger(__name__)

def load_query_from_yaml(path="queries.yaml"):
	if not os.path.isfile(path):
		logger.warning(f"YAML query file '{path}' does not exist. No YAML queries loaded.")
		return {}
	try:
		with open(path, "r", encoding="utf-8") as f:
			data = yaml.safe_load(f)
			if not isinstance(data, dict):
				logger.error(f"YAML file {path} does not contain a dict at the top level.")
				return {}
			return data
	except Exception as e:
		logger.error(f"Failed to read YAML query file {path}: {e}")
		return {}
