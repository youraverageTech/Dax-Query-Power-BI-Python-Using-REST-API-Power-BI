# Project — DAX Query Power BI via Python Using Power BI REST API
This documentation explains the project purpose, tools/libraries used, configuration, and the workflow to run DAX queries against Power BI and export the results.

## Summary
This Python script retrieves data/insights from a Power BI dataset using DAX queries and Power BI REST API for the connection.

## Tools / Dependencies
- Python.
- Python libraries (install via `pip`):
  - `msal` — for Azure AD authentication (client credentials flow)
  - `requests` — for HTTP requests to the Power BI REST API
  - `pandas` — for table manipulation and storage
  - `python-dotenv` — to load environment variables from a `.env` file
  - `openpyxl` — engine for writing Excel files
  - `pyyaml` - library for read yaml file.

Example installation:

```bash
pip install msal requests pandas python-dotenv openpyxl
```

## External services required
- Microsoft account and Power BI Pro / Premium Per User license.
- Azure Active Directory — an app registration (client) with permissions to the Power BI API.
- Power BI service — a dataset that can be queried (you will need the `dataset_id`).

## Configuration
Create a `.env` file in the project root containing:

```
client_id=YOUR_CLIENT_ID
tenant_id=YOUR_TENANT_ID
client_secret=YOUR_CLIENT_SECRET
dataset_id=YOUR_POWERBI_DATASET_ID
```

## Brief file structure
- `main.py` — the main script to execute project.
- `readme_en.md` — documentation of the project.
- `.env` — environment configuration (user-provided).
- `requirments.txt` - libraries python needed for this project.
- `all_output.xlsx` — output file containing results of all queries.
- `queries` - a folder that stores dax query files.
- `src` - a folder that stores python module.
  - `authenticate.py` - python module for authentication process.
  - `import_from_dir.py` - python module for import dax query from dax format files.
  - `import_from_yaml.py` - python module for import dax query from yaml file.
  - `export_to_excel.py` - python module for export output into excel format.
  - `execute_dax.py` - python module for process dax query.
  - `parse_pandas.py` - python module for parse output into pandas dataframe.
  - `multiple_execute_query.py` - python module for executing many dax queries into one single process.
  - `logger.py` - python module for logging information.
- `logs` - all logs information stored.
- `output` - all outputs stored.

### Diagram — Brief File Structure (current)

```
Project_test/
├─ .env                # environment variables (not committed)
├─ requirements.txt     # Python dependencies
├─ main.py             # entry point
├─ readme.md
├─ readme_en.md
├─ logs/               # runtime logs (created when logging enabled)
├─ output/             # any produced artifacts
├─ queries/            # all dax queries stored
├─ src/
│  ├─ __init__.py
│  ├─ authenticate.py
│  ├─ import_from_dir.py
│  ├─ import_from_yaml.py
│  ├─ execute_dax.py
│  ├─ parse_pandas.py
│  ├─ multiple_execute_query.py
│  ├─ export_to_excel.py
│  └─ logger.py
└─ (other files)
```

## Workflow
1. Create or use an existing workspace in the Power BI service.
2. Publish or ensure the dataset is available in the workspace; record the `dataset_id`.
3. Register an application (app registration) in Azure AD:
   - Create an app registration and note `client_id`, `tenant_id`, and `client_secret`.
   - Grant application permissions for the Power BI API and provide admin consent (admin/contributor).
4. Add the configuration values to the `.env` file.
   - client_id
   - tenant_id
   - dataset_id
   - client_secret
5. Install local dependencies:

```bash
pip install -r requirements.txt
```

or directly:

```bash
pip install msal requests pandas python-dotenv openpyxl
```

7. Create DAX query and save into queries folder. The formats for dax query files that can be processed in this project include dax and yaml formats. Warning on dax query if using measure that has been created and entered into a table such as table _measure, in the dax query the code _measure needs to be removed.
8. Run the script:

```bash
python3 -m main.py
```

9. Check the output in folder output.
