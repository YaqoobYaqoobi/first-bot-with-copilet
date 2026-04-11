import requests

def fetch_news():
    # نمونه ساده: گرفتن اخبار از CoinDesk API
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # در عمل باید از APIهای خبری کریپتو استفاده شود
        return [{"source": "CoinDesk", "headline": "Bitcoin price update", "content_summary": str(data)}]
    else:
        return []
