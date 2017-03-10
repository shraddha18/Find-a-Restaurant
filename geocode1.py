import httplib2
import json

def getGeocodeLocation(inputString):
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    google_api_key = "ENTER_API_KEY_HERE"
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)
