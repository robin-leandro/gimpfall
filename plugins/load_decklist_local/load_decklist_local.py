#!/usr/bin/python
from gimpfu import register, main, PF_DIRNAME

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instace its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import arrange_cards_into_sheets
from proxy_settings import get_default_settings, settings_map_to_gimp_tuple, ProxySettings


def load_decklist_local(path, *args):
	os.chdir(path)
	settings = ProxySettings(args)
	path_contents = os.listdir(path)
	image_paths = map(lambda p: os.path.join(path, p) , path_contents)
	image_names = map(lambda p: p.rpartition('.')[0], path_contents)
	arrange_cards_into_sheets(image_paths, image_names, settings)
		

default_settings = get_default_settings()
register(		
	"load_decklist_local",
	"Load Files in a Folder as a Deck",
	"Loads all the images in a folder, arranging them into sheets with the specified dimensions at 300ppi.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Load Deck From Folder",
	"",
	[((PF_DIRNAME, "directory", 'path to the folder to use', ''))]+settings_map_to_gimp_tuple(default_settings),
	[],
	load_decklist_local)

main()