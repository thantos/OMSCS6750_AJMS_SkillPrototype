""""""
from skill_helpers import build_response, build_speechlet_response

import match
import phrase_builder

from boxing_strings import *


class BoxingSkillAdaptor(object):
    """Translates skill interactions into boxing game interactions."""
    moves = [MOVEjab, MOVEcross, MOVEhook, MOVEuppercut, MOVEwrapup, MOVEfeint, MOVEtaunt, MOVEbob,
             MOVEfootwork, MOVEhandsup, MOVEprotect]

    def on_intent(self, intent_data, session):
        session = self.update_with_intent(intent_data, session)
        speech = phrase_builder.build(session)
        reprompt = self.reprompt(session)
        should_end = self.game_over(session)
        response = build_speechlet_response("Boxing",
                                            speech,
                                            reprompt_text=reprompt,
                                            should_end_session=should_end,
                                            plain_text=False)
        return build_response(session, response)

    def update_with_intent(self, intent_data, session):
        player_move = self.player_move(intent_data)
        session[PLAYERMOVE] = player_move
        session = match.update(session)
        return session

    def player_move(self, intent_data):
        move_name = intent_data.get("name")
        assert move_name in BoxingSkillAdaptor.moves
        return move_name

    def reprompt(self, session):
        return phrase_builder.reprompt(session)

    def game_over(self, session):
        return session[ANNOUNCE] == ANNOUNCEGameOver
