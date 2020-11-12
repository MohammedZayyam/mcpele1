import unittest
from mcpele1.montecarlo.template import np
from mcpele1.montecarlo.mc import MC
from mcpele1.action.record_energy_histogram import RecordEnergyHistogram
import random
#returns the same coords everytime
class NoTakeStep:
    def displace(self, coords, mcrunner):
        mcrunner.trial_coords = coords

#return the energy as 1 everytime
class TestPotential:
    def get_energy(self, x, mcrunner):
        return random.randint(0, 100)

class TestRecordCoordsTimeSeries(unittest.TestCase):
    
    def setUp(self):
        self.bdim = 3
        self.origin: np.ndarray= [5, 6, 7]
        self.temp = 1
        self.potential = TestPotential()
        self.mc = MC(self.potential, self.origin, self.temp)
        self.nrsteps = 100

    def test_frequencies(self) :
        self.step = NoTakeStep()
        self.mc.set_take_step(self.step)
        self.Record_Hist = RecordEnergyHistogram(0, 100, 50, 0)
        self.mc.add_action(self.Record_Hist)
        self.mc.run(self.nrsteps)
        #self.coords_list = np.array(self.Record_Coords.get_timeseries())
        ans = np.asarray(self.origin*self.nrsteps).reshape(self.nrsteps, -1)
        print(self.Record_Hist.get_histogram(), len(self.Record_Hist.get_histogram()))

if __name__ == "__main__":
    unittest.main()
