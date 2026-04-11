from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return 1   # مثبت
    elif polarity < -0.1:
        return -1  # منفی
    else:
        return 0   # خنثی
