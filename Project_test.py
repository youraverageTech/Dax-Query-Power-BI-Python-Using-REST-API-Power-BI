import msal
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# 2. Authenticate (Interactive login for Mac)
def authentication(client_id, authority, client_secret):
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=AUTHORITY,
        client_credential=client_secret,
    )

    token_result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in token_result:
        raise Exception("Failed to get access token")

    access_token = token_result["access_token"]

    return access_token
    
    # 3. Your DAX Query
def execute_dax_query(access_token, dataset_id, dax_query):
    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    dax_query = {
            "queries": [{"query": dax_query}],
        "serializerSettings": {
            "includeNulls": True} # Put your full DAX here
        }
        
        # 4. Execute
    response = requests.post(url, json=dax_query, headers=headers)

    if response.status_code != 200:
        print("Error:", response.text)
        raise Exception("Query failed")

    result = response.json()

    return result
    
    # 5. Parse to Pandas
def parse_to_pandas(result):
    data = result['results'][0]['tables'][0]['rows']
    return pd.DataFrame(data)


def multiple_execute_dax_query(access_token, dataset_id, query_dict, export=True, export_format="csv"):
    results = {}
    for query_name, query_dax in query_dict.items():
        try:
            raw_result = execute_dax_query(access_token, dataset_id, query_dax)
            df = parse_to_pandas(raw_result)
            results[query_name] = df

            # exporting df to csv
            if export and not df.empty:
                if export_format == "csv":
                    df.to_csv(f'{query_name}.csv', index=False)
                elif export_format == "excel":
                    df.to_excel(f"{query_name}.xlsx", index=False)
        except Exception as e:
            print(e)
            results[query_name] = pd.DataFrame()
    return results

def export_to_excel_multisheet(results_dict, filename="hasil_semua_query.xlsx"):
    """Ekspor semua DataFrame ke satu file Excel, masing-masing jadi sheet."""
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for sheet_name, df in results_dict.items():
            if not df.empty:
                # Excel sheet name max 31 karakter
                safe_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=safe_name, index=False)
    print(f"Semua hasil disimpan ke: {filename}")

