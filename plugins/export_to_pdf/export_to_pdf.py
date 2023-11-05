#!/usr/bin/python
from gimpfu import *
import os, sys

plugin_path = os.path.abspath(sys.argv[0])
default_filename = plugin_path.rpartition('\\')[0]+'\\untitled.pdf'

def export_to_pdf(file_name=default_filename):
	count, image_ids = pdb.gimp_image_list()
	pdb.file_pdf_save_multi(count, image_ids, True, True, False, file_name, file_name)

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