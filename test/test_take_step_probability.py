#from __future__ import division
import numpy as np
#from pele.potentials import Harmonic
from mcpele1.montecarlo.mc import MC
from mcpele1.takestep.take_step_probability import TakeStepProbability
from mcpele1.takestep.take_step_pattern import TakeStepPattern
from mcpele1.takestep.gaussian_coords_displacement import GaussianCoordsDisplacement
#from mcpele.monte_carlo import RandomCoordsDisplacement, MetropolisTest
#from mcpele.monte_carlo import RecordEnergyHistogram
import unittest
class Harmonic:
    distance:np.ndarray = []
    origin = []
    k =0
    ndim = 0
    nparticels = 0
    def __init__(self, origin, k, bdim):
        self.ndim = bdim
        self.distance = np.asarray(origin)
        self.origin = origin
        self.k = k
        self.nparticels = len(origin)/bdim
    
    def get_distance(self, x):
        for i in range(0, len(x)):
            self.distance[i] = x[i] - self.origin[i]
    
    def get_energy(self, x):
        self.get_distance(x)
        return 0.5*self.k*np.dot(self.distance, self.distance)


class TestTakeStepProbability(unittest.TestCase):
    
    def setUp(self):
        self.ndim = 42
        self.k = 100
        self.bdim = 2
        self.origin = np.zeros(self.ndim)
        self.potential = Harmonic(self.origin, self.k, self.bdim)
        self.potential_pattern = Harmonic(self.origin, self.k, self.bdim)
        self.temp = 1
        self.nr_steps = 10000
        self.mc = MC(self.potential, self.origin, self.temp)
        self.mc_pattern = MC(self.potential_pattern, self.origin, self.temp)
        
    def test_frequencies(self):
        self.tsA = GaussianCoordsDisplacement(42, 1, self.ndim)
        self.tsA_pattern = GaussianCoordsDisplacement(42, 1, self.ndim)
        self.tsB = GaussianCoordsDisplacement(44, 2, self.ndim)
        self.tsB_pattern = GaussianCoordsDisplacement(44, 2, self.ndim)
        self.step = TakeStepProbability(42)
        self.step.add_step(self.tsA, 1)
        self.step.add_step(self.tsB, 3)
        self.step_pattern = TakeStepPattern()
        self.step_pattern.add_step(self.tsA_pattern, 1)
        self.step_pattern.add_step(self.tsB_pattern, 3)
        freqA = 1 / (1 + 3)
        freqB = 1 - freqA
        self.mc.set_take_step(self.step)
        self.mc.run(self.nr_steps)
        self.mc_pattern.set_take_step(self.step_pattern)
        self.mc_pattern.run(self.nr_steps)
        print(self.tsA.get_count(), self.tsB.get_count())
        self.assertAlmostEqual(freqA, self.tsA.get_count() / self.nr_steps, delta=1e-2)
        self.assertAlmostEqual(freqB, self.tsB.get_count() / self.nr_steps, delta=1e-2)
        self.assertAlmostEqual(freqA, self.tsA_pattern.get_count() / self.nr_steps, delta=1e-2)
        self.assertAlmostEqual(freqB, self.tsB_pattern.get_count() / self.nr_steps, delta=1e-2)
"""        
class TestTakeStepProbabilityHarmoinc(unittest.TestCase):
    
    def setUp(self):
        self.box_dimension = 3
        self.nr_particles = 10
        self.k = 42
        self.nr_dof = self.box_dimension * self.nr_particles
        self.origin = np.zeros(self.nr_dof)
        self.potential = Harmonic(self.origin, self.k, self.bdim)
        self.temp = 1
        self.nr_steps = 6e4
        self.mc = MC(self.potential, self.origin, self.temp, self.nr_steps)
        self.take_step_A = RandomCoordsDisplacement(42, 4, single=True, nparticles=self.nr_particles, bdim=self.box_dimension, min_acc_ratio=0.2, max_acc_ratio=0.2)
        self.take_step_B = RandomCoordsDisplacement(44, 0.1, single=True, nparticles=self.nr_particles, bdim=self.box_dimension, min_acc_ratio=0.2, max_acc_ratio=0.2)
        self.step = TakeStepProbabilities(46)
        self.weight_A = 22
        self.weight_B = 78
        self.step.add_step(self.take_step_A, self.weight_A)
        self.step.add_step(self.take_step_B, self.weight_B)
        self.mc.set_takestep(self.step)
        self.frequency_step_A = self.weight_A / (self.weight_A + self.weight_B)
        self.frequency_step_B = self.weight_B / (self.weight_A + self.weight_B)
        self.metropolis = MetropolisTest(50)
        self.mc.add_accept_test(self.metropolis)
        self.hist_min = 0
        self.hist_max = 1e4
        self.eq_steps = self.nr_steps / 2
        self.mc.set_report_steps(self.eq_steps)
        self.measure_energy = RecordEnergyHistogram(self.hist_min, self.hist_max, (self.hist_max - self.hist_min)/14, self.eq_steps)
        self.mc.add_action(self.measure_energy)
        self.true_energy = self.box_dimension * (self.nr_particles - 1) / 2
    
    def test_basic_harmonic(self):
        self.mc.run()
        self.assertAlmostEqual(self.frequency_step_A, self.take_step_A.get_count() / self.nr_steps, delta=1e-2)
        self.assertAlmostEqual(self.frequency_step_B, self.take_step_B.get_count() / self.nr_steps, delta=1e-2)
        self.assertAlmostEqual(self.take_step_A.get_stepsize(), self.take_step_B.get_stepsize(), delta=1e-2)
        mean_energy, var_energy = self.measure_energy.get_mean_variance()
        self.assertAlmostEqual(mean_energy, self.true_energy, delta=3e-1)
"""   
if __name__ == "__main__":
    unittest.main()
