import os
import tempfile
import tweepy
import random

from wand.image import Image

from google.cloud import storage, vision

consumer_key= os.environ.get('consumer_key')
consumer_secret=os.environ.get('consumer_secret')
access_token=os.environ.get('access_token')
access_token_secret=os.environ.get('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

storage_client = storage.Client()

def blur_offensive_images(data, context):
    file_data = data

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]
    

    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f"gs://{bucket_name}/{file_name}"
    blob_source =vision.Image(source=vision.ImageSource(image_uri=blob_uri))
    
    file_name = blob.name
    _, temp_local_filename = tempfile.mkstemp()
    
    
    blob.download_to_filename(temp_local_filename)

    api = tweepy.API(auth)
    
    tweets=["Stop Hostile Architecture! We want our streets back.","This should not exist in our public spaces", "#hostilearchiteture"]
    
    tweet_content=random.choice(tweets)

    api.update_with_media(temp_local_filename, status=tweet_content)

    return

