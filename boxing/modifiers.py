from boxing_strings import *

def modifier(player_move, opp_move):
	# 				cross,	jab,	hook,	uppercut,	feint,	taunt,	wrapup,	bobweave,	footwork,	handsup,	protect
	jab_mod = 		[0,		0,		0,		0,			-1,		0,		-1,		-1,			-2,			-1,			-2]
	cross_mod = 	[0,		0,		0,		0,			-1,		2,		0,		-2,			-2,			-2,			-1]
	hook_mod = 		[0,		0,		0,		0,			-1,		2,		0,		-2,			-2,			-2,			-1]
	uppercut_mod =  [2,		1,		1,		0,			-1,		2,		0,		-1,			-2,			-2,			-2]
	wrapup_mod = 	[0,		0,		0,		0,			0,		0,		0,		-1,			-1,			1,			1]
	feint_mod = 	[0,		0,		0,		0,			0,		0,		0,		0,			0,			0,			0]
	taunt_mod = 	[0,		0,		0,		0,			0,		0,		0,		0,			0,			0,			0]
	bobweave_mod = 	[0,		0,		0,		0,			0,		0,		0,		0,			0,			0,			0]
	footwork_mod = 	[0,		0,		0,		0,			0,		0,		0,		0,			0,			0,			0]
	handsup_mod = 	[0,		0,		0,		0,			0,		0,		0,		0,			0,			0,			0]
	protect_mod = 	[0,		0,		0,		0,			0,		0,		0,		0,			0,			0,			0]

	moves = [MOVEjab, MOVEcross, MOVEhook, MOVEuppercut, MOVEwrapup, MOVEfeint, MOVEtaunt, MOVEbob, MOVEfootwork, MOVEhandsup, MOVEprotect]
	mods = [jab_mod, cross_mod, hook_mod, uppercut_mod, wrapup_mod, feint_mod, taunt_mod, bobweave_mod, footwork_mod, handsup_mod, protect_mod]
	
	move_idx = {m : idx for idx, m in enumerate(moves)}
	mod_dict = {move:mod for move,mod in zip(moves,mods)}


	return mod_dict[player_move][move_idx[opp_move]]