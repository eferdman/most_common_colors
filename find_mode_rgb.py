import requests
from PIL import Image
from io import BytesIO
from scipy import stats
import csv

image_url_file = open('image_urls.txt', mode='r')
with open('output.csv', mode='w') as output_file:
		csv_writer = csv.writer(output_file, delimiter=',', quotechar='"')
		for url in image_url_file:
			url = url.rstrip('\n')
			row = [url]
			r = requests.get(url, stream=True)
			r.raw.decode_content = True
			img = Image.open(BytesIO(r.content))
			rgb_values = list(img.getdata())
			hex_values = ["{:02x}{:02x}{:02x}".format(*x) for x in rgb_values]
			hex_to_ints = [int(x, 16) for x in hex_values]

			# find the 3 modes, convert back to hex_code, append to row
			for i in range(3):
				mode = stats.mode(hex_to_ints).mode[0]
				# format hex code string
				hex_code = hex(mode)[2:]
				if len(hex_code) < 6:
					for i in range(6 - len(hex_code)):
						hex_code = '0' + hex_code
				hex_code = "#{}".format(hex_code)
				row.append(hex_code)
				# remove last mode from list
				hex_to_ints = [x for x in hex_to_ints if x!= mode]

			csv_writer.writerow(row)
			output_file.flush()
