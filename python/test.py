'''from twitter import login_and_scrape_tweets, predict_tweets
if __name__ == "__main__":
    username = "ShanthoshS32920"  
    password = "Hackfest123!"

    tweets = login_and_scrape_tweets(username, password)
    predictions = predict_tweets(tweets)
    
    if predictions:
        for i, tweet in enumerate(tweets):
            prediction = predictions.get(str(i + 1), {})
            tweet['prediction'] = prediction.get('prediction', 'N/A')
            tweet['confidence'] = prediction.get('confidence', 'N/A')
            print(f"Tweet: {tweet['text']}\nHashtags: {tweet['hashtags']}\nMentions: {tweet['mentions']}\nPrediction: {tweet['prediction']}\nConfidence: {tweet['confidence']}\n")'''
            
import requests

tweet = "The body of a woman who went missing following a landslide in Shirur village in Uttara Kannada district was recovered from the Gangavalli river on Tuesday during search operation, taking the death toll to eight, police said"
response = requests.post('http://localhost:8080/api_validation/location_finder_twitter', json={"tweet": tweet})

if response.ok:
    data = response.json()
    print(data['locations'])
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
