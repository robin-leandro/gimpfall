#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT, PF_FILE, pdb, gimp

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import arrange_cards_into_sheets, PPI


default_cardback = 'C:\\Users\\Robin\\Documents\\repos\\gimpfall\\plugins\\load_cardback\\ElementalOmnath.png'

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19, cardback_path=default_cardback):
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
	arrange_cards_into_sheets(card_paths, card_names, sheet_width_px, sheet_height_px, cardback_path)


register(		
	"load_decklist",
	"Load Decklist From Scryfall",
	"Loads a list of cards from Scyfall, arranging them into sheets with the specified dimensions at 300ppi.",
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