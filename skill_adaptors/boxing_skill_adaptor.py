""""""
from skill_helpers import build_response, build_speechlet_response

from boxing import update_with_intent, reprompt, game_over

class BoxingSkillAdaptor(object):
    """Translates skill interactions into boxing game interactions."""

    def on_intent(self, intent_data, session):
        meta = None
        if session:
            meta = session['meta']

        session = update_with_intent(intent_data, meta)
        speech = session['speech']
        reprmp = reprompt(session)
        should_end = game_over(session)
        session_attributes = {'scene': 'boxing', 'meta':session}
        response = build_speechlet_response("Boxing",
                                            speech,
                                            reprompt_text=reprmp,
                                            should_end_session=should_end,
                                            plain_text=False)

        return build_response(session_attributes, response)


