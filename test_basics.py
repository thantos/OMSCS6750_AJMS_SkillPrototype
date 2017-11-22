from unittest import TestCase
from lambda_function import *
import json


def response_text(response):
    return response['response']['outputSpeech']['text']


class TestBasics(TestCase):
    def setUp(self):
        self.scene_name = 'tutorial'
        self.json = json.load(open('scenes/tutorial.json'))
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
