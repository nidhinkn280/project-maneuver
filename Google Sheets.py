import gspread
from oauth2client.service_account import ServiceAccountCredentials

def push_to_google_sheets(data):
    scope = ["https://docs.google.com/spreadsheets"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("project-maneuver.json", scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open_by_key("1-D98mKKkJHgPStql6t5morDFV6HXLFzt5NUnjPkhLh4").sheet1

    # Clear existing data
    sheet.clear()

    # Append new data
    for row in data:
        sheet.append_row(row)

# Example usage:
data = [
    ["Date", "Sales", "Orders"],
    ["2024-04-01", 100, 10],
    ["2024-04-02", 150, 15],
    ["2024-04-03", 200, 20]
]
push_to_google_sheets(data)
