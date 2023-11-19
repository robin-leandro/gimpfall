#!/usr/bin/python
from gimpfu import register, main, PF_INT

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = plugin_path.rpartition('gimpfall')[0]+'gimpfall'
# not ideal to append to syspath like this
# but since gimp runs its own python instance its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import crop_scale_fill


def crop_scale_fill_image(image, _, target_width=744, target_height=1038):
	crop_scale_fill(image, target_width, target_height)

register(		
	"crop_scale_fill_image",
	"Crop, Scale & Fill",
	"Scale as close to targets as possible while maintaining aspect ratio, then if downscaled crop the excess or if upscaled fill the required space with background color.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Image>/gimpfall/Crop & Scale",
	"RGB*, GRAY*",
	[
		(PF_INT, "width", "width", 744),
		(PF_INT, "height", "height", 1038)
	],
	[],
	crop_scale_fill_image)

main()				 