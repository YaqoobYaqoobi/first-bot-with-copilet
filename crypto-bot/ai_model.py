from data.sentiment_analysis import analyze_sentiment

def analyze_market(technical_data, fundamental_data):
    score = technical_data.get('trend_score',0) + fundamental_data.get('sentiment_score',0)
    if score > 1.5:
        return "BUY"
    elif score < -1.5:
        return "SELL"
    else:
        return "HOLD"

def process_news(news_list):
    sentiment_total = 0
    for news in news_list:
        sentiment_total += analyze_sentiment(news["headline"] + " " + news["content_summary"])
    return {"sentiment_score": sentiment_total}
