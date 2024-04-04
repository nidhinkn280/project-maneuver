import requests

def send_to_slack(webhook_url, message):
    payload = {
        "text": message
    }
    requests.post(webhook_url, json=payload)

# Example usage:
webhook_url = "https://hooks.slack.com/services/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"
message = "Performance data has been updated. View the spreadsheet here: https://docs.google.com/spreadsheets/d/1-D98mKKkJHgPStql6t5morDFV6HXLFzt5NUnjPkhLh4/edit?usp=sharing"
send_to_slack(webhook_url, message)
