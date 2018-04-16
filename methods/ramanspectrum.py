import numpy as np
import matplotlib.pyplot as plt
from uncertainties import correlated_values
from scipy.optimize import curve_fit
from uncertainties.unumpy import nominal_values as noms
from uncertainties.unumpy import std_devs as stds
from lmfit import Model
from scipy.special import wofz
from scipy.special import erf
from lmfit.models import ConstantModel
from lmfit.model import save_modelresult
from lmfit.model import load_modelresult
from uncertainties import ufloat

def voigt(x, x0, sigma, gamma):
    """
    Voigt function as model for the peaks. Calculated numerically
    with the complex errorfunction wofz
    (https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.special.wofz.html)
    """
    return  np.real(wofz(((x - x0) + 1j*gamma) / sigma / np.sqrt(2)))




def poly(x, a):
    """
    Constant function as model for the underground.
    """
    return [a for i in x]


class ramanspectrum(object):
    def __init__(self, data_file, label, peakfile = None, baselinefile = None, fitfile = None):
        self.x, self.y = np.genfromtxt(data_file, unpack = True)
        self.maxyvalue = np.max(self.y)
        self.y = self.y / self.maxyvalue
        self.label = label
        self.peakfile = peakfile
        self.baselinefile = baselinefile
        self.fitfile = fitfile


    def PlotRawData(self, show = True, ax = None):
        """
        Creates a plot of the raw data. show = True will show the plot, show = False will return a matplotlib object
        """

        if (ax != None):
            return ax.plot(self.x, self.y, 'kx', label = 'Messdaten', linewidth = 0.5)
        if(show == True):
            plt.plot(self.x, self.y, 'k-', label = 'Messdaten')
            plt.show()
        else:
            return plt.plot(self.x, self.y, 'bx', label = 'Messdaten', linewidth = 0.5)


    def SelectPeaks(self):
        """
        Function opens a Window with the data, you can choose initial values for the peaks by clicking on the plot.
        """

        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        polyparams = self.Fitbaseline()
        ax.plot(self.x, poly(self.x, *noms(polyparams)), 'r-')
        x = []
        y = []

        def onclickpeaks(event):
            if event.button:
                x.append(event.xdata)
                y.append(event.ydata)
                plt.plot(event.xdata, event.ydata, 'ko')
                fig.canvas.draw()

        cid = fig.canvas.mpl_connect('button_press_event', onclickpeaks)
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
        np.savetxt(self.label + '/locpeak_' + self.label + '.txt', np.transpose([np.array(x), np.array(y)])) # store the chosen initial values
        self.peakfile = self.label + '/locpeak_' + self.label + '.txt'

    def SelectBaseline(self):
        """
        Function opens a window with the data, you can select the regions that do not belong to backround signal by clicking.
        """
        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        ax.set_title('Baseline-Fit')
        ax.set_ylim(bottom = 0)
        x = []
        def onclickbase(event):
            if event.button:
                x.append(event.xdata)
                plt.vlines(x = event.xdata, color = 'r', linestyle = '--', ymin = 0, ymax = np.max(self.y))
                if(len(x) % 2 == 0 & len(x) != 1):
                    barx0 = np.array([(x[-1] - x[-2])/2])
                    height = np.array([np.max(self.y)])
                    width = np.array([x[-1] - x[-2]])
                    plt.bar(x[-2], height = height, width = width, align = 'edge',facecolor="red", alpha=0.2, edgecolor="black",linewidth = 5, ecolor = 'black',  bottom = 0)
                fig.canvas.draw()

        cid = fig.canvas.mpl_connect('button_press_event', onclickbase)
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
        np.savetxt(self.label + '/baseline_' + self.label + '.txt', np.array(x))
        self.baselinefile = self.label + '/baseline_'+ self.label + '.txt'


    def SelectSpectrum(self):
        """
        Select the interesting region in the spectrum.
        """

        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        ax.set_title('Select Spectrum')
        ax.set_ylim(bottom = 0)
        x = []
        def onclickbase(event):
            if event.button:
                x.append(event.xdata)
                plt.vlines(x = event.xdata, color = 'g', linestyle = '--', ymin = 0, ymax = np.max(self.y))
                if(len(x) % 2 == 0 & len(x) != 1):
                    barx0 = np.array([(x[-1] - x[-2])/2])
                    height = np.array([np.max(self.y)])
                    width = np.array([x[-1] - x[-2]])
                    plt.bar(x[-2], height = height, width = width, align = 'edge',facecolor="green", alpha=0.2, edgecolor="black",linewidth = 5, ecolor = 'black',  bottom = 0)
                fig.canvas.draw()

        cid = fig.canvas.mpl_connect('button_press_event', onclickbase)
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
        self.y = self.y[(self.x > x[0]) & (self.x < x[-1])]
        self.x = self.x[(self.x > x[0]) & (self.x < x[-1])]
        np.savetxt(self.label + '/spectrumborders_' + self.label + '.txt', np.array(x))



    def FitSpectrumInit(self, label):
        """
        Fit the spectrum with the fit params of another spectrum (given by label) as initial values. Useful when you fit big number of similar spectra.
        """


        borders = np.genfromtxt(label + '/spectrumborders_' + label + '.txt', unpack = True)
        np.savetxt(self.label + '/spectrumborders_' + self.label + '.txt', borders)
        self.y = self.y[(self.x > borders[0])  &  (self.x < borders[-1])]
        self.x = self.x[(self.x > borders[0])  &  (self.x < borders[-1])]
        FitData =  np.load(label + '/fitparams_' + label + '.npz')
        baseline = FitData['c'] / self.maxyvalue
        ctr = FitData['x0']
        sigma = FitData['sigma']
        gamma = FitData['gamma']
        ramanmodel = ConstantModel()
        ramanmodel.set_param_hint('c', value = baseline[0], min = 0)

        for i in range(len(sigma)):
            prefix = 'p' + str(i + 1)
            tempvoigt = Model(func = voigt, prefix = prefix)
            tempvoigt.set_param_hint(prefix + 'x0', value = ctr[i], min = 0)
            tempvoigt.set_param_hint(prefix + 'sigma', value = sigma[i], min = 0)
            tempvoigt.set_param_hint(prefix + 'gamma', value = gamma[i], min = 0)
            tempvoigt.set_param_hint(prefix + 'height', expr = 'wofz(((0) + 1j*'+ prefix + 'gamma) / '+ prefix + 'sigma / sqrt(2)).real')
            tempvoigt.set_param_hint(prefix + 'fwhm', expr = '0.5346 * 2 *' + prefix + 'gamma + sqrt(0.2166 * (2*' + prefix + 'gamma)**2 + (2 * ' + prefix + 'sigma * sqrt(2 * log(2) ) )**2  )')
            ramanmodel += tempvoigt



        pars = ramanmodel.make_params()
        fitresult = ramanmodel.fit(self.y, pars, x = self.x, scale_covar = True)


        plt.clf()
        comps = fitresult.eval_components()
        xplot = np.linspace(self.x[0], self.x[-1], 1000)
        plt.plot(self.x, self.y* self.maxyvalue, 'r-')
        plt.plot(self.x, fitresult.best_fit* self.maxyvalue)
        for i in range(0, len(sigma)):
            plt.plot(self.x, comps['p' + str(i+1)]* self.maxyvalue + comps['constant']* self.maxyvalue, 'k-')
        plt.savefig(self.label + '/rawplot_' + self.label + '.pdf')
        save_modelresult(fitresult, self.label + '/modelresult_' + self.label + '.sav')
        plt.clf()





    def FitSpectrum(self):
        """
        Fit Spectrum with initial values provided by SelectBaseline and SelectPeaks
        """

        polyparams = self.Fitbaseline(self)
        base = polyparams[0].n
        ramanmodel = ConstantModel()
        ramanmodel.set_param_hint('c', value = base, min = 0)
        globwidth = 1

        xpeak, ypeak = np.genfromtxt(self.peakfile, unpack = True)


        for i in range(0, len(xpeak)):
            prefix = 'p' + str(i + 1)

            tempvoigt = Model(func = voigt, prefix = prefix)
            tempvoigt.set_param_hint(prefix + 'x0', value = xpeak[i], min = 0)
            tempvoigt.set_param_hint(prefix + 'sigma', value = globwidth, min = 0)
            tempvoigt.set_param_hint(prefix + 'gamma', value = globwidth, min = 0)
            tempvoigt.set_param_hint(prefix + 'height',value = ypeak[i], expr = 'wofz(((0) + 1j*'+ prefix + 'gamma) / '+ prefix + 'sigma / sqrt(2)).real')
            tempvoigt.set_param_hint(prefix + 'fwhm', expr = '0.5346 * 2 *' + prefix + 'gamma + sqrt(0.2166 * (2*' + prefix + 'gamma)**2 + (2 * ' + prefix + 'sigma * sqrt(2 * log(2) ) )**2  )')
            ramanmodel += tempvoigt



        pars = ramanmodel.make_params()
        fitresult = ramanmodel.fit(self.y, pars, x = self.x, scale_covar = True)






        print(fitresult.fit_report(min_correl=0.5))
        comps = fitresult.eval_components()
        xplot = np.linspace(self.x[0], self.x[-1], 1000)
        plt.plot(self.x, self.y* self.maxyvalue, 'rx')
        plt.plot(self.x, fitresult.best_fit* self.maxyvalue)
        for i in range(0, len(xpeak)):
            plt.plot(self.x, comps['p' + str(i+1)]* self.maxyvalue + comps['constant']* self.maxyvalue, 'k-')
        plt.show()
        plt.savefig(self.label + '/rawplot_' + self.label + '.pdf')
        save_modelresult(fitresult, self.label + '/modelresult_' + self.label + '.sav')


    def SaveFitParams(self):
        """
        Save the Results of the fit in a .zip file using numpy.savez().
        """

        fitresult = load_modelresult(self.label + '/modelresult_' + self.label + '.sav')

        fitparams = fitresult.params
        c, stdc, x0, stdx0, height, stdheight, sigma, stdsigma, gamma, stdgamma, fwhm, stdfwhm = ([] for i in range(12))

        for name in list(fitparams.keys()):
            par = fitparams[name]
            param = ufloat(par.value, par.stderr)

            if ('c' in name):
                param = param *  self.maxyvalue
                c.append(param.n)
                stdc.append(param.s)

            elif ('height' in name):
                param = param *  self.maxyvalue
                height.append(param.n)
                stdheight.append(param.s)

            elif ('x0' in name):
                x0.append(param.n)
                stdx0.append(param.s)

            elif ('sigma' in name):
                sigma.append(param.n)
                stdsigma.append(param.s)

            elif ('gamma' in name):
                gamma.append(param.n)
                stdgamma.append(param.s)

            elif ('fwhm' in name):
                fwhm.append(param.n)
                stdfwhm.append(param.s)


        np.savez(self.label + '/fitparams_' + self.label , x0 = x0, stdx0 = stdx0, c = c, stdc = c, height = height, stdheight = stdheight, sigma = sigma, stdsigma = stdsigma, gamma = gamma, stdgamma = stdgamma, fwhm = fwhm, stdfwhm = stdfwhm)



    def Fitbaseline(self,  show = False):

        bed = np.genfromtxt(self.baselinefile, unpack = True) # load the data from SelectBaseline
        #generate mask for baseline fit
        bgndx = (self.x <= bed[0])
        for i in range(1, len(bed) - 2, 2):
            bgndx = bgndx | ((self.x >= bed[i]) & (self.x <= bed[i + 1]))
        bgndx = bgndx | (self.x >= bed[-1])

        #FIT Baseline
        polyparams, cov = curve_fit(poly, self.x[bgndx], self.y[bgndx])
        if (show == True):
            self.PlotRawData(False)
            xplot = np.linspace(self.x[0], self.x[-1], 100)
            plt.plot(xplot, poly(xplot, *polyparams), 'r-')
            plt.show()
        self.base = polyparams[0]
        return correlated_values(polyparams, cov)
