#!/usr/bin/python
from gimpfu import register, main, PF_STRING

#this append to the syspath really really sucks but since these scripts run from gimp there is little i can do i think
from sys import path
#this append to the syspath really really sucks but since these scripts run from gimp and this isnt the cwd on runtime there is little i can do i think
path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import import_into_gimp

def search_scryfall(query='sol ring'):
	import_into_gimp(query_scryfall(query))

register(
	"search_scryfall",
	"Fetch",
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