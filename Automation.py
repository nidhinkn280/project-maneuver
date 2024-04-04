import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slack_sdk import WebClient
from datetime import datetime, timedelta
ACCESS_TOKEN = "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"
SHOP_URL = "betterbody-co-test.myshopify.com"
# Google Sheets credentials
GOOGLE_SHEET_KEY = "4c7dcf4f3054ad557cca0b7ba0a3dcd51f4280d9"
SCOPE = ["https://docs.google.com/spreadsheets"]
CREDS_FILE = "project-maneuver.json"  # Path to your Google Sheets credentials JSON file

# Slack credentials
SLACK_TOKEN = "xoxe.xoxp-1-Mi0yLTY5MjU0NTAxMDgyODgtNjkwMjY2NTIxODU3OC02OTExNTE3MzcwNDIwLTY5MzI0NTg3OTc0MDgtZDBlMGYzZTdjNjE1YjhmOGYyNzBmY2E3OTU1ZDU4MzNhZDliNDMzNzI0NjM4YzQ0NGRiZGM4NTk1NTA3Y2NhNQ"
SLACK_CHANNEL = "project-maneuver"

# Function to fetch data from Shopify
def fetch_shopify_data(date):
    endpoint = f"https://betterbody-co-test.myshopify.com/admin/api/2024-04/orders.json"
    headers = {"Content-Type": "application/json"}
    params = {
      ACCESS_TOKEN = "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"
        "date": date.strftime("%Y-%m-%d"),
    }
    response = requests.get(endpoint, headers=headers, params=params)
    data = response.json()
    return data

# Function to calculate metrics
def calculate_metrics(data):
    total_sessions = data["total_sessions"]
    total_revenue = data["total_revenue"]
    total_orders = data["total_orders"]
    conversion_rate = total_orders / total_sessions if total_sessions > 0 else 0
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0
    return total_sessions, total_revenue, total_orders, conversion_rate, average_order_value

# Function to authenticate and access Google Sheets
def access_google_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_KEY).sheet1
    return sheet

# Function to update Google Sheet
def update_google_sheet(sheet, date, metrics):
    row = [date.strftime("%Y-%m-%d")] + list(metrics)
    sheet.append_row(row)

# Function to send data to Slack
def send_to_slack(message):
    client = WebClient(token=SLACK_TOKEN)
    client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

# Main function
def main():
    # Dates to retrieve data for
    assigned_date = datetime(2024, 3, 25)
    dates_to_fetch = [
        assigned_date - timedelta(days=1),
        assigned_date - timedelta(days=2),
        assigned_date.replace(day=assigned_date.day - 30)
    ]

    # Fetch data for each date and update Google Sheet
    for date in dates_to_fetch:
        data = fetch_shopify_data(date)
        metrics = calculate_metrics(data)
        sheet = access_google_sheet()
        update_google_sheet(sheet, date, metrics)

    # Send confirmation message to Slack
    send_to_slack("Performance data has been updated in the Google Sheet.")

if __name__ == "__main__":
    main()
