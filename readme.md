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
- `main.py` — the main script containing authentication, DAX execution, parsing to pandas, and export functions.
- `readme_en.md` — documentation of the project.
- `.env` — environment configuration (user-provided).
- `requirments.txt` - libraries python needed for this project.
- `all_output.xlsx` — output file containing results of all queries.

## Workflow
1. Create or use an existing workspace in the Power BI service.
2. Publish or ensure the dataset is available in the workspace; record the `dataset_id`.
3. Register an application (app registration) in Azure AD:
   - Create an app registration and note `client_id`, `tenant_id`, and `client_secret`.
   - Grant application permissions for the Power BI API and provide admin consent (admin/contributor).
4. Add the configuration values to the `.env` file.
5. Install local dependencies:

```bash
pip install -r requirements.txt
```

or directly:

```bash
pip install msal requests pandas python-dotenv openpyxl
```

7. create DAX query.
8. Run the script:

```bash
python3 -m main.py
```

9. Check the output file `all_output.xlsx`.
