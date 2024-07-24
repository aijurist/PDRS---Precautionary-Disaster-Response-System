import time
import re
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from flask import Blueprint, jsonify, request
from model import make_serializable
import requests

twitter_blueprint = Blueprint('twitter', __name__)

def preprocess_tweet(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip() 
    return text

def extract_mentions(text):
    return re.findall(r'@\w+', text)

def extract_hashtags(text):
    return re.findall(r'#\w+', text)

def login_and_scrape_tweets(username, password, tweet_count=20):
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.get("https://twitter.com/login")

    username_field = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username_field.send_keys(username)
    username_field.send_keys(Keys.ENTER)

    password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)
    time.sleep(10)  

    search_url = 'https://x.com/search?q=(India%20AND%20(Disaster%20OR%20flood%20OR%20drought%20OR%20landslide%20OR%20eruption%20OR%20cyclone%20OR%20earthquake%20OR%20tsunami%20OR%20monsoon%20OR%20storm))%20-("election"%20OR%20"politics")&src=typed_query&f=live'
    driver.get(search_url)
    time.sleep(5)  

    tweet_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(tweet_data) < tweet_count:
        tweets = driver.find_elements(By.CSS_SELECTOR, "[data-testid='tweet']")
        for tweet in tweets:
            tweet_text = tweet.text
            if tweet_text not in tweet_data:
                cleaned_text = preprocess_tweet(tweet_text)
                hashtags = extract_hashtags(tweet_text)
                mentions = extract_mentions(tweet_text)
                tweet_data.append({'text': cleaned_text, 'hashtags': hashtags, 'mentions': mentions})
                if len(tweet_data) >= tweet_count:
                    break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()

    # Manually check and remove any extra tweets
    if len(tweet_data) > tweet_count:
        tweet_data = tweet_data[:tweet_count]

    return tweet_data

def predict_tweets(tweets):
    endpoint_url = 'http://localhost:8080/api_model/predict'
    location_finder_url = 'http://localhost:8080/api_validation/location_finder_twitter'
    get_population_url = 'http://localhost:8080/api_validation/get_population'

    data = {'twitter_data': [tweet['text'] for tweet in tweets]}

    try:
        response = requests.post(endpoint_url, json=data)
        if response.status_code == 200:
            predictions = response.json()
            final_response = {}

            for i, tweet in enumerate(tweets):
                result = predictions.get(str(i + 1))
                final_response[i + 1] = {
                    'text': tweet['text'],
                    'prediction': make_serializable(result['prediction']),
                    'confidence': make_serializable(result['confidence']),
                    'hashtags': tweet['hashtags'],
                    'mentions': tweet['mentions']
                }

                if result['prediction'] == 1:
                    # Make POST request to /api_validation/location_finder_twitter
                    location_response = requests.post(location_finder_url, json={'tweet': tweet['text']})
                    location_status = location_response.json()['status'] 
                    if location_status == 'error':
                        continue
                    if location_response.status_code == 200:
                        location_data = location_response.json()
                        print(location_data)
                        locations = location_data['locations']
                        location_name = locations['location']
                        is_urban = locations['is_urban']

                        final_response[i + 1]['location_data'] = locations

                        # Make POST request to /api_validation/get_population
                        population_data = {
                            'location_name': location_name,
                            'radius': 5,  # Assuming a default radius, adjust as needed
                            'is_urban': is_urban
                        }
                        population_response = requests.post(get_population_url, json=population_data)
                        if population_response.status_code == 200:
                            population_info = population_response.json()
                            final_response[i + 1]['population'] = population_info
                        else:
                            final_response[i + 1]['population'] = 'Failed to get population data'
                    else:
                        final_response[i + 1]['location_data'] = 'Failed to get location data'
            print(final_response)
            return final_response
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

@twitter_blueprint.route('/scrape_twitter', methods=['POST'])   
def run_prediction_script():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    tweet_count = data.get('tweet_count', 20)
    
    tweets = login_and_scrape_tweets(username, password, tweet_count)
    
    if tweets:
        predictions = predict_tweets(tweets)
        if predictions is not None:
            return jsonify(predictions=predictions, tweets=tweets)
        else:
            return jsonify(error="Failed to get predictions from ML model"), 500
    else:
        return jsonify(error="No tweets scraped"), 400