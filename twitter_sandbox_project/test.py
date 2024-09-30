# author : Rahul Dhingra

import unittest
from app import app, create_tweet, delete_tweet
import random

class TwitterServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_tweet(self):
        random_content = f"Test tweet content {random.randint(0, 10000)}"
        with self.app as client:
            response = client.post('/create', data={'content': random_content}, follow_redirects=True)
            self.assertIn(b'Tweet created with ID', response.data)

    def test_delete_tweet(self):
        tweet = create_tweet('Test tweet to delete')
        tweet_id = tweet['data']['id']
        response = delete_tweet(tweet_id)
        self.assertEqual(response, 200)

if __name__ == '__main__':
    unittest.main()
