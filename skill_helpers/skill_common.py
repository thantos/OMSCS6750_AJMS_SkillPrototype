"""Come helers that sklls use."""


# --------------- Helpers that build all of the responses ---------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session, plain_text=True):
    """Build speechlet response."""
    if plain_text:
        return build_speechlet_response_plain(title, output, reprompt_text, should_end_session)
    else:
        return build_speechlet_response_ssml(title, output, reprompt_text, should_end_session)


def build_speechlet_response_plain(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_ssml(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
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
