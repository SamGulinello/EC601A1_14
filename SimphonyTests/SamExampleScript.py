"""
Simulated Photonic Circuit Capable of Adding Two Numbers
"""

import matplotlib.pyplot as plt
import math
import numpy as np

from simphony.libraries import siepic
from simphony.simulation import Detector, Laser, Simulation

WAVELENGTH = 1550e-9
PI = math.pi


def getAmplitude(freq):

    lightSpeed = 299792458.0
    TwoPi = math.pi * 2

    return (lightSpeed / freq / TwoPi)

def getRelativePhase(len1, len2):
    pass

def wlToFreq(wl):

    # speed of light divided by wavelength
    return 299792458.0 / wl

def freqToWL(freq):

    # speed of light divided by frequency
    return 299792458.0 / freq

def Add(num1, num2):
    y_recombiner = siepic.YBranch()
    with Simulation() as sim:
        l1 = Laser(power = num1)
        l2 = Laser(power = num2)

        Detector().connect(y_recombiner)
        l1.connect(y_recombiner)
        l2.connect(y_recombiner)

        theoretical = sim.sample()
    
    return theoretical[0,0,0]

def Multiply():

    #Define Componenets
    gc_input = siepic.GratingCoupler()
    y_splitter = siepic.YBranch()
    wg_long = siepic.Waveguide(length=150e-3)
    wg_short = siepic.Waveguide(length=150e-3)
    y_recombiner = siepic.YBranch()
    gc_output = siepic.GratingCoupler()

    # Connect Componenets
    y_splitter["pin1"].connect(gc_input["pin1"])
    y_splitter.connect(wg_long)
    y_splitter["pin3"].connect(wg_short)
    y_recombiner.multiconnect(gc_output, wg_short, wg_long)

    theoretical = None
    with Simulation() as sim:
        l = Laser(power=220e-9)
        l.powersweep(220e-9,320e-9,20)
        l.wlsweep(1500e-9,1600e-9,20)
        l.connect(gc_input)
        Detector().connect(gc_output)

        theoretical = sim.sample()
    
    print(theoretical)
    plt.plot(range(20), theoretical[0, :, 0])
    plt.plot(range(20), theoretical[:,0,0])
    plt.title("MZI")
    plt.tight_layout()
    plt.show()

def Straight():
    #Define Componenets
    gc_input = siepic.GratingCoupler()
    wg_long = siepic.Waveguide(length=150e-9)
    gc_output = siepic.GratingCoupler()

    #Connect Components
    gc_input.connect(wg_long)
    gc_output.connect(wg_long)

    theoretical = None
    with Simulation() as sim:
        l = Laser(power=220e-9, wl=1550e-9)
        l.powersweep(220e-9,320e-9,20)
        #l.wlsweep(1500e-9,1600e-9,20)
        l.connect(gc_input)
        Detector().connect(gc_output)

        theoretical = sim.sample()
        print(vars(sim))
    
    print(theoretical[:,:,0][0])
    
    
    plt.plot(range(20), theoretical[:, :, 0][0])
    plt.title("MZI")
    plt.tight_layout()
    plt.show()


def NumPyMult(arr1, arr2):
    
    return arr1 * arr2

Multiply()

# sum = Add(1,1)
# print(sum)