import requests
import time
import tweepy
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Function to post on Facebook
def post_on_facebook(access_token, message):
    url = f"https://graph.facebook.com/me/feed?access_token={access_token}"
    data = {
        'message': message
    }
    response = requests.post(url, data=data)
    return response.json()

# Function to post on LinkedIn
def post_on_linkedin(access_token, message):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'author': 'urn:li:person:YOUR_LINKEDIN_ID',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': message
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to post on Twitter
def post_on_twitter(api_key, api_secret_key, access_token, access_token_secret, message):
    auth = tweepy.OAuth1Session(api_key, api_secret_key, access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(message)

# Function to post on Pinterest
def post_on_pinterest(access_token, message):
    # Implementation for Pinterest API
    pass

# Route for rendering the form
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling form submission
@app.route('/post', methods=['POST'])
def post():
    platform = request.form['platform']
    message = request.form['message']
    if platform == 'facebook':
        access_token = request.form['access_token']
        post_on_facebook(access_token, message)
    elif platform == 'linkedin':
        access_token = request.form['access_token']
        post_on_linkedin(access_token, message)
    elif platform == 'twitter':
        api_key = request.form['api_key']
        api_secret_key = request.form['api_secret_key']
        access_token = request.form['access_token']
        access_token_secret = request.form['access_token_secret']
        post_on_twitter(api_key, api_secret_key, access_token, access_token_secret, message)
    elif platform == 'pinterest':
        access_token = request.form['access_token']
        post_on_pinterest(access_token, message)
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
