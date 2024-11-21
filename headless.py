import sys
sys.path.append(sys.path[0] + "/..")

from simulation.simulation import Simulation
from simulation.dummy_agen import DummyAgen

level_file = 'data/levels/simple.txt'
with open(level_file, 'r') as file:
    lines = file.readlines()
print(lines)
sim = Simulation()
agen = DummyAgen()
sim.run(lines, agen)
print(sim.__getstate__())