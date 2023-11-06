#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import arrange_cards_into_sheets, PPI

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19):
	decklist = decklist.split('\n')
	card_paths = []
	card_names = []
	for line in decklist:
		amount, _, card = line.partition(' ')
		path = query_scryfall(card)
		for _ in range(int(amount)):
			card_paths.append(path)
			card_names.append(card)
	arrange_cards_into_sheets(card_paths, card_names, sheet_width_in*PPI, sheet_height_in*PPI)
	#TODO different plugin that loads list of cards from a local directory instead of scryfall
	#TODO open-ended "paper roll" mode
	#TODO sick ass progress bar


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
		(PF_FLOAT, "sheet_height_in", "height in inches", 13)
	],
	[],
	load_decklist)

main()