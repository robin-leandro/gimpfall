from gimpfu import *
import math
from proxy_settings import ProxySettings

PPI = 300
def in_to_px(inc):
	return int(inc*PPI)

def cm_to_px(cm):
	return int(cm/2.54*PPI)

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

def card_setup(image, final_width, final_height, grayscale = False):
	unround_corners(image)
	crop_scale(image, final_width, final_height, 'crop')
	add_border(image, final_width, final_height, 'white')
	if grayscale:
		pdb.gimp_image_convert_grayscale(image)
	return image
	
def unround_corners(image):
	corner_layer = pdb.gimp_layer_new(image, image.width, image.height, RGB_IMAGE, 'remove corners', 100, NORMAL_MODE)
	image.add_layer(corner_layer, 2)
	pdb.gimp_palette_set_background('black')
	corner_layer.fill(BACKGROUND_FILL)
	pdb.gimp_image_flatten(image)
	return image

def crop_scale(image, target_width, target_height, strategy='fill'):
	initial_width = image.width
	initial_height = image.height

	temp_width = target_width
	temp_height = target_height
	if strategy=='fill' and initial_width * target_height > target_width * initial_height:
		temp_height = (target_width * initial_height) / initial_width
	else:
		temp_width = (target_height * initial_width) / initial_height

	pdb.gimp_image_scale(image, temp_width, temp_height)

	if strategy=='fill':
		add_border(image, target_width, target_height, 'black')
		return image

	if strategy=='crop':
		#TODO: fix
		#pdb.gimp_message('we croppin a {w}x{h} to {w2}x{h2}'.format(w=temp_width, h=temp_height, w2=target_width, h2=target_height))
		#pdb.gimp_image_crop(image, target_width, target_height, (abs(temp_width-target_width))/2, (abs(temp_height-target_height))/2)
		return image

	raise NameError('no strategy {s}'.format(s=strategy))

def add_border(image, new_width, new_height, color):
	pdb.gimp_image_resize(image, new_width, new_height, (new_width-image.width)/2, (new_height-image.height)/2)
	card_layer = pdb.gimp_layer_new(image, new_width, new_height, RGB_IMAGE, 'border', 100, NORMAL_MODE)
	image.add_layer(card_layer, 2)
	pdb.gimp_palette_set_background(color)
	card_layer.fill(BACKGROUND_FILL)
	pdb.gimp_image_flatten(image)
	return image

def page_setup(sheet_width_px, sheet_height_px, card_width, card_height):
	# according to docs math.floor is supposed to return int
	# but its not doing that so ugly casts it is ig
	cards_per_row = int(math.floor(sheet_width_px / card_width))
	cards_per_column = int(math.floor(sheet_height_px / card_height))
	cards_per_sheet = cards_per_row * cards_per_column
	horizontal_margin = int((sheet_width_px - cards_per_row * card_width) / 2)
	vertical_margin = int((sheet_height_px - cards_per_column * card_height) / 2)
	return cards_per_row, cards_per_column, cards_per_sheet, horizontal_margin, vertical_margin

def arrange_cards_into_sheets(card_paths, card_names, proxy_settings):
	sheet_width_in, sheet_height_in, cardback_path, card_width_cm, card_height_cm, greyscale, fix_eighth_in_margin = proxy_settings.get_all()
	sheet_width_px, sheet_height_px = in_to_px(sheet_width_in), in_to_px(sheet_height_in)
	card_width, card_height = cm_to_px(card_width_cm), cm_to_px(card_height_cm)

	if card_width > sheet_width_px or card_height > sheet_height_px:
		raise NameError('sheet with provided dimensions cannot fit any cards')

	# dont wanna be double importing duplicates
	paths_dict = {}
	gimp.progress_init('Importing images into Gimp...')
	def image_from_path(args):
		count, p = args
		gimp.progress_init('Importing images into Gimp...')
		gimp.progress_update(float(count)/float(len(card_paths)))
		if p in paths_dict:
			return paths_dict[p]
		return paths_dict.setdefault(p, card_setup(import_into_gimp(p, False), card_width, card_height, greyscale))
	card_images = map(image_from_path, enumerate(card_paths))

	cards_per_row, _, cards_per_sheet, horizontal_margin, vertical_margin = page_setup(sheet_width_px, sheet_height_px, card_width, card_height)
	total_sheets = int(math.ceil(float(len(card_images))/float(cards_per_sheet)))

	#just a cheeky lil debugging message, keep moving along folks
	#pdb.gimp_message("cards per row {cpr}\ncards per col {cpc}\ncards per sheet {cps}\ntotal sheets {tSheet}\nhorizontal margin {hm}\nvertical margin {vm}".format(cpr=cards_per_row,cpc = cards_per_column, cps =cards_per_sheet, tSheet = total_sheets, hm=horizontal_margin, vm=vertical_margin))

	cardbacks = []
	cardback_names = []
	if cardback_path is '':
		cardback_path = None
	if cardback_path is not None:
		print('\n\n\n\n\nAAAAAAAAAAAAAAAAAAAA\n\n\n\n')
		cardback_image = crop_scale(import_into_gimp(cardback_path, False), card_width, card_height)
		for i in range(cards_per_sheet):
			cardback_names.append('cardback')
			cardbacks.append(cardback_image) 

	sheets_and_cardbacks = total_sheets if cardback_path is None else total_sheets*2
	for i in range(total_sheets):
		gimp.progress_init('Generating proxy sheet {n} of {ts}'.format(n=i+1, ts=sheets_and_cardbacks))
		gimp.progress_update(float(i)/float(sheets_and_cardbacks))
		__arrange_cards_into_sheet(card_images[i*cards_per_sheet:(i+1)*cards_per_sheet], 
		card_names[i*cards_per_sheet:(i+1)*cards_per_sheet],
		sheet_width_px,
		sheet_height_px,
		cards_per_row,
		horizontal_margin,
		vertical_margin,
		card_width, 
		card_height)
		if cardback_path is not None:
			__arrange_cards_into_sheet(cardbacks, 
				cardback_names,
				sheet_width_px,
				sheet_height_px,
				cards_per_row,
				horizontal_margin,
				vertical_margin,
				card_width, 
				card_height)
			gimp.progress_update(float(i+1)/float(sheets_and_cardbacks))

	cleanup_temp_images()

# assumes sheet is large enough to fit the passed cards
def __arrange_cards_into_sheet(card_images, card_names, sheet_width_px, sheet_height_px, cards_per_row, horizontal_margin, vertical_margin, card_width, card_height):
	image = pdb.gimp_image_new(sheet_width_px, sheet_height_px, RGB)
	for count, card_image in enumerate(card_images):
		card_layer = pdb.gimp_layer_new(image, sheet_width_px, sheet_height_px, RGB_IMAGE, 'card #{num}: {name}'.format(num = count+1, name = card_names[count]), 100, NORMAL_MODE)
		image.add_layer(card_layer, count)
		card_layer.resize(card_width, card_height, 0, 0)
		card_layer.set_offsets(horizontal_margin + card_width * (count % cards_per_row), vertical_margin + card_height*(count/cards_per_row))
		pdb.gimp_edit_copy(card_image.active_layer)
		selection = pdb.gimp_edit_paste(card_layer, True)
		pdb.gimp_floating_sel_anchor(selection)
		pdb.gimp_progress_pulse()
	
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