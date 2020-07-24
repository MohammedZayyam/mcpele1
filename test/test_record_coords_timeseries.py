import unittest
from mcpele1.montecarlo.template import np
from mcpele1.montecarlo.mc import MC
from mcpele1.action.record_coords_timeseries import RecordsCoordsTimeSeries

#returns the same coords everytime
class NoTakeStep:
    def displace(self, coords, mcrunner):
        mcrunner.trial_coords = coords

#return the energy as 1 everytime
class NoPotential:
    def get_energy(self, x):
        return 1

class TestRecordCoordsTimeSeries(unittest.TestCase):
    
    def setUp(self):
        self.bdim = 3
        self.origin: np.ndarray= [5, 6, 7]
        self.temp = 1
        self.potential = NoPotential()
        self.mc = MC(self.potential, self.origin, self.temp)
        self.nrsteps = 5

    def test_frequencies(self) :
        self.step = NoTakeStep()
        self.mc.set_take_step(self.step)
        self.Record_Coords = RecordsCoordsTimeSeries(self.bdim, 1, 1)
        self.mc.add_action(self.Record_Coords)
        self.mc.run(self.nrsteps)
        self.coords_list = np.array(self.Record_Coords.get_timeseries())
        ans = np.asarray(self.origin*self.nrsteps).reshape(self.nrsteps, -1)
        np.allclose(self.coords_list, ans)

if __name__ == "__main__":
    unittest.main()
