#!/usr/bin/python
from gimpfu import register, main, PF_STRING, PF_FLOAT, PF_DIRNAME, PF_FILE

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import arrange_cards_into_sheets, PPI


def load_deck_from_folder(path, sheet_width_in=13, sheet_height_in=19, cardback_path=''):
	os.chdir(path)
	path_contents = os.listdir(path)
	image_paths = map(lambda p: path+'\\'+p, path_contents)
	image_names = map(lambda p: p.rpartition('.')[0], path_contents)
	if cardback_path == '':
		cardback_path = None

	arrange_cards_into_sheets(image_paths, image_names, sheet_width_in*PPI, sheet_height_in*PPI, cardback_path)
		


register(		
	"load_deck_from_folder",
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
		(PF_FILE, "cardback_path", "path to the cardback to use", '')
	],
	[],
	load_deck_from_folder)

main()