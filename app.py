from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pymongo
import uuid
from datetime import datetime

app = Flask(__name__)

# ProxyMesh credentials and endpoint
proxy_host = "us-ca.proxymesh.com"
proxy_port = 31280
proxy_user = "Hitesh_mungara"
proxy_pass = "feqNad-8qymgo-biscym"

# MongoDB connection setup
mongo_client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.qckufju.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['twitter_trends']
collection = db['trending_topics']

# Function to fetch top 5 trending topics
def fetch_trending_topics():
    chrome_options = Options()
    proxy = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # Open Twitter homepage
    driver.get("https://twitter.com/home")
    time.sleep(5)

    try:
        whats_happening_section = driver.find_element(By.XPATH, "//section[@aria-labelledby='accessible-list-0']")
        trending_topics = whats_happening_section.find_elements(By.XPATH, ".//div[@dir='ltr']//span")

        top_5_trending = [topic.text for topic in trending_topics[:5]]
        unique_id = str(uuid.uuid4())
        end_time = datetime.now()
        ip_address = proxy_host

        document = {
            "unique_id": unique_id,
            "trend1": top_5_trending[0] if len(top_5_trending) > 0 else None,
            "trend2": top_5_trending[1] if len(top_5_trending) > 1 else None,
            "trend3": top_5_trending[2] if len(top_5_trending) > 2 else None,
            "trend4": top_5_trending[3] if len(top_5_trending) > 3 else None,
            "trend5": top_5_trending[4] if len(top_5_trending) > 4 else None,
            "end_time": end_time,
            "ip_address": ip_address
        }

        collection.insert_one(document)
        driver.quit()
        return document

    except Exception as e:
        driver.quit()
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['GET'])
def run_script():
    result = fetch_trending_topics()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
