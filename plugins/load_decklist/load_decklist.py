#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import crop_scale, import_into_gimp, arrange_cards_into_sheets, delete_images, PPI

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19):
	card_names = decklist.split('\n')
	card_images = []
	for card in card_names:
		image = import_into_gimp(query_scryfall(card), False)
		crop_scale(image)
		card_images.append(image)
	arrange_cards_into_sheets(card_images, card_names, sheet_width_in*PPI, sheet_height_in*PPI)
	delete_images(card_images)
	#TODO locally cache downloaded cards
	#TODO different plugin that loads list of cards from a local directory instead of scryfall
	#TODO open-ended "roll" mode


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
		(PF_STRING, "decklist", "newline-separated list of cards to load", 'mudbutton torchrunner\ngoblin grenade'),
		(PF_FLOAT, "sheet_width_in", "width in inches", 19),
		(PF_FLOAT, "sheet_height_in", "height in inches", 13)
	],
	[],
	load_decklist)

main()				 