from __future__ import print_function
from json import loads
import os


# --------------- Helpers that build all of the responses ---------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
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


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior -----------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    card_title = "OMSCS Prototype"
    speech_output = "Thank you for participating in the OMSCS Group Project" \
                    " Combat Game Skill Prototype. "
    return build_speechlet_response(card_title, speech_output, None, False)


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for participating in the OMSCS Group Project" \
                    " Combat Game Skill Prototype. "
    # Setting this to true ends the session and exits the skill.
    return build_speechlet_response(card_title, speech_output, None, True)


def exampleHandler():
    speech_out = "This is an example response, anything else?"
    return build_speechlet_response("Example", speech_out, None, False)


def getSceneName(attributes):
    if attributes is not None and 'scene' in attributes:
        return attributes['scene']
    return None


def loadSceneData(scene_name):
    if scene_name is not None:
        try:
            # https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project/40416154#40416154
            my_path = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(my_path, "scenes/" + scene_name + ".json")
            with open(path) as f:
                return loads(f.read())
        finally:
            pass
    return None


def loadScene(scene_name, intent_data, session_attributes):
    if scene_name is None:
        scene = "tutorial"

    scene_data = loadSceneData(scene_name)

    if scene_data is not None:
        return handleSceneType(
            scene_name, scene_data, intent_data, session_attributes)
    else:
        raise ValueError("Invalid scene: " + scene)


def handleSceneType(scene_name, scene_data, intent_data, session_attributes):
    t = None

    if 'type' in scene_data:
        t = scene_data['type']
    else:
        raise ValueError("Scene is missing type")
    if t == "simple":
        return handleSimpleScene(
            scene_name, scene_data, intent_data, session_attributes)
    else:
        raise ValueError("Unhandled scene type: " + t)


def handleSimpleScene(scene_name, scene_data, intent_data, session_attributes):
    round = 0

    expected_intents = []
    defaults = {}
    reprompt = "come on now"  # sarcasm, choose come up with something else
    cardTitle = scene_data.get('cardTitle', scene_name)
    rounds = []

    if "defaults" in scene_data:
        defaults = scene_data["defaults"]
        if "reprompt" in defaults:
            reprompt = defaults["reprompt"]

    if "expectedIntents" in scene_data:
        expected_intents = scene_data["expectedIntents"]
    else:
        raise ValueError(
            "At least one expected intent required in simple scene" +
            scene_name)

    if session_attributes is not None:
        meta = session_attributes.get("meta", {})
        round = meta.get("round", 0)

    # Only expect intents after the first round
    if round > 0:
        intent_name = intent_data['name']
        if intent_name not in expected_intents:
            default_text = defaults.get('onMissedIntent', 'try again')

            return build_response(
                session_attributes,
                build_speechlet_response(
                    cardTitle, default_text, reprompt, False))

    if "rounds" in scene_data:
        rounds = scene_data["rounds"]
    else:
        raise ValueError("No rounds defined in scene: " + scene_name)

    if len(rounds) <= round:
        return build_response(
            session_attributes,
            build_speechlet_response(
                cardTitle, "thats all folks", None, True))

    r_text = rounds[round]

    return build_response(
        {"scene": scene_name, "meta": {"round": round + 1}},
        build_speechlet_response(
            cardTitle, r_text, reprompt, round + 1 == len(rounds)))


# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId="
          + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    # return build_response(
    #    {"scene": "tutorial", "meta": {"round": 1}},
    #    get_welcome_response())
    return loadScene("tutorial", {}, {})


def catchBaseIntent(intent_name):
    if intent_name == "exampleIntent":
        return exampleHandler()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or \
            intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    return None


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']
    attributes = session['attributes']

    baseResponse = catchBaseIntent(intent_name)

    if baseResponse is not None:
        return build_response(session, baseResponse)

    scene = getSceneName(attributes)

    return loadScene(scene, intent, attributes)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID
    to prevent someone else from configuring a skill that sends requests to
    this function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
