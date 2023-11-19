#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT, PF_FILE

import sys, os, math
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import arrange_cards_into_sheets, page_setup, PPI


default_cardback = 'C:\\Users\\Robin\\Documents\\repos\\gimpfall\\plugins\\load_cardback\\ElementalOmnath.png'

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19, cardback_path=default_cardback):
	sheet_width_px = sheet_width_in*PPI
	sheet_height_px = sheet_height_in*PPI

	decklist = decklist.split('\n')
	card_paths = []
	card_names = []
	for line in decklist:
		amount, _, card = line.partition(' ')
		path = query_scryfall(card)
		for _ in range(int(amount)):
			card_paths.append(path)
			card_names.append(card)
	
	# _, _, cards_per_sheet, _, _ = page_setup(sheet_width_px, sheet_height_px)
	# total_sheets = int(math.ceil(float(len(card_paths)) / float(cards_per_sheet)))

	# new_card_paths = []
	# new_card_names = []
	# for i in range(total_sheets):
	# 	new_card_paths.extend(card_paths[i*cards_per_sheet:(i+1)*cards_per_sheet])
	# 	new_card_names.extend(card_names[i*cards_per_sheet:(i+1)*cards_per_sheet])
	# 	for i in range(cards_per_sheet):
	# 		new_card_paths.append(cardback_path)
	# 		new_card_names.append('cardback')
		
	if cardback_path == '':
		cardback_path = None
	arrange_cards_into_sheets(card_paths, card_names, sheet_width_px, sheet_height_px, cardback_path)
	#TODO different plugin that loads list of cards from a local directory instead of scryfall
	#TODO handle errors man, would be great to gracefully exit by deleting all leftover images
	#TODO open-ended "paper roll" mode
	#TODO sick ass progress bar
	#TODO handle double sided cards (how tho lmao)
		# there should be a setting to choose between printing 2 cards or one double-sided cardgit add 
	#TODO clean up the input, lets not die because of an empty line yeah?


register(		
	"load_decklist",
	"Load Decklist From Scryfall",
	"Loads a list of cards from Scyfall, arranging them into a sheet with the specified dimensions at 300ppi.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Decklist From Scryfall",
	"",
	[
		(PF_STRING, "decklist", "newline-separated list of cards to load of the form: \"(amount) (exact card name)\"", '1 mudbutton torchrunner\n1 goblin grenade'),
		(PF_FLOAT, "sheet_width_in", "width in inches", 19),
		(PF_FLOAT, "sheet_height_in", "height in inches", 13),
		(PF_FILE, "cardback_path", "path to the cardback to use", '')
	],
	[],
	load_decklist)

main()