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
        response =  build_speechlet_response("Boxing", speech, None, True, plain_text=False)
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

# TODO
# move the match test from phrase builder to test boxing skill adaptor
# add randomized reprompt data "why aren't they doing anything?" what will the coach call out next? george looks to the cor


# response = BoxingSkillAdaptor().on_intent({'name':'jab'}, {OPPONENTMOVE:MOVEuppercut})
# session = response['sessionAttributes']
# response = BoxingSkillAdaptor().on_intent({'name':'jab'}, session)
# print response
# print response['sessionAttributes']
