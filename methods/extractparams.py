import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf
from lmfit import Model
from ramanspectrum import *
import uncertainties.unumpy as unp
from uncertainties.unumpy import nominal_values as noms
from uncertainties.unumpy import std_devs as stds

with open('labels.txt', 'r') as file:
	labels = file.readlines()
for i in range(len(labels)):
	labels[i] = labels[i].rstrip()


for peaknum in range(7):
	wid = []
	ctr = []
	peak = []
	gamma = []
	sigma = []
	displacement = []
	for label in labels:
		label = label.split(r'\n')[0]
		dist = label.split('_')[1]
		dist = dist.split('µ')[0]
		dist = dist.replace(',', '.')
		dist = float(dist)
		displacement.append(dist)
		FitData =  np.load(label + '/fitparams_' + label + '.npz')
		width = FitData['fwhm']
		center = FitData['x0']
		gam = FitData['gamma']
		sig = FitData['sigma']
		height = FitData['height']
		c = FitData['c']
		sigma.append(sig[peaknum])
		ctr.append(center[peaknum])
		wid.append(width[peaknum])
		peak.append(height[peaknum])
		gamma.append(gam[peaknum])
		plt.clf()



	displacement = np.array(displacement)
	wid = np.array(wid)
	ctr = np.array(ctr)
	peak = np.array(peak)
	gamma = np.array(gamma)
	sigma = np.array(sigma)
	np.savetxt('../results/params/params' + str(peaknum + 1) +'.txt', np.column_stack([displacement, peak, ctr, wid, gamma, sigma]), header = 'x, height, center, fwhm, gamma, sigma')

	plt.clf()
	plt.plot(displacement, gamma , '.', label = str(peaknum +1))
	plt.legend()
	plt.savefig('../results/gamma/gamma' + str(peaknum + 1) + '.pdf')
	plt.clf()

	plt.plot(displacement, sigma , '.', label = str(peaknum +1))
	plt.legend()
	plt.savefig('../results/sigma/sigma' + str(peaknum + 1) + '.pdf')
	plt.clf()

	plt.plot(displacement, wid , '.', label = str(peaknum +1))
	plt.legend()
	plt.savefig('../results/width/width' + str(peaknum + 1) + '.pdf')
	plt.clf()

	plt.plot(displacement, ctr , '.', label = str(peaknum+1))
	plt.legend()
	plt.savefig('../results/center/center' + str(peaknum + 1) + '.pdf')
	plt.clf()

	plt.plot(displacement, peak , '.', label = str(peaknum+1))
	plt.legend()
	plt.savefig('../results/height/height' + str(peaknum + 1) + '.pdf')
	plt.clf()

	plt.clf()
	plt.subplot(311)
	plt.grid()
	plt.plot(displacement, wid, 'g.')# / np.max(wid)
	plt.ylabel('Halbwertsbreite')

	plt.subplot(312)
	plt.grid()
	plt.plot(displacement, ctr, 'b.')#
	plt.ylabel('Position')

	plt.subplot(313)
	plt.plot(displacement, peak / np.max(peak), 'r.')
	plt.ylabel('Intensität')
	plt.xlabel('Verschiebung')
	plt.grid()
	plt.savefig('../results/compare_params/comparison' + str(peaknum + 1) + '.pdf')
	plt.clf()
