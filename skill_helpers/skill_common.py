"""Come helers that sklls use."""

# --------------- Helpers that build all of the responses ---------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session, text_type='PlainText'):
    """Build speechlet response."""
    return {
        'outputSpeech': {
            'type': text_type,
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': text_type,
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """Build response object."""
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
