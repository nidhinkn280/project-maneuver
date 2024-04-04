import requests

def fetch_performance_details(shop_domain, access_token):
    url = f"https://betterbody-co-test.myshopify.com/admin/api/2023-01/analytics.json"
    headers = {
    "X-Shopify-Access-Token":access_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    return response_data
shop_domain = betterbody-co-test.myshopify.com
access_token = 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
performance_data = fetch_performance_details(shop_domain, access_token)
print(performance_data)
