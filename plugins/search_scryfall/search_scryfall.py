#!/usr/bin/python
from gimpfu import register, main, PF_STRING

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import import_into_gimp

def search_scryfall(query='sol ring'):
	import_into_gimp(query_scryfall(query))

register(
	"search_scryfall",
	"Fetch card From Scryfall",
	"Query Scryfall for a card name, download the png file and open it as a new image",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Search Scryfall",
	"",
	[
		(PF_STRING, "query", "query", 'sol ring')
	],
	[],
	search_scryfall)

main()