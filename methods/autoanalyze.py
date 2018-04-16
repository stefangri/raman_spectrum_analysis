from ramanspectrum import *
import sys

"""
Method to analyze several spectra with equal shape. Run python 'autonalyze.py labels.txt'. Fit the first spectrum interactivilly, the next
spectra will be analyzed automatically using the fit params of the previous spectrum as initial values for the next one.

"""
labelfile = sys.argv[1]
with open(labelfile, 'r') as file:
	labels = file.readlines()
for i in range(len(labels)):
	labels[i] = labels[i].rstrip()



for i in range(len(labels)):
	label = labels[i]
	label = label.split(r'\n')[0]
	spec = ramanspectrum(data_file = label + '/data_' + label + '.txt',label = label)
	print('analyzing ' + label)

	if i == 0:
		spec.SelectSpectrum()
		spec.SelectBaseline()
		spec.SelectPeaks()
		spec.FitSpectrum()
		spec.SaveFitParams()

	else:
		spec.FitSpectrumInit(label = labels[i - 1])
		spec.SaveFitParams()
