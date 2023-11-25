import urllib2, urllib
import json
import os, sys

SCRYFALL_URL = 'https://api.scryfall.com'
SEARCH_ENDPOINT = '/cards/search'

plugin_path = os.path.abspath(sys.argv[0])
card_directory = os.path.join(plugin_path.rpartition('gimpfall')[0], 'gimpfall', 'cards')

if not os.path.exists(card_directory):
  os.mkdir(card_directory)
os.chdir(card_directory)

def query_scryfall(query='sol ring'):
	params = {
		'q': '!"{q}" is:hires game:paper (border:black or border:borderless)'.format(q=query),
		'order': 'edhrec'
	}

	# the data param in this function works in the request body, not url (also makes request a post)
	# but this fugly concatenation does the trick!
	response = urllib2.urlopen(SCRYFALL_URL+SEARCH_ENDPOINT+'?'+urllib.urlencode(params))
	response_json = json.load(response)['data'][0]

	# check if image is cached
	filename = "{name}_{id}.png".format(name = response_json['name'].encode('ascii', 'ignore').lower().replace(' ', '_').replace('//', '-'), id = response_json['id'])
	if os.path.isfile(filename):
		return os.path.join(card_directory, filename)

	# not cached, get from scryfall
	# double faced cards have this instead of a 'image_uris' value in the root document
	if 'card_faces' in response_json:
		png_url = response_json['card_faces'][0]['image_uris']['png']
	else:
		png_url = response_json['image_uris']['png']

	image_request = urllib2.urlopen(png_url)
	
	image_file = open(filename, 'wb')
	image_file.write(''.join(image_request.readlines()))
	image_file.close()
	return os.path.join(card_directory, filename)