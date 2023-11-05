from gimpfu import *
import math
CARD_WIDTH = 744
CARD_HEIGHT = 1038
PPI = 300

def import_into_gimp(path, display=True):
	image = pdb.file_png_load(path, path)
	if display:
		pdb.gimp_display_new(image)
	return image


def crop_scale(image, target_width=CARD_WIDTH, target_height=CARD_HEIGHT):
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

def page_setup(sheet_width_px, sheet_height_px):
	# according to docs math.floor is supposed to return int
	# but its not doing that so ugly casts it is ig
	cards_per_row = int(math.floor(sheet_width_px / CARD_WIDTH))
	cards_per_column = int(math.floor(sheet_height_px / CARD_HEIGHT))
	cards_per_sheet = cards_per_row * cards_per_column
	horizontal_margin = int((sheet_width_px - cards_per_row * CARD_WIDTH) / 2)
	vertical_margin = int((sheet_height_px - cards_per_column * CARD_HEIGHT) / 2)
	return cards_per_row, cards_per_column, cards_per_sheet, horizontal_margin, vertical_margin

def arrange_cards_into_sheets(card_images, card_names, sheet_width_px, sheet_height_px):
	if CARD_WIDTH > sheet_width_px or CARD_HEIGHT > sheet_height_px:
		raise NameError('sheet with provided dimensions cannot fit any cards')

	cards_per_row, _, cards_per_sheet, horizontal_margin, vertical_margin = page_setup(sheet_width_px, sheet_height_px)
	total_sheets = int(math.ceil(float(len(card_images))/float(cards_per_sheet)))
	#just a cheeky lil debugging message keep moving along folks
	#pdb.gimp_message("cards per row {cpr}\ncards per col {cpc}\ncards per sheet {cps}\ntotal sheets {tSheet}\nhorizontal margin {hm}\nvertical margin {vm}".format(cpr=cards_per_row,cpc = cards_per_column, cps =cards_per_sheet, tSheet = total_sheets, hm=horizontal_margin, vm=vertical_margin))

	for i in range(total_sheets):
		arrange_cards_into_sheet(card_images[i*cards_per_sheet:(i+1)*cards_per_sheet], 
		card_names[i*cards_per_sheet:(i+1)*cards_per_sheet],
		sheet_width_px,
		sheet_height_px,
		cards_per_row,
		horizontal_margin,
		vertical_margin)

# assumes sheet is large enough to fit the passed cards
def arrange_cards_into_sheet(card_images, card_names, sheet_width_px, sheet_height_px, cards_per_row, horizontal_margin, vertical_margin):
	image = pdb.gimp_image_new(sheet_width_px, sheet_height_px, RGB)
	for count, card_image in enumerate(card_images):
		card_layer = pdb.gimp_layer_new(image, sheet_width_px, sheet_height_px, RGB_IMAGE, 'card #{num}: {name}'.format(num = count+1, name = card_names[count]), 100, NORMAL_MODE)
		image.add_layer(card_layer, count)
		card_layer.resize(CARD_WIDTH, CARD_HEIGHT, 0, 0)
		card_layer.set_offsets(horizontal_margin + CARD_WIDTH * (count % cards_per_row), vertical_margin + CARD_HEIGHT*(count/cards_per_row))
		pdb.gimp_edit_copy(card_image.active_layer)
		selection = pdb.gimp_edit_paste(card_layer, True)
		pdb.gimp_floating_sel_anchor(selection)
	
	background_layer = pdb.gimp_layer_new(image, sheet_width_px, sheet_height_px, RGB_IMAGE, 'background', 100, NORMAL_MODE)
	image.add_layer(background_layer, len(image.layers))
	background_layer.fill(FILL_WHITE)
	pdb.gimp_display_new(image)
	
# handles copies of the same image, blindly deleting them would throw GIMP errors
def delete_images(images):
	for image in images:
		if pdb.gimp_image_is_valid(image):
			gimp.delete(image)