if __name__ == "__main__":
    # 1. Configuration
    load_dotenv()
    client_id = os.getenv("client_id")
    tenant_id = os.getenv("tenant_id")
    dataset_id = os.getenv("dataset_id")
    client_secret = os.getenv("client_secret")
    AUTHORITY = f"https://login.microsoftonline.com/{tenant_id}"
    SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
    
    query_dict = {
        "query-1" : """
DEFINE 
VAR __DS0FilterTable =
TREATAS({"February"}, 'dim_date'[Month Name])

EVALUATE
    SUMMARIZECOLUMNS(
        __DS0FilterTable,
        "Total_YTD", IGNORE([Total YTD]),
        "Target_YTD", IGNORE([Target YTD]),
        "Total_YTD_Last_Year", IGNORE([Total YTD Last Year]),
        "Target_YTD_Last_Year", IGNORE([Target YTD Last Year]),
        "Varriance", IGNORE([Varriance]),
        "Last_Year_Varriance", IGNORE([Last Year Varriance]),
        "YoY_Growth", IGNORE([YoY Growth]),
        "v__Varriance", IGNORE([% Varriance]),
        "v__Varriance_Last_Year", IGNORE([% Varriance Last Year]),
        "v__YoY_Growth", IGNORE([% YoY Growth]))
""",    
        "query-2" : """
DEFINE
	VAR __DS0FilterTable = 
		TREATAS({"February"}, 'dim_date'[Month Name])

	VAR __DS0Core = 
		SUMMARIZECOLUMNS(
			ROLLUPADDISSUBTOTAL('dim_product'[product_name], "IsGrandTotalRowTotal"),
			__DS0FilterTable,
			"Total_YTD", [Total YTD],
			"Target_YTD", [Target YTD],
			"Total_YTD_Last_Year", [Total YTD Last Year],
			"Target_YTD_Last_Year", [Target YTD Last Year],
			"Varriance", [Varriance],
			"Last_Year_Varriance", [Last Year Varriance],
			"YoY_Growth", [YoY Growth],
			"v__Varriance", [% Varriance],
			"v__Varriance_Last_Year", [% Varriance Last Year],
			"v__YoY_Growth", [% YoY Growth]
		)

	VAR __DS0PrimaryWindowed = 
		TOPN(502, __DS0Core, [IsGrandTotalRowTotal], 0, 'dim_product'[product_name], 1)

EVALUATE
	__DS0PrimaryWindowed

ORDER BY
	[IsGrandTotalRowTotal] DESC, 'dim_product'[product_name]
""",    
        "query-3" : """
DEFINE VAR __DS0FilterTable =
    TREATAS({"February"}, 'dim_date'[Month Name])

EVALUATE
    SUMMARIZECOLUMNS(
        __DS0FilterTable,
        "Total_YTD", IGNORE([Total YTD]),
        "Varriance", IGNORE([Varriance]),
        "Target_YTD", IGNORE([Target YTD]),
        "v__Varriance", IGNORE([% Varriance]))
""",    
        "query-4" : """
DEFINE
	VAR __DS0FilterTable = 
		TREATAS({"February"}, 'dim_date'[Month Name])

	VAR __ValueFilterDM1 = 
		FILTER(
			KEEPFILTERS(
				SUMMARIZECOLUMNS(
					'dim_product'[product_name],
					__DS0FilterTable,
					"Total_YTD", [Total YTD],
					"Target_YTD", [Target YTD],
					"Achievment_Status", [Achievment Status],
					"Varriance", [Varriance],
					"v__Varriance", [% Varriance]
				)
			),
			[Achievment_Status] = "Achieved"
		)

	VAR __DS0Core = 
		SUMMARIZECOLUMNS(
			ROLLUPADDISSUBTOTAL('dim_product'[product_name], "IsGrandTotalRowTotal"),
			__DS0FilterTable,
			__ValueFilterDM1,
			"Total_YTD", [Total YTD],
			"Target_YTD", [Target YTD],
			"Achievment_Status", [Achievment Status],
			"Varriance", [Varriance],
			"v__Varriance", [% Varriance]
		)

	VAR __DS0PrimaryWindowed = 
		TOPN(502, __DS0Core, [IsGrandTotalRowTotal], 0, 'dim_product'[product_name], 1)

EVALUATE
	__DS0PrimaryWindowed

ORDER BY
	[IsGrandTotalRowTotal] DESC, 'dim_product'[product_name]
""",
        "query-5" : """
DEFINE
	VAR __DS0FilterTable = 
		TREATAS({"February"}, 'dim_date'[Month Name])

	VAR __ValueFilterDM1 = 
		FILTER(
			KEEPFILTERS(
				SUMMARIZECOLUMNS(
					'dim_product'[product_name],
					__DS0FilterTable,
					"Total_YTD", [Total YTD],
					"Target_YTD", [Target YTD],
					"Achievment_Status", [Achievment Status],
					"Varriance", [Varriance],
					"v__Varriance", [% Varriance]
				)
			),
			[Achievment_Status] <> "Achieved"
		)

	VAR __DS0Core = 
		SUMMARIZECOLUMNS(
			ROLLUPADDISSUBTOTAL('dim_product'[product_name], "IsGrandTotalRowTotal"),
			__DS0FilterTable,
			__ValueFilterDM1,
			"Total_YTD", [Total YTD],
			"Target_YTD", [Target YTD],
			"Achievment_Status", [Achievment Status],
			"Varriance", [Varriance],
			"v__Varriance", [% Varriance]
		)

	VAR __DS0PrimaryWindowed = 
		TOPN(502, __DS0Core, [IsGrandTotalRowTotal], 0, 'dim_product'[product_name], 1)

EVALUATE
	__DS0PrimaryWindowed

ORDER BY
	[IsGrandTotalRowTotal] DESC, 'dim_product'[product_name]
""", 
        "query-6" : """
DEFINE 
    VAR __DS0FilterTable =
    TREATAS({"February"}, 'dim_date'[Month Name])

EVALUATE
    SUMMARIZECOLUMNS(
        __DS0FilterTable,
        "Total_YTD_Last_Year", IGNORE([Total YTD Last Year]),
        "Target_YTD_Last_Year", IGNORE([Target YTD Last Year]),
        "Last_Year_Varriance", IGNORE([Last Year Varriance]),
        "v__Varriance_Last_Year", IGNORE([% Varriance Last Year]))
""",
        "query-7" : """
DEFINE
	VAR __DS0FilterTable = 
		TREATAS({"February"}, 'dim_date'[Month Name])

	VAR __ValueFilterDM1 = 
		FILTER(
			KEEPFILTERS(
				SUMMARIZECOLUMNS(
					'dim_product'[product_name],
					__DS0FilterTable,
					"Total_YTD_Last_Year", [Total YTD Last Year],
					"Target_YTD_Last_Year", [Target YTD Last Year],
					"Last_Year_Varriance", [Last Year Varriance],
					"v__Varriance_Last_Year", [% Varriance Last Year],
					"Achievment_Measure_Last_year", [Achievment Measure Last year]
				)
			),
			[Achievment_Measure_Last_year] = "Achieved"
		)

	VAR __DS0Core = 
		SUMMARIZECOLUMNS(
			ROLLUPADDISSUBTOTAL('dim_product'[product_name], "IsGrandTotalRowTotal"),
			__DS0FilterTable,
			__ValueFilterDM1,
			"Total_YTD_Last_Year", [Total YTD Last Year],
			"Target_YTD_Last_Year", [Target YTD Last Year],
			"Last_Year_Varriance", [Last Year Varriance],
			"v__Varriance_Last_Year", [% Varriance Last Year],
			"Achievment_Measure_Last_year", [Achievment Measure Last year]
		)

	VAR __DS0PrimaryWindowed = 
		TOPN(502, __DS0Core, [IsGrandTotalRowTotal], 0, 'dim_product'[product_name], 1)

EVALUATE
	__DS0PrimaryWindowed

ORDER BY
	[IsGrandTotalRowTotal] DESC, 'dim_product'[product_name]
""",
        "query-8" : """
DEFINE
	VAR __DS0FilterTable = 
		TREATAS({"February"}, 'dim_date'[Month Name])

	VAR __ValueFilterDM1 = 
		FILTER(
			KEEPFILTERS(
				SUMMARIZECOLUMNS(
					'dim_product'[product_name],
					__DS0FilterTable,
					"Total_YTD_Last_Year", [Total YTD Last Year],
					"Target_YTD_Last_Year", [Target YTD Last Year],
					"Last_Year_Varriance", [Last Year Varriance],
					"v__Varriance_Last_Year", [% Varriance Last Year],
					"Achievment_Measure_Last_year", [Achievment Measure Last year]
				)
			),
			[Achievment_Measure_Last_year] <> "Achieved"
		)

	VAR __DS0Core = 
		SUMMARIZECOLUMNS(
			ROLLUPADDISSUBTOTAL('dim_product'[product_name], "IsGrandTotalRowTotal"),
			__DS0FilterTable,
			__ValueFilterDM1,
			"Total_YTD_Last_Year", [Total YTD Last Year],
			"Target_YTD_Last_Year", [Target YTD Last Year],
			"Last_Year_Varriance", [Last Year Varriance],
			"v__Varriance_Last_Year", [% Varriance Last Year],
			"Achievment_Measure_Last_year", [Achievment Measure Last year]
		)

	VAR __DS0PrimaryWindowed = 
		TOPN(502, __DS0Core, [IsGrandTotalRowTotal], 0, 'dim_product'[product_name], 1)

EVALUATE
	__DS0PrimaryWindowed

ORDER BY
	[IsGrandTotalRowTotal] DESC, 'dim_product'[product_name]
"""
    }

    access_token = authentication(client_id, AUTHORITY, client_secret)
    all_results = multiple_execute_dax_query(
        access_token=access_token,
        dataset_id=dataset_id,
        query_dict=query_dict,
        export=False,
        export_format="csv"
    )

    export_to_excel_multisheet(all_results, filename="all_output.xlsx")

    print("\nPreview masing-masing hasil:")
    for name, df in all_results.items():
        print(f"\n[{name}]")
        print(df.head(3))