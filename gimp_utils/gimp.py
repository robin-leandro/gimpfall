
from gimpfu import pdb

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