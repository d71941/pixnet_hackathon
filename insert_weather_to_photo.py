import sys, json, datetime, os, math


WEATHER_PATH = "weathers.json"
ALBUM_PATH = "album_location"
ALBUM_WEATHER_PATH = "album_weather"

def get_weather_for_photo(year, weather_data, photo):
		#print "id = %s" % (photo["id"])

		location_index = photo["location"]["city"]
		photo_datetime = datetime.datetime.fromtimestamp(int(photo["taken_at"]))

		if photo_datetime.year != year:
			return None

		day_of_year = (photo_datetime.date() - datetime.date(year, 01, 01)).days
		mintue_of_day = photo_datetime.hour*60 + photo_datetime.minute
		#print photo_datetime
		#print mintue_of_day

		day_weather = weather_data[location_index][day_of_year]

		hour_index = -1
		min_diff = 9999
		for i, hour_weather in enumerate(day_weather["hourly"]):
			time_string = hour_weather["time"]
			diff = abs(mintue_of_day - (int(time_string[:-2])*60 + int(time_string[-2:])))
			if diff < min_diff:
				min_diff = diff
				hour_index = i

		if hour_index < 0:
			return None

		weather = {key:day_weather["hourly"][hour_index].get(key, None) for key in ('cloudcover', 'humidity', 'precipMM', 'tempC', 'visibility', 'weatherCode')}
		weather = dict(weather.items() + day_weather["astronomy"][0].items())
		return weather




################################################################

year = int(sys.argv[1])

f = open(str(year) + '/' + WEATHER_PATH)
weather_data = json.load(f)
f.close()

dir_path = str(year) + '/' + ALBUM_WEATHER_PATH
if not os.path.exists(dir_path):
	os.makedirs(dir_path)

total = 0

for filename in os.listdir(ALBUM_PATH + "/"):
	f = open(ALBUM_PATH + "/" + filename)
	photo_data = json.load(f)
	f.close()

	output_file_path = dir_path + "/" + filename.split('.')[0] + ".json"

	print "%s -> %s" % (ALBUM_PATH + "/" + filename, output_file_path)

	category_valid = 0
	output_photos = []
	for photo in photo_data:
		weather = get_weather_for_photo(year, weather_data, photo)
		if(weather):
			#print weather
			photo["weather"] = weather
			output_photos.append(photo)

	total += len(output_photos)
	f = open(output_file_path, "w")
	f.write(json.dumps(output_photos))
	f.close()


print total

