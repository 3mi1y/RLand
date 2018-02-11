import sys
import requests
import json
import usaddress

########################
### Global Variables ###
########################
BASE_URL = 'http://gisservicemt.gov/arcgis/rest/services/MSL/Montana/GeocodeServer/findAddressCandidates'

# FIXME: This seems like a non-pythonic way to filter
# Used like this because we need to check for KeyErrors
# It seems like every entry will have a score, so maybe this could just be an inline lambda
def _sort_by_score(json):
	try:
		return json['score']
	except KeyError:
		return 0

def search_by_address(address):
	"""
	search_by_address(address) -> [address_candidates]
	Returns an array of properties matching the given address

	param: address (String): The address associated with the property
	"""

	address = usaddress.tag(address)
	street = ' '.join([address[0].get('AddressNumber', ''), address[0].get('StreetNamePreDirectional', ''), address[0].get('StreetName', ''), address[0].get('StreetNamePostType', '')])
	city = address[0].get('PlaceName', '')
	state = address[0].get('StateName', '')
	zip_code = address[0].get('ZipCode', '')
	
	payload = (('Street', street), ('City', city), ('State', state), ('ZIP', zip_code), ('f', 'json'))

	if address[1] == 'Street Address':
		# TODO: asynchronous?
		r = requests.post(BASE_URL, params=payload)

		candidates = [c for c in r.json()['candidates']]
		# Sort by 'score'
		candidates.sort(key=_sort_by_score, reverse=True)
		return candidates

	else:
		return []

l = search_by_address("32 Campus Drive, Missoula, MT, 59812")
print(l[0])
