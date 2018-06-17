import matplotlib as mlp
mlp.use('pgf')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = '[lmroman10-regular]:+tlig;' #use \showthe\font in latex document to get the right font key
rcParams['text.usetex'] = True
rcParams['pgf.texsystem'] = 'lualatex'
rcParams['font.size'] = 10
rcParams['mathtext.fontset'] = 'custom'
rcParams['pgf.preamble'] = r'\usepackage[locale=DE]{siunitx}'
rcParams['text.latex.preamble'] = r'\usepackage[math-style=ISO,bold-style=ISO,sans-style=italic,nabla=upright,partial=upright,]{unicode-math}'
rcParams['axes.formatter.use_mathtext'] = True
rcParams['legend.fontsize'] = 10
rcParams['figure.figsize'] =  5.906, 3.937 # size of the figure in inch
rcParams['savefig.dpi'] = 300
import numpy as np


fig, ax = plt.subplots(1, 1)
x, y = np.genfromtxt('data.txt', unpack = True)

ax.plot(x, y, linestyle = '-', label = r'Data', color = '#1f77b4')



#sub_ax = fig.add_axes([0.58, 0.55, 0.3, 0.3], xlim = (0, 1), ylim = (0, 1))
#sub_ax.plot(x, x**2)
#sub_ax.text(0.02 , 0.98, '(b)', horizontalalignment='left', verticalalignment='top', transform = sub_ax.transAxes)

ax.legend(loc = 'best')
ax.set_ylabel(r'Intensity $/ \si{Counts \per \second}$')
ax.set_xlabel(r'Ramanshift $/ \si{\centi\meter^{-1}}$')
ax.text(0.02 , 0.98, '(a)', horizontalalignment='left', verticalalignment='top', transform = ax.transAxes)
ax.set_xlim(x[0], 600)

fig.savefig('plot.pdf', bbox_inches = 'tight', pad_inches = 0)
