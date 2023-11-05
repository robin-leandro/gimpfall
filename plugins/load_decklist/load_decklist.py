#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT
from sys import path
#this append to the syspath really really sucks but since these scripts run from gimp and this isnt the cwd on runtime there is little i can do i think
path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import crop_scale, import_into_gimp, arrange_cards_into_sheets

PPI = 300

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19):
	card_names = decklist.split('\n')
	card_images = []
	for card in card_names:
		image = import_into_gimp(query_scryfall(card), False)
		crop_scale(image)
		card_images.append(image)
	arrange_cards_into_sheets(card_images, card_names, sheet_width_in*PPI, sheet_height_in*PPI)
	#TODO locally cache downloaded cards
	#TODO different plugin that loads list of cards from a local directory instead of scryfall
	#TODO open-ended "roll" mode?
	#TODO CARDBACKS? CARDBACKS? CARDBACKS? CARDBACKS? CARDBACKS?


register(		
	"load_decklist",
	"Load Decklist",
	"Loads a list of cards from Scyfall, arranging them into a sheet with the specified dimensions at 300ppi.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Decklist",
	"",
	[
		(PF_STRING, "decklist", "newline-separated list of cards to load", 'mudbutton torchrunner\ngoblin grenade'),
		(PF_FLOAT, "sheet_width_in", "width in inches", 19),
		(PF_FLOAT, "sheet_height_in", "height in inches", 13)
	],
	[],
	load_decklist)

main()				 