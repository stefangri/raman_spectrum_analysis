"""
Run autolatexplot.py labels.txt. Creates latex plots for all spectra in labels.txt.
"""


from latexplot import *
import sys

labelfile = sys.argv[1]
with open(labelfile, 'r') as file:
	labels = file.readlines()
for i in range(len(labels)):
	labels[i] = labels[i].rstrip()

for label in labels:
	label = label.split(r'\n')[0]
	latexplot(label)
