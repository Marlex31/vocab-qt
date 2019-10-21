import csv
from collections import OrderedDict


with open('french.csv', 'r') as f:
	f_read = csv.reader(f) # DictReader() or reader()
	next(f_read)

	for line in f_read:
		print(line[0:2]) # only for reader()
 
		# print(dict(OrderedDict(line)))
		# print('\n')