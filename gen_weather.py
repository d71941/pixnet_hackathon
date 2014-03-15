import datetime, os, json, urllib2, time, sys

LOCATION_PATH = "locations.json"
KEY_PATH = "keys.json"

WEATHER_API_URL = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"

def load_locations(location_path):
	locations = []
	f = open(location_path)
	locations +=  json.load(f)

	return locations

def get_weather(weather_date, weather_location, key):
	try:
		response = urllib2.urlopen("%s?q=%f,%f&date=%s&key=%s&format=json" % (WEATHER_API_URL, weather_location['lat'], weather_location['lon'], weather_date.strftime("%Y-%m-%d") ,key), timeout=5)
	except:
		print "Can't get %s/%s.json" % (l["name"].encode('utf8'), weather_date.strftime("%Y-%m-%d"))
		return None;

	return response.read()


def load_keys():
	key_file = open(KEY_PATH)
	keys = json.load(key_file)
	return keys

########################################################

begin = int(sys.argv[1])
end = int(sys.argv[2])

locations = load_locations(LOCATION_PATH)
keys = load_keys()
key_index = 0

for l in locations[begin:end+1]:
	print "Getting weather data for %s..." % (l["name"].encode('utf8'))

	if not os.path.exists(l["name"].encode('utf8')):
		os.makedirs(l["name".encode('utf8')])

	weather_date = datetime.date(2013, 01, 01)
	while weather_date < datetime.date(2014, 01, 01):

		file_path = l["name"].encode('utf8')+'/'+weather_date.strftime("%Y-%m-%d")+".json"
		if os.path.exists(file_path):
			weather_date = weather_date + datetime.timedelta(1)
			continue

		json_string = get_weather(weather_date, l, keys[key_index]['key'])
		if json_string:
			f = open(file_path, "w")
			f.write(json_string)
			f.close()
			weather_date = weather_date + datetime.timedelta(1)
		else:
			key_index = (key_index + 1) % len(keys)

		print "."
		time.sleep(1)


'''
if not os.path.exists(locations[0]["name"].encode('utf8')):
    os.makedirs(locations[0]["name".encode('utf8')])
f = open(locations[0]["name"].encode('utf8')+'/'+weather_date.strftime("%Y-%m-%d")+".json", "w")
f.write(json)
'''
