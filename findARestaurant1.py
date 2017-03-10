from geocode1 import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "CLIENT_ID_GOES_HERE"
foursquare_client_secret = "CLIENT_SECRET_GOES_HERE"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s'% (foursquare_client_id,foursquare_client_secret,latitude,longitude,mealType))
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])
	#return result

	if result['response']['venues']:
		#3. Grab the first restaurant
		firstrestaurant = result['response']['venues'][0]
		restaurant_name = firstrestaurant['name']
		restaurant_id = firstrestaurant['id']
		restaurant_address = firstrestaurant['location']['formattedAddress']
		if firstrestaurant['contact'].get('phone'):
			restaurant_phonenumber = firstrestaurant['contact']['phone']
		else:
			restaurant_phonenumber = "Not available"
		address = ""
		for n in restaurant_address:
			address += n + " "
		restaurant_address = address
		#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((restaurant_id,foursquare_client_id,foursquare_client_secret)))
		result = json.loads(h.request(url, 'GET')[1])
		#return result

		if result['response']['photos']['items']:
			#5. Grab the first image
			firstimage=result['response']['photos']['items'][0]
			prefix=firstimage['prefix']
			suffix=firstimage['suffix']
			imageURL = prefix + "300x300" + suffix
			#6. If no image is available, insert default a image url
		else:
			imageURL = "https://pixabay.com/en/new-york-manhattan-nyc-panoramic-1920757/"
		#7. Return a dictionary containing the restaurant name, address, and image url
		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL, 'phone':restaurant_phonenumber}
		print "Restaurant Name: %s" % restaurantInfo['name']
		print "Restaurant Address: %s" % restaurantInfo['address']
		print "Image: %s " % restaurantInfo['image']
		print "Phone number: %s \n" % restaurantInfo['phone']
		return restaurantInfo
	else:
		print "No Restaurants Found for %s" % location
		return "No Restaurants Found"

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Indian", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Ceviche", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")
	findARestaurant("Churros","Madrid, Spain")
