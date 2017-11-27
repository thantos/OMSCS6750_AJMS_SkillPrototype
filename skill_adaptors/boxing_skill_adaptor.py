""""""
from skill_helpers import build_response, build_speechlet_response


class BoxingSkillAdaptor(object):
    """Translates skill interactions into boxing game interactions."""

    def on_intent(intent_data, session):
        return build_response({}, build_speechlet_response(
                "Boxing",
                "Welcome to boxing. Content coming soon,",
                None, True))
