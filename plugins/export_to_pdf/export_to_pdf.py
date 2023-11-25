#!/usr/bin/python
from gimpfu import register, main, pdb, PF_FILE
import os, sys

plugin_path = os.path.abspath(sys.argv[0])
module_path = os.path.join(plugin_path.rpartition('gimpfall')[0],'gimpfall')
# not ideal to append to syspath like this
# but since gimp runs its own python instance its required for modules to work
sys.path.append(module_path)
from gimp_utils.gimp import cleanup_temp_images

default_filename = os.path.join(plugin_path.rpartition(os.path.join('/'))[0],'untitled.pdf')

def export_to_pdf(file_name=default_filename):
	cleanup_temp_images()
	count, image_ids = pdb.gimp_image_list()
	pdb.file_pdf_save_multi(count, tuple(reversed(image_ids)), True, True, False, file_name, file_name)

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
		(PF_FILE, "file_name", "The name of the PDF file to generate", default_filename)
	],
	[],
	export_to_pdf)

main()				 