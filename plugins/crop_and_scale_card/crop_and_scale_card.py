#!/usr/bin/python
from gimpfu import register, main, PF_INT
#this append to the syspath really really sucks but since these scripts run from gimp there is little i can do i think
import sys
sys.path.append('C:\Users\Robin\Documents\\repos\gimpfall')
from gimp_utils.gimp import crop_scale


def crop_and_scale_card(image, _, target_width=744, target_height=1038):
	#pdb.gimp_message('hello world')
	crop_scale(image, target_width, target_height)

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