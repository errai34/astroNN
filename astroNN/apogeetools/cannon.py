# ---------------------------------------------------------#
#   astroNN.apogeetools.cannon: cannon tools
# ---------------------------------------------------------#

import os
from astropy.io import fits
import numpy as np
import astroNN.apogeetools.downloader
import astroNN.datasets.h5_compiler
import astroNN.NN.test
import pylab as plt
from astropy.stats import mad_std


def cannon_plot(apogee_indexlist, num_labels, std_labels, target, folder_name=None, aspcap_answer=None):
    """
    NAME: cannon_plot
    PURPOSE: plot cannon result
    INPUT:0
    OUTPUT: plots
    HISTORY:
        2017-Oct-27 Henry Leung
    """
    cannon_fullfilename = astroNN.apogeetools.downloader.allstarcannon(dr=14)
    cannonplot_fullpath = os.path.join(folder_name, 'Cannon_Plots/')
    if not os.path.exists(cannonplot_fullpath):
        os.makedirs(cannonplot_fullpath)
    hdulist = fits.open(cannon_fullfilename)

    x_lab = 'ASPCAP'
    y_lab = 'Cannon'

    i = 0
    for i in range(num_labels):
        tg = astroNN.NN.test.target_to_aspcap_conversion(target[i])
        try:
            cannon_result = (hdulist[1].data['{}'.format(tg)])[apogee_indexlist]
            resid = cannon_result - aspcap_answer[:, i]
            madstd = mad_std(resid, axis=0)
            mean = np.mean(resid, axis=0)
            plt.figure(figsize=(15, 11), dpi=200)
            plt.axhline(0, ls='--', c='k', lw=2)
            plt.scatter(aspcap_answer[:, i], resid, s=3)
            fullname = astroNN.NN.test.target_name_conversion(target[i])
            plt.xlabel('ASPCAP ' + fullname, fontsize=25)
            plt.ylabel('$\Delta$ ' + fullname + '\n(' + y_lab + ' - ' + x_lab + ')', fontsize=25)
            plt.tick_params(labelsize=20, width=1, length=10)
            if num_labels == 1:
                plt.xlim([np.min(aspcap_answer[:, i]), np.max(aspcap_answer[:, i])])
            else:
                plt.xlim([np.min(aspcap_answer[:, i]), np.max(aspcap_answer[:, i])])
            ranges = (np.max(aspcap_answer[:, i]) - np.min(aspcap_answer[:, i])) / 2
            plt.ylim([-ranges, ranges])
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=2)
            plt.figtext(0.6, 0.75,'$\widetilde{m}$=' + '{0:.3f}'.format(mean[i]) + ' $\widetilde{s}$=' + '{0:.3f}'.format(
                madstd / std_labels[i]) + ' s=' + '{0:.3f}'.format(madstd), size=25, bbox=bbox_props)
            plt.tight_layout()
            plt.savefig(cannonplot_fullpath + '{}_Cannon.png'.format(target[i]))
            plt.close('all')
            plt.clf()
        except KeyError:
            pass
        i += 1
    return None
