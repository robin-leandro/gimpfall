from gimpfu import *
import math
CARD_WIDTH_PX = 744
CARD_HEIGHT_PX = 1038
ALIGNMENT_ERROR_PADDING_PX = 45 # about 3/20in or 3.81mm
CARD_WIDTH_WITH_ALIGNMENT_PADDING_PX = CARD_WIDTH_PX + (ALIGNMENT_ERROR_PADDING_PX * 2)
CARD_HEIGHT_WITH_ALIGNMENT_PADDING_PX = CARD_HEIGHT_PX + (ALIGNMENT_ERROR_PADDING_PX * 2)
PPI = 300

GIMP_FILETYPE_HANDLERS = {
	'png': 'file-png-load',
	'jpg': 'file-jpeg-load',
	'jpeg': 'file-jpeg-load'
}

def import_into_gimp(path, display=True):
	image = pdb[GIMP_FILETYPE_HANDLERS[path.rpartition('.')[2]]](path, path)

	if display:
		pdb.gimp_display_new(image)
	return image

def crop_scale_fill(image, target_width=CARD_WIDTH_PX, target_height=CARD_HEIGHT_PX):
	initial_width = image.width
	initial_height = image.height


	# resulting width from scaling the height to target and retaining aspect ratio
	tentative_width = target_width * initial_height / target_height

	# resulting height from scaling the height to target and retaining aspect ratio
	tentative_height = target_height * initial_width / target_width
	
	if (tentative_width > target_width and tentative_height > tentative_height) or (tentative_width < target_width and tentative_height < tentative_height):
		# this _should_ be impossible
		raise NameError('the crop-scale-fill math is not mathin')

	if tentative_height == target_height and tentative_width == target_width:
		# image started out with the correct aspect ratio
		# just scale and job's done
		pdb.gimp_image_scale(image, target_width, target_height)
		return image

	# we either need to upscale or downscale the image
	# we'll include the equal area edge-case in the upscale path
	rectangle_area = lambda l, w: l*w
	upscale = rectangle_area(target_height, target_width) >= rectangle_area(initial_height, initial_width)
	
	if 


	if upscale:
		
		return image
	
	# if the image was downscaled, we need to crop

	#pdb.gimp_image_crop(xxx,xxx,xxx,xx,xx,xx,xx,x)
	return image
	



def page_setup(sheet_width_px, sheet_height_px):
	# according to docs math.floor is supposed to return int
	# but its not doing that so ugly casts it is ig
	cards_per_row = int(math.floor(sheet_width_px / CARD_WIDTH_PX))
	cards_per_column = int(math.floor(sheet_height_px / CARD_HEIGHT_PX))
	cards_per_sheet = cards_per_row * cards_per_column
	horizontal_margin = int((sheet_width_px - cards_per_row * CARD_WIDTH_PX) / 2)
	vertical_margin = int((sheet_height_px - cards_per_column * CARD_HEIGHT_PX) / 2)
	return cards_per_row, cards_per_column, cards_per_sheet, horizontal_margin, vertical_margin

def arrange_cards_into_sheets(card_paths, card_names, sheet_width_px, sheet_height_px, cardback_path = None, include_alignment_margin=False):
	if CARD_WIDTH_PX > sheet_width_px or CARD_HEIGHT_PX > sheet_height_px:
		raise NameError('sheet with provided dimensions cannot fit any cards')

	gimp.progress_init('Importing images into Gimp...')
	paths_dict = {}
	def image_from_path(args):
		count, p  = args
		gimp.progress_init('Importing images into Gimp...')
		gimp.progress_update(float(count)/float(len(card_paths)))
		if p in paths_dict:
			return paths_dict[p]
		image = crop_scale_fill(import_into_gimp(p, False))
		# surely theres a more elegant way than just un/commenting this lol
		pdb.gimp_image_convert_grayscale(image)
		return paths_dict.setdefault(p, image)
	card_images = map(image_from_path, enumerate(card_paths))
	cards_per_row, _, cards_per_sheet, horizontal_margin, vertical_margin = page_setup(sheet_width_px, sheet_height_px)
	total_sheets = int(math.ceil(float(len(card_images))/float(cards_per_sheet)))

	#just a cheeky lil debugging message keep moving along folks
	#pdb.gimp_message("cards per row {cpr}\ncards per col {cpc}\ncards per sheet {cps}\ntotal sheets {tSheet}\nhorizontal margin {hm}\nvertical margin {vm}".format(cpr=cards_per_row,cpc = cards_per_column, cps =cards_per_sheet, tSheet = total_sheets, hm=horizontal_margin, vm=vertical_margin))

	cardbacks = []
	cardback_names = []
	if cardback_path is not None:
		cardback_image = crop_scale_fill(import_into_gimp(cardback_path, False))
		for i in range(cards_per_sheet):
			cardback_names.append('cardback')
			cardbacks.append(cardback_image) 

	gimp.progress_init('Generating sheet images...')
	for i in range(total_sheets):
		__arrange_cards_into_sheet(card_images[i*cards_per_sheet:(i+1)*cards_per_sheet], 
		card_names[i*cards_per_sheet:(i+1)*cards_per_sheet],
		sheet_width_px,
		sheet_height_px,
		cards_per_row,
		horizontal_margin,
		vertical_margin)
		gimp.progress_update(float(i*2)/float(total_sheets*2))
		if cardback_path is not None:
			__arrange_cards_into_sheet(cardbacks, 
				cardback_names,
				sheet_width_px,
				sheet_height_px,
				cards_per_row,
				horizontal_margin,
				vertical_margin)
		gimp.progress_update(float((i*2)+1)/float(total_sheets*2))
	
	cleanup_temp_images()

	

# assumes sheet is large enough to fit the passed cards
def __arrange_cards_into_sheet(card_images, card_names, sheet_width_px, sheet_height_px, cards_per_row, horizontal_margin, vertical_margin):
	image = pdb.gimp_image_new(sheet_width_px, sheet_height_px, RGB)
	for count, card_image in enumerate(card_images):
		card_layer = pdb.gimp_layer_new(image, sheet_width_px, sheet_height_px, RGB_IMAGE, 'card #{num}: {name}'.format(num = count+1, name = card_names[count]), 100, NORMAL_MODE)
		image.add_layer(card_layer, count)
		card_layer.resize(CARD_WIDTH_PX, CARD_HEIGHT_PX, 0, 0)
		card_layer.set_offsets(horizontal_margin + CARD_WIDTH_PX * (count % cards_per_row), vertical_margin + CARD_HEIGHT_PX*(count/cards_per_row))
		pdb.gimp_edit_copy(card_image.active_layer)
		selection = pdb.gimp_edit_paste(card_layer, True)
		pdb.gimp_floating_sel_anchor(selection)
	
	background_layer = pdb.gimp_layer_new(image, sheet_width_px, sheet_height_px, RGB_IMAGE, 'background', 100, NORMAL_MODE)
	image.add_layer(background_layer, len(image.layers))
	background_layer.fill(FILL_WHITE)
	pdb.gimp_display_new(image)
	
# deletes all images without an associated display
def cleanup_temp_images():
	__delete_images(gimp.image_list())
	
def __delete_images(images):
	for image in images:
		if pdb.gimp_image_is_valid(image):
			gimp.delete(image)