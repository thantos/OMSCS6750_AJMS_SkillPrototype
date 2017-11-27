from unittest import TestCase
from lambda_function import *
import json
import os.path

def response_text(response):
    return response['response']['outputSpeech']['text']


class TestBasics(TestCase):
    def setUp(self):
        self.scene_name = 'tutorial'
        # https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project/40416154#40416154
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "scenes/tutorial.json")
        self.json = json.load(open(path))
        self.fire_intent = {'name': 'fireIntent'}

    def test_fire_five_times(self):
        session_attributes = {}

        for i in range(5):
            # the tutorial skill requires the user to say 'fire' 5 times
            response = loadScene(self.scene_name, self.fire_intent, session_attributes)

            # after each 'fire' make sure we read the correct statement from the tutorial json
            text = response_text(response)
            expected_text = self.json['rounds'][i]
            self.assertEqual(text, expected_text)

            # this maintains our state throughout the game - one variable 'round' = 0-5
            session_attributes = response['sessionAttributes']
