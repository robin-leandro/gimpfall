#!/usr/bin/python
from gimpfu import register, main, PF_STRING
import sys

#this append to the syspath really really sucks but since these scripts run from gimp and this isnt the cwd on runtime there is little i can do i think
sys.path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import crop_scale, import_into_gimp, arrange_cards_into_sheet

def load_decklist(decklist):
	card_names = decklist.split(',')
	card_images = []
	for card in card_names:
		image = import_into_gimp(query_scryfall(card), False)
		crop_scale(image)
		card_images.append(image)
	arrange_cards_into_sheet(card_images, card_names)
	#TODO arrange images into one sheet
	#TODO CARDBACKS? CARDBACKS? CARDBACKS? CARDBACKS? CARDBACKS?


register(		
	"load_decklist",
	"Load Decklist",
	"Loads a list of cards from Scyfall, arranging them into a into a 13x19in sheet",
	#TODO parameterize sheet size
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Decklist",
	"",
	[
		(PF_STRING, "decklist", "comma-separated list of cards to load", 'mudbutton torchrunner,goblin grenade')
	],
	[],
	load_decklist)

main()				 