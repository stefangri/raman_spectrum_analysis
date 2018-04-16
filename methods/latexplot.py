"""
Creates Plot of the fit result with latex fonts.
"""



import uncertainties.unumpy as unp
from scipy.special import wofz
import matplotlib as mlp
mlp.use('pgf')
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = '[lmroman10-regular]:+tlig;'
rcParams['text.usetex'] = True
rcParams['pgf.texsystem'] = 'lualatex'
rcParams['font.size'] = 10
rcParams['mathtext.fontset'] = 'custom'
rcParams['pgf.preamble'] = r'\usepackage[locale=DE]{siunitx}'
rcParams['text.latex.preamble'] = r'\usepackage[math-style=ISO,bold-style=ISO,sans-style=italic,nabla=upright,partial=upright,]{unicode-math}'
rcParams['axes.formatter.use_mathtext'] = True
rcParams['legend.fontsize'] = 10
rcParams['figure.figsize'] = 5.906, 3.937
rcParams['savefig.dpi'] = 300
from matplotlib.patches import Rectangle
from uncertainties.unumpy import nominal_values as noms
from uncertainties.unumpy import std_devs as stds
from siunitx import *
import sys

def voigt(x, x0, sigma, gamma):
    return  np.real(wofz(((x - x0) + 1j*gamma) / sigma / np.sqrt(2)))


def latexplot(label):
    plt.clf()
    x, y = np.genfromtxt(label + '/data_' + label + '.txt', unpack = True)
    borders = np.genfromtxt(label + '/spectrumborders_' + label + '.txt', unpack = True)
    y = y[(x > borders[0])  &  (x < borders[-1])]
    x = x[(x > borders[0])  &  (x < borders[-1])]
    FitData =  np.load(label + '/fitparams_' + label + '.npz')
    baseline = FitData['c']
    ctr = FitData['x0']
    sigma = FitData['sigma']
    gamma = FitData['gamma']
    height = FitData['height']
    fig, ax = plt.subplots(1,1)

    xplot = np.linspace(x[0], x[-1], 5000)

    yfit = np.ones(len(xplot)) * baseline
    for i in range(0, len(sigma)):
        ypeak = voigt(xplot, ctr[i], sigma[i], gamma[i]) * np.max(y)
        ax.text(ctr[i], voigt(ctr[i], ctr[i], sigma[i], gamma[i]) * np.max(y) + baseline, str(i + 1), fontsize=9)
        if i == 0:
            ax.plot(xplot, ypeak + baseline , linewidth = 0.5, color = 'grey', label = 'Gefittete Peaks')
        else:
            ax.plot(xplot, ypeak + baseline , linewidth = 0.5, color = 'grey')

        yfit += ypeak



    ax.plot(x, y, 'b-',label = 'Messdaten', linewidth = 0.5)
    ax.plot(xplot, yfit, 'r-', label = 'Fit', linewidth = 0.5)
    siunitx_ticklabels(ax)

    ax.set_xlabel(r'Raman Shift' r'$\displaystyle \,  / \si{cm^{-1}}$')
    ax.set_ylabel(r'Intensity' r'$\displaystyle\,  /  \si{Counts\per\second}$')
    ax.set_xlim(x[0], x[-1])
    ax.grid()
    ax.legend()
    fig.tight_layout()
    fig.savefig(label + '/latexplot_' + label + '.pdf')
    plt.close(fig)
    plt.clf()

if __name__ == '__main__':
    label = sys.argv[1]
    latexplot(label)
