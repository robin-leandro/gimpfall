#!/usr/bin/python
from gimpfu import register, main, pdb, PF_FILE, gimp
import os, sys

plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instance its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import cleanup_temp_images

default_filename = os.path.join(plugin_path.rpartition(os.path.join('/'))[0],'untitled.png')

def export_to_png(file_name=default_filename):
	cleanup_temp_images()
	images = gimp.image_list()
	for count, image in enumerate(images):
		name = file_name.replace('.png', '_{0}.png'.format(count))
		pdb.file_png_save_defaults(image, image.active_drawable, name, name)

register(		
	"export_to_png",
	"Export to PNG",
	"Export all open images as separate PNG files.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Export to PNG",
	"",
	[
		(PF_FILE, "file_name", "The name of the PNG files to generate, a counter will be appended", default_filename)
	],
	[],
	export_to_png)

main()				 