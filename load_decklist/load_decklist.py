#!/usr/bin/python
from gimpfu import *
import sys

#this append to the syspath really really sucks but since these scripts run from gimp there is little i can do i think
sys.path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from scryfall_lib.query_scryfall import query_scryfall

def load_decklist(decklist):
	cards = decklist.split(',')
	card_images = []
	for card in cards:
		path = query_scryfall(card)
		card_images.append(pdb.file_png_load(path, path))
	
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