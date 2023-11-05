#!/usr/bin/python
#TODO fix import
from gimpfu import *#register, main, PF_FLOAT, PF_FILE

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required fo modules to work
sys.path.append(module_path)
from gimp_utils.gimp import arrange_cards_into_sheets, import_into_gimp, page_setup, PPI

default_cardback = plugin_path.rpartition('\\')[0]+'\\Tolaria_Cardback.png'

def load_cardback(file_name=default_cardback, sheet_width_in=19, sheet_height_in=13):
	sheet_width_px = sheet_width_in*PPI
	sheet_height_px = sheet_height_in*PPI
	_, _, cards_per_sheet, _, _ = page_setup(sheet_width_px, sheet_height_px)

	image = import_into_gimp(file_name, False)
	cardbacks = []
	card_names = []
	for i in range(cards_per_sheet):
		cardbacks.append(image)
		card_names.append('cardback')
	arrange_cards_into_sheets(cardbacks, card_names, sheet_width_px, sheet_height_px)
	gimp.delete(image)
	
	
register(		
	"load_cardback",
	"Load Cardback From File",
	"Fill a sheet with the given dimensions with a provided image, to be used as a cardback",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Cardback",
	"",
	[
		(PF_FILE, "file_name", "The name of the image to load as a card back", default_cardback),
		(PF_FLOAT, "sheet_width_in", "width in inches", 19),
		(PF_FLOAT, "sheet_height_in", "height in inches", 13)
	],
	[],
	load_cardback)

main()				 