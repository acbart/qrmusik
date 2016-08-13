import sys
import os
from PIL import Image
import subprocess

"""
Build code sheet from definitions file:
* First line: comma-separated numbers 
  total target image width in pixels, height,  target dimensions for square icons in pixels, number of rows to make, number of cols to make
* One line per code/icon pair:
  string to encode first, then a comma, then the path to the Icon image
"""


if len(sys.argv) < 3:
	print "Usage: {:s} config_file.txt out_file.png".format(sys.argv[0])
	exit(-1)


# read config file
with open(sys.argv[1]) as f:
	lines = f.readlines()


# parse image configuration
words = lines[0].split()
width = int(words[0])
height = int(words[1])
icon_size = int(words[2])
n_rows = int(words[3])
n_cols = int(words[4])

print "Targe image size: {:d} x {:d}, icon size {:d}, making {:d} rows and {:d} cols".format(width, height, icon_size, n_rows, n_cols)


# offset for each code/icon pair
x_offset = width / float(n_cols)
y_offset = height / float(n_rows)

# margin: quarter for x, because we paste an image pair
x_margin = (x_offset - 2 * icon_size)/4.
y_margin = (y_offset - icon_size)/2.


# combined image
out = Image.new('RGBA', (width, height), color=(255, 255, 255, 255))


# tmp file for QR codes
qr_tmp_file	= "qr_tmp.png"


# build combined image
for i_line, line in enumerate(lines[1:]):
	# row/col to paste in
	row = i_line / n_cols
	col = i_line - n_cols * row

	# extract line data
	words = line.split(',')
	data = words[0].strip()
	icon = words[1].strip()

	# build QR code, read it in
	subprocess.check_call(["qrencode", "-s", "5", "-o", qr_tmp_file, data])
	qr = Image.open(qr_tmp_file)

	# read icon
	ic = Image.open(icon)

	# resize icon
	ic = ic.resize((icon_size, icon_size))

	# offset for qr/icon pair
	x = col * x_offset
	y = row * y_offset

	# paste both, using icon as mask for itself to handle transparency
	out.paste(qr, (int(x + x_margin), int(y + y_margin)))
	out.paste(ic, (int(x + x_offset/2. + x_margin), int(y + y_margin)))

	# clean up
	os.remove(qr_tmp_file)

# save output image
out.save(sys.argv[2])

