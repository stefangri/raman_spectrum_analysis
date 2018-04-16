from ramanspectrum import *
import sys

"""
Run python 'autoplot.py labels.txt'. Creates simple plots of the spectra.
"""

label = sys.argv[1]
with open('labels.txt', 'r') as file:
	labels = file.readlines()
for i in range(len(labels)):
	labels[i] = labels[i].rstrip()

for label in labels:
	label = label.split(r'\n')[0]
	spec = ramanspectrum(data_file = label + '/data_' + label + '.txt',label = label)
	plt.clf()
	plt.plot(spec.x, spec.y, 'b-')
	plt.xlim(self.x[0], 550)
	plt.savefig(label + '/simpleplot_' + label + '.pdf')
