
from argparse import _VersionAction
from gimpfu import *

def import_into_gimp(path, display=True):
	image = pdb.file_png_load(path, path)
	if display:
		pdb.gimp_display_new(image)
	return image


def crop_scale(image, target_width=744, target_height=1038):
	initial_width = image.width
	initial_height = image.height

	if (initial_width < target_width or initial_height < target_height):
		pdb.gimp_message('Image is already smaller than targets')
		return

	temp_height = initial_height*target_width / initial_width
	temp_width = initial_width*target_height / initial_height

	#TODO make sure this algorithm is correct
	# maybe i need to normalize by dividing by target_x ?
	if ( temp_width-target_width > temp_height-target_height ): 
		temp_height = target_height
	else:
		temp_width = target_width

	pdb.gimp_image_scale(image, temp_width, temp_height)
	pdb['gimp-image-crop'](image, target_width, target_height, (temp_width-target_width)/2, (temp_height-target_height)/2)

def arrange_cards_into_sheet(card_images, card_names):
	#for now constant width&height, maybe ill parameterize this or not who knows (i wont :3)
	width = 5550
	height = 3750
	horizontal_margin = 171
	vertical_margin = 315
	cards_per_row = 7

	# assume all cards are same size lol
	card_width = card_images[0].width
	card_height = card_images[0].height

	image = pdb.gimp_image_new(width, height, RGB)
	for count, card_image in enumerate(card_images):
		card_layer = pdb.gimp_layer_new(image, width, height, RGB_IMAGE, 'card #{num}: {name}'.format(num = count+1, name = card_names[count]), 100, NORMAL_MODE)
		image.add_layer(card_layer, count)
		card_layer.resize(card_width, card_height, 0, 0)
		card_layer.set_offsets(horizontal_margin + card_width * (count % cards_per_row), vertical_margin + card_height*(count/cards_per_row))
		pdb.gimp_edit_copy(card_image.active_layer)
		selection = pdb.gimp_edit_paste(card_layer, True)
		pdb.gimp_floating_sel_anchor(selection)
		pdb.gimp_image_delete(card_image)


	background_layer = pdb.gimp_layer_new(image, width, height, RGB_IMAGE, 'background', 100, NORMAL_MODE)
	image.add_layer(background_layer, len(image.layers))
	background_layer.fill(FILL_WHITE)

	pdb.gimp_display_new(image)
	