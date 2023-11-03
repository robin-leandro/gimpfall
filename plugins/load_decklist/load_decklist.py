#!/usr/bin/python
from gimpfu import register, main, PF_STRING
import sys

#this append to the syspath really really sucks but since these scripts run from gimp and this isnt the cwd on runtime there is little i can do i think
sys.path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_utils.query_scryfall import query_scryfall
from gimp_utils.gimp import crop_scale, import_into_gimp

def load_decklist(decklist):
	cards = decklist.split(',')
	card_images = []
	for card in cards:
		card_images.append(import_into_gimp(query_scryfall(card), False))
	for image in card_images:
		crop_scale(image)
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
		(PF_STRING, "decklist", "comma-separated lit of cards to load", 'mudbutton torchrunner,goblin grenade')
	],
	[],
	load_decklist)

main()				 