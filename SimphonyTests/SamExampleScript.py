"""
Simulated Photonic Circuit Capable of Adding Two Numbers
"""



import matplotlib.pyplot as plt
import numpy as np

from simphony.libraries import siepic
from simphony.simulation import Detector, Laser, Simulation

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


sum = Add(1,1)
print(sum)