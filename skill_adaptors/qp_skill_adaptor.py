"""QP Skill Adapator Module."""
from skill_helpers import build_response, build_speechlet_response


class QPSkillAdaptor(object):
    """Translates skill logic into QP game logic."""

    def __init__(self):
        """Build QP Skill Adaptor."""

    def on_intent(self, intent_data, session):
        """Route intents within qp."""
        return build_response({}, build_speechlet_response(
                "Quick Particle",
                "Welcome to quick particle. Content coming soon,",
                None, True))
