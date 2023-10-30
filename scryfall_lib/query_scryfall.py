import requests
import os

SCRYFALL_URL = 'https://api.scryfall.com'
SEARCH_ENDPOINT = '/cards/search'

def query_scryfall(query='sol ring'):
	params = {
		'q': query,
		'order': 'edhrec'
	}
	# 2.7 so no string interpolation Sadge
	search_request = requests.get(SCRYFALL_URL+SEARCH_ENDPOINT, params=params)
	png_url = search_request.json()['data'][0]['image_uris']['png']
	image_request = requests.get(png_url)
	image_file = open('temp.png', 'wb')
	image_file.write(image_request.content)
	image_path = os.getcwd()+'\\'+image_file.name
	image_file.close()
	return image_path