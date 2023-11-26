#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT, PF_INT, PF_DIRNAME, PF_FILE, PF_BOOL, pdb

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import arrange_cards_into_sheets, PPI, CARD_WIDTH, CARD_HEIGHT


def load_decklist_local(path, sheet_width_in=13, sheet_height_in=19, cardback_path='', card_margin_x_in=0, card_margin_y_in=0, greyscale=False):
	os.chdir(path)
	path_contents = os.listdir(path)
	image_paths = map(lambda p: os.path.join(path, p) , path_contents)
	image_names = map(lambda p: p.rpartition('.')[0], path_contents)
	if cardback_path == '':
		cardback_path = None

	arrange_cards_into_sheets(image_paths, image_names, sheet_width_in*PPI, sheet_height_in*PPI, cardback_path, CARD_WIDTH+int(PPI*card_margin_x_in/2), CARD_HEIGHT+int(PPI*card_margin_y_in/2), greyscale=False)
		


register(		
	"load_decklist_local",
	"Load Files in a Folder as a Deck",
	"Loads all the images in a folder, arranging them into sheets with the specified dimensions at 300ppi.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Deck From Folder",
	"",
	[
		(PF_DIRNAME, "directory", 'path to the folder to use', ''),
		(PF_FLOAT, "sheet_width_in", "width in inches", 19),
		(PF_FLOAT, "sheet_height_in", "height in inches", 13),
		(PF_FILE, "cardback_path", "path to the cardback to use", ''),
		(PF_FLOAT, "card_margin_x_in", "amount of whitescape to leave in between cards. If using a cardback, it will be scaled to the card size + both margins.", 0),
		(PF_FLOAT, "card_margin_y_in", "amount of whitescape to leave in between cards. If using a cardback, it will be scaled to the card size + both margins.", 0),
		(PF_BOOL, "greyscale", "Greyscale images?", False)
	],
	[],
	load_decklist_local)

main()