#!/usr/bin/python
from gimpfu import register, main, pdb, PF_DIRNAME, PF_STRING
import os, sys

plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instance its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import cleanup_temp_images

default_filename = 'untitled.pdf'

def export_to_pdf(file_path, file_name=default_filename):
	cleanup_temp_images()
	count, image_ids = pdb.gimp_image_list()
	name = os.path.join(file_path, file_name)
	pdb.file_pdf_save_multi(count, tuple(reversed(image_ids)), True, True, False, name, name)

register(		
	"export_to_pdf",
	"Export to PDF",
	"Export all open images as pages in one pdf file.",
	"Robin Leandro",
	"Robin Leandro",
	"2023",
	"<Toolbox>/gimpfall/Export to PDF",
	"",
	[
		(PF_DIRNAME, "file_path", "The directory where the file will be saved", ''),
		(PF_STRING, "file_name", "The name of the PDF file to generate", default_filename)
	],
	[],
	export_to_pdf)

main()				 