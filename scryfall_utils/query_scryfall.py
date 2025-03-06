import urllib, urllib2, ssl
import json
import os, sys

plugin_path = os.path.abspath(sys.argv[0])
card_directory = os.path.join(plugin_path.rpartition('gimpfall')[0], 'gimpfall', 'cards')

SCRYFALL_CERT = os.path.join(plugin_path.rpartition('gimpfall')[0], 'gimpfall', 'scryfall-com-chain.pem')
SCRYFALL_URL = 'http://api.scryfall.com'
SEARCH_ENDPOINT = '/cards/search'

if not os.path.exists(card_directory):
  os.mkdir(card_directory)

def query_scryfall(query='sol ring'):
	os.chdir(card_directory)
	params = {
		'q': '!"{q}" is:hires game:paper (border:black or border:borderless)'.format(q=query),
		'order': 'edhrec'
	}

	# urllib2's data param in this function works in the request body, not url (it also makes request a post)
	# instead we use urllib "1" to encode the query params onto a string and append it to the url
	# also, cert issues caused me to have to download scryfalls cert and provide it here (maybe a windows issue since it worked on linux)
	# if something breaks maybe update the cert or make the request normally
	response = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl.create_default_context(cafile=SCRYFALL_CERT)), urllib2.ProxyHandler({})).open(SCRYFALL_URL+SEARCH_ENDPOINT+'?'+urllib.urlencode(params)).read()
	response_json = json.loads(response)['data'][0]

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

	#image_request = urllib2.urlopen(png_url)
	image_request = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl.create_default_context(cafile=SCRYFALL_CERT)), urllib2.ProxyHandler({})).open(png_url)
	
	image_file = open(filename, 'wb')
	image_file.write(''.join(image_request.readlines()))
	image_file.close()
	return os.path.join(card_directory, filename)