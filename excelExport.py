# import requests
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # 1. Get data from internal API
# response = requests.get("https://api.navigator.server.nvidia.com/api/v1.1/nodeAllocation", verify=False)
# data = response.json()

# # DEBUG: show response
# # print("API Data:", type(data))

# # 2. Auth with Google Sheets
# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)

# # 3. Open your target spreadsheet
# sheet = client.open("Test-Nav").sheet1

# # 4. Extract specific fields (adjust keys based on print output above)
# key1 = data.get('key1', 'MISSING')
# key2 = data.get('key2', 'MISSING')

# # 5. Update the sheet
# sheet.update('A1', [[key1, key2]])

import requests
import pandas as pd

# 1. Get data from internal API
response = requests.get("https://api.navigator.server.nvidia.com/api/v1.1/nodeAllocation", verify=False)
data = response.json()
print("API Data:", type(data))

# DEBUG: Inspect data
# print("API Data:", data)

import pprint
pprint.pprint(data[:2])  # Show first 2 entries

records = []


for item in data:
    record = {
        "id": item.get("id") if item.get("id") else None, 
        "jira_key": item.get("jira_key") if item.get("jira_key") else None,
        "customer": item.get("customer") if item.get("customer") else None,
        "confirmed_quantity": item.get("confirmed_quantity") if item.get("confirmed_quantity") else None,
        "gpu_type": item["confirmed_hw_type"]["gpu_type"] if item.get("confirmed_hw_type") else None,
        "status": item.get("status") if item.get("status") else None,
        "cluster_type": item.get("cluster_type") if item.get("cluster_type") else None,
        "use_case_type": item.get("use_case_type") if item.get("use_case_type") else None,
        "csp": item["csp"]["csp"] if item.get("csp") else None,
    }
    records.append(record)

# 3. Create DataFrame and save to Excel
df = pd.DataFrame(records)
df.to_excel("node_allocations2.xlsx", index=False)
