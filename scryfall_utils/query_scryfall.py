import requests
import os, sys

SCRYFALL_URL = 'https://api.scryfall.com'
SEARCH_ENDPOINT = '/cards/search'

plugin_path = os.path.abspath(sys.argv[0])
card_directory = plugin_path.rpartition('\\')[0]+"\\cards"

if not os.path.exists(card_directory):
  os.mkdir(card_directory)
os.chdir(card_directory)

def query_scryfall(query='sol ring'):
	params = {
		'q': '!"{q}" is:hires game:paper (border:black or border:borderless)'.format(q=query),
		'order': 'edhrec'
	}
	# 2.7 so no string interpolation Sadge
	search_request = requests.get(SCRYFALL_URL+SEARCH_ENDPOINT, params)
	response_json = search_request.json()['data'][0]

	# check if image is cached
	filename = "{name}_{id}.png".format(name = response_json['name'].encode('ascii', 'ignore').lower().replace(' ', '_').replace('//', '-'), id = response_json['id'])
	if os.path.isfile(filename):
		return card_directory+'\\'+filename

	# not cached, get from scryfall
	# double faced cards have this instead of a 'image_uris' value in the root document
	if 'card_faces' in response_json:
		png_url = response_json['card_faces'][0]['image_uris']['png']
	else:
		png_url = response_json['image_uris']['png']
	image_request = requests.get(png_url)
	image_file = open(filename, 'wb')
	image_file.write(image_request.content)
	image_file.close()
	return card_directory+'\\'+filename