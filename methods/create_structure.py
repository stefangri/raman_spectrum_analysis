import os
import glob
import shutil




def create_structure():
    """
    Method to create a folder structure for the raman spectra. Later you can store the results for every spectrum in the folder named by the
    file with the original data.
    """


    labels = glob.glob('*.txt')

    for i in labels:
        os.makedirs(i.split('.')[0] )
        os.rename(i, i.split('.')[0] + '/data_' + i)

    for i in range(len(labels)):
        labels[i] = labels[i].split('.')[0]

    with open('labels.txt', 'w') as w: #save list of labels so that you can easy iterate all spectra later
        for i in labels:
            w.write(i + '\n')

if __name__ == '__main__':
    create_structure()
