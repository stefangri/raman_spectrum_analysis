from ramanspectrum import *
import sys
import time



def analyze(label):
    """
    Combination of the methods provided by ramanspectrum class.
    """

    spec = ramanspectrum(label + '/data_' + label + '.txt', label = label)
    spec.SelectSpectrum()
    spec.SelectBaseline()
    spec.SelectPeaks()
    spec.FitSpectrum()


if __name__ == '__main__':
    label = sys.argv[1]
    analyze(label)
