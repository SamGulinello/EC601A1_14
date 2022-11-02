# An attempt at creating a MZI
# LARGLY TAKEN FROM MZI.py IN THE SIMPHONY EXAMPLES


import matplotlib.pyplot as plt
import numpy as np

from simphony.libraries import siepic
from simphony.simulation import Detector, Laser, Simulation

# define compenents
gc_input = siepic.GratingCoupler()
y_splitter = siepic.YBranch()
wg_long = siepic.Waveguide(length=150e-6)
wg_short = siepic.Waveguide(length=50e-6)
y_recombiner = siepic.YBranch()
gc_output = siepic.GratingCoupler()

# connect components
y_splitter.multiconnect(gc_input, wg_long, wg_short)
y_recombiner.multiconnect(gc_output,wg_long, wg_short)

theoretical = None
with Simulation() as sim:
    l = Laser(power=20e-3)
    l.wlsweep(1500e-9, 1600e-9)
    l.connect(gc_input)
    Detector().connect(gc_output)

    theoretical = sim.sample()

plt.plot(sim.freqs, theoretical[:, 0, 0])
plt.title("MZI")
plt.tight_layout()
plt.show()