"""
Simulated MZI showing the direct relation to input power and the output of the circuit.
"""

import matplotlib.pyplot as plt
import numpy as np

from simphony.libraries import siepic
from simphony.simulation import Detector, Laser, Simulation

WAVELENGTH = 1550e-9
POWER = 220e-9

class MZI():

    def __init__(self, lengthDiff):
        
        length = 1500e-9

        #Define Componenets
        self.gc_input = siepic.GratingCoupler()
        self.y_splitter = siepic.YBranch()
        self.wg_long = siepic.Waveguide(length=length)
        self.wg_short = siepic.Waveguide(length=length - lengthDiff)
        self.y_recombiner = siepic.YBranch()
        self.gc_output = siepic.GratingCoupler()

        # Piece Together MZI
        self._connect_components()

    def _connect_components(self):

        # Connect Componenets
        self.y_splitter["pin1"].connect(self.gc_input["pin1"])
        self.y_splitter.connect(self.wg_long)
        self.y_splitter["pin3"].connect(self.wg_short)
        self.y_recombiner.multiconnect(self.gc_output, self.wg_short, self.wg_long)

def wlToFreq(wl):

    # speed of light divided by wavelength
    return 299792458.0 / wl

def freqToWL(freq):

    # speed of light divided by frequency
    return 299792458.0 / freq


def PowerSweep():

    # instantiate an MZI with no difference in length between the two waveguides
    # a difference of 0 in length will cause the input to be multiplied by 1
    mzi = MZI(lengthDiff = 0)
    # simulate a light source performing a power sweep in the input
    with Simulation() as sim:
        l = Laser(wl = WAVELENGTH)
        l.powersweep(220e-9,320e-9,20)
        l.connect(mzi.gc_input)
        Detector().connect(mzi.gc_output)

        theoretical = sim.sample()

    plt.plot(range(20), theoretical[0, :, 0])
    plt.xlabel("Time")
    plt.ylabel("MZI Output")
    plt.title("MZI")
    plt.tight_layout()
    plt.show()


def PhaseShift():

    # Record the Output of an MZI after changing it's phase shift over time
    output = []
    for diff in range(0, 15):
        mzi = MZI(lengthDiff = diff * 0.1)
        with Simulation() as sim:
            l = Laser(power=POWER, wl = WAVELENGTH)
            l.connect(mzi.gc_input)
            Detector().connect(mzi.gc_output)

            theoretical = sim.sample()
            output.append(theoretical[0,0,0])
    
    # Plot the Time Series Data
    plt.plot(output)
    plt.title("MZI")
    plt.tight_layout()
    plt.show()

PowerSweep()