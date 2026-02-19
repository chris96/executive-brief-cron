import requests
import feedparser
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== CONFIG ==========
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")

# ========== FUNCTIONS ==========

def get_market_snapshot():
    response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=^GSPC,^DJI,^IXIC")
    data = response.json()["quoteResponse"]["result"]

    snapshot = []
    for item in data:
        snapshot.append(
            f"{item['shortName']}: {item['regularMarketPrice']} ({item['regularMarketChangePercent']:.2f}%)"
        )
    return "\n".join(snapshot)

def get_ai_accounting_news():
    feed = feedparser.parse("https://news.google.com/rss/search?q=AI+accounting")
    articles = feed.entries[:5]
    news = ""
    for article in articles:
        news += f"- {article.title}\n"
    return news

def build_email_body():
    today = datetime.now().strftime("%B %d, %Y")
    market = get_market_snapshot()
    news = get_ai_accounting_news()

    return f"""
Daily Executive Brief
Date: {today}

=== Market Snapshot ===
{market}

=== AI in Accounting News ===
{news}
"""

def send_email(body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = "Daily Executive Brief"

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# ========== RUN ==========
if __name__ == "__main__":
    email_body = build_email_body()
    send_email(email_body)
    print("Executive Brief Sent Successfully.")
