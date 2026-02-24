import os
from src.logger import get_logger

logger = get_logger(__name__)

def load_queries_from_dir(path="queries", ext=".dax"):
	"""Load all files with extension `ext` from `path` and return dict {name: content}.

	The file name (without extension) will be used as the query key.
	"""
	queries = {}
	if not os.path.isdir(path):
		logger.warning(f"Queries directory '{path}' does not exist. No .dax files loaded.")
		return queries

	for fname in sorted(os.listdir(path)):
		if not fname.lower().endswith(ext.lower()):
			continue
		full = os.path.join(path, fname)
		try:
			with open(full, "r", encoding="utf-8") as f:
				content = f.read()
				key = os.path.splitext(fname)[0]
				queries[key] = content
		except Exception as e:
			logger.error(f"Failed to read query file {full}: {e}")
			
	return queries
