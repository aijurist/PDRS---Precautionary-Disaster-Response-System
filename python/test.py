from twitter import login_and_scrape_tweets, predict_tweets

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
            print(f"Tweet: {tweet['text']}\nHashtags: {tweet['hashtags']}\nMentions: {tweet['mentions']}\nPrediction: {tweet['prediction']}\nConfidence: {tweet['confidence']}\n")