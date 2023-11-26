#!/usr/bin/python
from gimpfu import gimp, register, main, PF_STRING, PF_FLOAT, PF_FILE, PF_BOOL

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import arrange_cards_into_sheets, PPI, CARD_WIDTH, CARD_HEIGHT

default_cardback = os.path.join(module_path, 'Tolaria_Cardback.png')

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19, cardback_path=default_cardback, greyscale=False):
	sheet_width_px = sheet_width_in*PPI
	sheet_height_px = sheet_height_in*PPI

	decklist = decklist.split('\n')
	card_paths = []
	card_names = []
	gimp.progress_init('Getting images from Scryfall...')
	for count, line in enumerate(decklist):
		if line == '' or line.isspace():
			continue
		amount, _, card = line.partition(' ')
		path = query_scryfall(card)
		for i in range(int(amount)):
			card_paths.append(path)
			card_names.append(card)
		gimp.progress_update(float(count)/float(len(decklist)))
		
	if cardback_path == '':
		cardback_path = None

	arrange_cards_into_sheets(card_paths, card_names, sheet_width_px, sheet_height_px, cardback_path, 800, 1100, greyscale)
	#TODO different plugin that loads list of cards from a local directory instead of scryfall
	#TODO handle errors man, would be great to gracefully exit by deleting all leftover images
	#TODO open-ended "paper roll" mode
	#TODO sick ass progress bar (rescue from the other branch)
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
		(PF_FILE, "cardback_path", "path to the cardback to use", default_cardback),
		(PF_BOOL, "greyscale", "Greyscale images?", False)
	],
	[],
	load_decklist)

main()