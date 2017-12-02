from unittest import TestCase
from .skill_common import *


class SkillCommonTests(TestCase):

    def test_build_sp_resp_enhanced_should_handle_ssml(self):
        test_resp = "Test me"
        resp = build_speechlet_response_enahnced(SSMLResponse(test_resp))

        self.assertIn(test_resp, resp["outputSpeech"]["ssml"])
        self.assertTrue(resp["outputSpeech"]["ssml"].startswith("<speak>"))
        self.assertTrue(resp["outputSpeech"]["ssml"].endswith("</speak>"))

    def test_build_sp_resp_enhanced_should_handle_plain(self):
        test_resp = "Test me"
        resp = build_speechlet_response_enahnced(PlainResponse(test_resp))

        self.assertIn(test_resp, resp["outputSpeech"]["text"])
        self.assertFalse(resp["outputSpeech"]["text"].startswith("<speak>"))
        self.assertFalse(resp["outputSpeech"]["text"].endswith("</speak>"))

    def test_build_sp_resp_enhanced_should_merge_ssml(self):
        test_resp = "Test me"
        test_resp2 = "Em Tset"
        resp = build_speechlet_response_enahnced(
            [SSMLResponse(test_resp), SSMLResponse(test_resp2)])

        self.assertIn(test_resp, resp["outputSpeech"]["ssml"])
        self.assertIn(test_resp2, resp["outputSpeech"]["ssml"])
        self.assertTrue(resp["outputSpeech"]["ssml"].startswith("<speak>"))
        self.assertTrue(resp["outputSpeech"]["ssml"].endswith("</speak>"))

    def test_build_sp_resp_enhanced_should_merge_ssml_and_pt(self):
        test_resp = "Test me"
        test_resp2 = "Em Tset"
        resp = build_speechlet_response_enahnced(
            [SSMLResponse(test_resp), PlainResponse(test_resp2)])

        self.assertIn(test_resp, resp["outputSpeech"]["ssml"])
        self.assertIn(test_resp2, resp["outputSpeech"]["ssml"])
        self.assertTrue(resp["outputSpeech"]["ssml"].startswith("<speak>"))
        self.assertTrue(resp["outputSpeech"]["ssml"].endswith("</speak>"))

    def test_build_sp_resp_enhanced_should_merge_pt_and_ssml(self):
        test_resp = "Test me"
        test_resp2 = "Em Tset"
        resp = build_speechlet_response_enahnced(
            [PlainResponse(test_resp2), SSMLResponse(test_resp)])

        self.assertIn(test_resp, resp["outputSpeech"]["ssml"])
        self.assertIn(test_resp2, resp["outputSpeech"]["ssml"])
        self.assertTrue(resp["outputSpeech"]["ssml"].startswith("<speak>"))
        self.assertTrue(resp["outputSpeech"]["ssml"].endswith("</speak>"))

    def test_build_sp_resp_enhanced_should_merge_pt(self):
        test_resp = "Test me"
        test_resp2 = "Em Tset"
        resp = build_speechlet_response_enahnced(
            [PlainResponse(test_resp2), PlainResponse(test_resp)])

        self.assertIn(test_resp, resp["outputSpeech"]["text"])
        self.assertIn(test_resp2, resp["outputSpeech"]["text"])
        self.assertFalse(resp["outputSpeech"]["text"].startswith("<speak>"))
        self.assertFalse(resp["outputSpeech"]["text"].endswith("</speak>"))
