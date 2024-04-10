# fds python wpifire
# js

# imports
import fdsreader
import os
from collections import defaultdict
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.rcParams['font.size'] = 14
plt.rcParams['lines.linewidth'] = 2.0


def importFile(fdsPath= None):
    pass

def mlr_plotter():

    mdot_out = sim.devices['TMF YOUT'].data
    sim_time = sim.devices['Time'].data

    plt.figure()
    plt.semilogy(sim_time,-mdot_out*1E3)
    plt.title(r'$\dot{m}_{\text{HF}}$ [g/s]')
    plt.xlabel('Time [sec]')

    plt.savefig(outputDir+'mdot.png',dpi=300,bbox_inches='tight')
    plt.savefig(outputDir+'mdot.eps',dpi=300,bbox_inches='tight')

    print(f'Fin.')

def fds_fde_plotter(sim_time: np.ndarray):
    print('\t\t- FDE Plotter')
    fed_dev = sim.devices['FED001'].data
    fid_dev = sim.devices['FIC001'].data

    plt.figure()
    
    plt.semilogy(sim_time,fed_dev,label = 'FED')
    plt.semilogy(sim_time,fid_dev,label = 'FID')

    plt.title(r'Fractional Effective Dosage')
    plt.xlabel('Time [sec]')
    plt.legend(frameon=True,fancybox=True)

    plt.savefig(outputDir+'fds_dev.png',dpi=300,bbox_inches='tight')
    plt.savefig(outputDir+'fds_dev.eps',dpi=300,bbox_inches='tight')


def tke_plot(sim_time: np.ndarray):
    uvel = sim.devices['UPROBE'].data
    vvel = sim.devices['VPROBE'].data
    wvel = sim.devices['WPROBE'].data

    kgs = sim.devices['KGSPROBE'].data
    FFT_U = abs(np.fft.fft(uvel))**2
    FFT_V = abs(np.fft.fft(vvel))**2
    FFT_W = abs(np.fft.fft(wvel))**2
    TKE_plot = FFT_U+FFT_V+FFT_W

    TKE = 0.5 * ((uvel - uvel.mean())**2 + (vvel - vvel.mean())**2 + (wvel - wvel.mean())**2)
    print(f'\t\t Measure of Turbulent Resolution (M): {M}')

    plt.semilogy(TKE_plot)
    
    plt.savefig(outputDir+'tke_dev.png',dpi=300,bbox_inches='tight')
    plt.savefig(outputDir+'tek_dev.eps',dpi=300,bbox_inches='tight')


if __name__ =='__main__':
    systemPath = os.path.dirname('/scratch/06726/jslaten/fire_jobs/008/')
    inputFDSFile = os.path.join(systemPath,"wpifire.001.fds")
    outputDir = os.path.join('/scratch/06726/jslaten/generated/')

    print('Importing WPI Fire model',flush=True)
    timestart=time.time()
    sim = fdsreader.Simulation(systemPath)
    timeend=time.time()
    print(f'\t Total time taken {timeend-timestart:.4f}')
    sim_time = sim.devices['Time'].data

    # mlr_plotter(sim_time)
    # fds_fde_plotter(sim_time)
    tke_plot(sim_time)
    