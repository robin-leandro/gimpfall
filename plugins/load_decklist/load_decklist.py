#!/usr/bin/python
from gimpfu import gimp, register, main, PF_STRING

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import arrange_cards_into_sheets
from proxy_settings import get_default_settings, settings_map_to_gimp_tuple, ProxySettings

default_cardback = os.path.join(module_path, 'Tolaria_Cardback.png')

def load_decklist(decklist, *args):
	settings  = ProxySettings(args)
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
	
	cardback_path = settings.get('cardback_path')
	if cardback_path == '':
		cardback_path = None

	arrange_cards_into_sheets(card_paths, card_names, proxy_settings=settings)


default_settings = get_default_settings()
register(		
	"load_decklist",
	"Load Decklist From Scryfall",
	"Loads a list of cards from Scyfall, arranging them into a sheet with the specified dimensions at 300ppi.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Decklist From Scryfall",
	"",
	[(PF_STRING, "decklist", "newline-separated list of cards to load of the form: \"(amount) (exact card name)\"", '1 mudbutton torchrunner\n1 goblin grenade'),]+settings_map_to_gimp_tuple(default_settings),
	[],
	load_decklist)

main()