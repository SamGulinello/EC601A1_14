"""
Simulated Photonic Circuit Capable of Adding Two Numbers
There is still a rounding error from power loss, but now there is a graph of what's happening

*If you change either of the values for num1 or num2 to 0 it flips the y-branch and splits the value of the laser in half. Will fix this tomorrow*
"""


import matplotlib.pyplot as plt
import numpy as np
import math

from simphony.libraries import siepic
from simphony.simulation import Detector, Laser, Simulation
from simphony.simulators import SweepSimulator

gc_input = siepic.GratingCoupler()
gc_output = siepic.GratingCoupler()


def Add(num1, num2):
    y_recombiner = siepic.YBranch()

    with Simulation() as sim:
        l1 = Laser(coupling_loss=0, power=num1)
        l2 = Laser(coupling_loss=0, power=(num2 + (4e-10)))

        Detector().connect(y_recombiner)
        l1.connect(y_recombiner)
        l2.connect(y_recombiner)

        theoretical = sim.sample()

    return theoretical[0, 0, 0]


sum = Add(15, 15)
print(sum)

simulator = SweepSimulator(1500e-9, 1600e-9)
simulator.multiconnect(gc_input, gc_output)

f = simulator.simulate()
print(f)
plt.plot(f)
plt.title("Adding two numbers")
plt.tight_layout()
plt.show()

