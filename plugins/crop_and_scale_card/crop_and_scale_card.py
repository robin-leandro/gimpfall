#!/usr/bin/python
from gimpfu import register, main, PF_INT

import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instance its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import crop_scale


def crop_and_scale_card(image, _, target_width=744, target_height=1038):
	crop_scale(image, target_width, target_height)

register(		
	"crop_and_scale_card",
	"Crop & Scale",
	"Scale as close to targets as possible while maintaining aspect ratio, then crop to target offsetting on center. Assumes image is close enough in aspect ratio to an actual card where no important info will be cropped.",
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
	crop_and_scale_card)

main()				 