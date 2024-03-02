#!/usr/bin/python
from gimpfu import register, main, PF_FLOAT, PF_STRING
import sys, os
plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instance its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import crop_scale, cm_to_px


def crop_and_scale_card(image, _, width_cm=744, height_cm=1038, mode='crop'):
	crop_scale(image, cm_to_px(width_cm), cm_to_px(height_cm), mode)
	#card_setup(image, target_width, target_height)
	#crop_inches_proportionally(0.125, image, target_width, target_height)


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
		(PF_FLOAT, "width_cm", "width in centimeters", 6.3),
		(PF_FLOAT, "height_cm", "height in centimeters", 8.8),
		(PF_STRING, "mode", "mode (crop, fill, scale)", 'crop')
	],
	[],
	crop_and_scale_card)

main()				 