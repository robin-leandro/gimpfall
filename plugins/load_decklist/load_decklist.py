#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT
from sys import path
#this append to the syspath really really sucks but since these scripts run from gimp and this isnt the cwd on runtime there is little i can do i think
path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import CARD_WIDTH, CARD_HEIGHT, crop_scale, import_into_gimp, arrange_cards_into_sheet

PPI = 300

def load_decklist(decklist, sheet_width_in=13, sheet_height_in=19):
	sheet_width_px = sheet_width_in*PPI
	sheet_height_px = sheet_height_in*PPI
	if CARD_WIDTH > sheet_width_px or CARD_HEIGHT > sheet_height_px:
		raise NameError('sheet with provided dimensions cannot fit any cards')

	card_names = decklist.split('\n')
	card_images = []
	for card in card_names:
		image = import_into_gimp(query_scryfall(card), False)
		crop_scale(image)
		card_images.append(image)
	arrange_cards_into_sheet(card_images, card_names, sheet_width_px, sheet_height_px)
	#TODO more than one sheet?
	#TODO open-ended "roll" mode?s
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
		(PF_FLOAT, "width", "width in inches", 19),
		(PF_FLOAT, "height", "height in inches", 13)
	],
	[],
	load_decklist)

main()				 