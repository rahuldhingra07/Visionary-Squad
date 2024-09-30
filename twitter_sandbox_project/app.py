# author : Priyanka Angad Jadhav 
from flask import Flask, request, render_template, redirect, url_for
from requests_oauthlib import OAuth1Session
import json

app = Flask(__name__)

bearer_token = "AAAAAAAAAAAAAAAAAAAAAGI6vwEAAAAAFL%2BDQt6BFRFlZ44YGM4iU5xvnMw%3DD9SU6Kyz0zlGaZTTN5E9wgmob0EMC0FGT8jSWbiaL5Lj6mouiw"

api_key = "9L3mndPgPbdLuBFkZV0Srd9GE"
api_secret_key = "YPRqADOgMdUJ04NAkA6d721fk74Wwj7y81pdJvmqMQxCtX1DdZ"
access_token = "1833269658281250819-MGlETlWY9NAYl8eXMUh8ttK4F2ph28"
access_token_secret = "wWoDiFYAYCb70DkQkFXzBTJe1IHThfSNEKK7oGdgARslK"

def create_oauth_session():
    return OAuth1Session(
        api_key,
        client_secret=api_secret_key,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

def create_tweet(content):
    url = "https://api.twitter.com/2/tweets"
    oauth = create_oauth_session()
    json_data = {"text": content}
    response = oauth.post(url, json=json_data)
    
    if response.status_code != 201:
        print("Error creating tweet:")
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
    
    return response.json()

# author : Priyanka Mutha (Deleting tweet)

def delete_tweet(tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    oauth = create_oauth_session()
    response = oauth.delete(url)
    
    if response.status_code != 200:
        print("Error deleting tweet:")
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
    
    return response.status_code

@app.route('/')
def index():
    message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/create', methods=['POST'])
def create():
    content = request.form['content']
    tweet = create_tweet(content)
    
    if 'data' in tweet:
        tweet_id = tweet['data']['id']
        message = f"Tweet created with ID: {tweet_id}"
    else:
        error_detail = tweet.get('detail', 'Unknown error')
        message = f"Error creating tweet: {error_detail}"
    
    return redirect(url_for('index', message=message))


@app.route('/delete', methods=['POST'])
def delete():
    tweet_id = request.form['tweet_id']
    status_code = delete_tweet(tweet_id)
    
    if status_code == 200:
        message = f"Deleted Tweet with ID: {tweet_id}"
    else:
        message = f"Error deleting tweet. Status Code: {status_code}"
    
    return redirect(url_for('index', message=message))

if __name__ == '__main__':
    app.run(debug=True)
