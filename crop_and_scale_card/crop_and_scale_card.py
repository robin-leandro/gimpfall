#!/usr/bin/python
from gimpfu import *

def crop_and_scale_card(image, _, target_width=744, target_height=1038):
	initial_width = image.width
	initial_height = image.height

	if (initial_width < target_width or initial_height < target_height):
		pdb.gimp_message('Image is already smaller than targets')
		return

	temp_height = initial_height*target_width / initial_width
	temp_width = initial_width*target_height / initial_height

	# maybe i need to normolize by dividing by target_x ?
	if ( temp_width-target_width > temp_height-target_height ): 
		temp_height = target_height
	else:
		temp_width = target_width

	pdb.gimp_image_scale(image, temp_width, temp_height)
	pdb['gimp-image-crop'](image, target_width, target_height, (temp_width-target_width)/2, (temp_height-target_height)/2)

register(		
	"crop_and_scale_card",
	"Crop & Scale",
	"Scale as close to targets as possible while maintaining aspect ratio, then crop to target offsetting on center. Assumes image is close enough in aspect ratio to an actual card where no important info will be cropped.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Image>/gimpfall/Crop Scale",
	"RGB*, GRAY*",
	[
		(PF_INT, "width", "width", 744),
		(PF_INT, "height", "height", 1038)
	],
	[],
	crop_and_scale_card)

main()				 