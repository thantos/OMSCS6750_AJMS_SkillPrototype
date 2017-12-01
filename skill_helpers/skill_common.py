"""Some helpers that sklls use."""


# --------------- Helpers that build all of the responses ---------------------

def build_speechlet_response_enahnced(
                                output, reprompt=None,
                                card=None, should_end_session=False):
    return {
        'outputSpeech': output.__dict__,
        'card': card.__dict__ if card is not None else None,
        'reprompt': {
            'outputSpeech': reprompt.__dict__
        } if reprompt is not None else None,
        'shouldEndSession': should_end_session
    }


def build_speechlet_response(
            title, output, reprompt_text, should_end_session, plain_text=True):
    """Build speechlet response."""
    o = PlainResponse(output) if plain_text else SSMLResponse(output)
    r = None if reprompt_text is None else \
        (PlainResponse(reprompt_text)
         if plain_text else SSMLResponse(reprompt_text))

    return build_speechlet_response_enahnced(
        o, r, SimpleCard(title, output)
        if title is not None else None,
        should_end_session)


def build_response(session_attributes, speechlet_response):
    """Build response object."""
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


class PlainResponse(object):

    def __init__(self, text):
        self.type = "PlainText"
        self.text = text


class SSMLResponse(object):

    def __init__(self, text):
        self.type = "SSML"
        self.ssml = \
            "<speak>" + text + "</speak>" \
            if not text.startswith("<speak>") else text


class SimpleCard(object):

    def __init__(self, title, text):
        self.type = "Simple"
        self.content = text
        self.title = title
