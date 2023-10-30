#!/usr/bin/python
from gimpfu import *
import sys
#this append to the syspath really really sucks but since these scripts run from gimp there is little i can do i think
sys.path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_lib.query_scryfall import query_scryfall

def search_scryfall(query='sol ring'):
	image_path = query_scryfall(query)
	image = pdb.file_png_load(image_path, image_path)
	pdb.gimp_display_new(image)
	return image
	#TODO delete temp file


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