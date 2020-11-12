from mcpele1.montecarlo.mc import MC
from mcpele1.accepttest.metropolis_test import MetropolisTest
from mcpele1.action.record_energy_time_series import RecordEnergyTimeSeries
from mcpele1.takestep.gaussian_coords_displacement import SimpleGaussian
import numpy as np
import copy, sys, math
import random
# python raises too many arguments error
# proper fix?
class IsingMetropolisMonteCarlo(MC):
    """ Single flip montecarlo runner for the ising model

    """
    def __init__(self, potential, initial_coords, temperature, N,
                 record_every=10, stepskip=1000, nsteps=1e5):
        #calling the base class
        super(IsingMetropolisMonteCarlo, self).__init__(potential, initial_coords, temperature)
        random.seed(10)
        #initial_coords = random.randint(2,
        #                                size=(N, N),
        #                                dtype=bool)  # we're starting
                                                     # with a random initial configuration

        # define the monte carlo runner with
        # the potential function , initial coordinates and temperature
        #ising_model = IsingModel(N, N)
        self.mc = MC(potential, initial_coords, temperature)
        # add the step type
        #self.take_step = IsingFlip(10, N, N)
        seeds = range(np.iinfo(np.int32).max)
        # accept test
        self.accept_test = MetropolisTest(seeds)
        self.take_steps = SimpleGaussian(43, 4)
        # action
        # record_energy
        self.action = RecordEnergyTimeSeries(record_every, stepskip)
        self.config = 0
        print(initial_coords)
        self.mc.set_take_step(self.take_step)
        self.mc.add_accept_test(self.accept_test)
        self.mc.add_action(self.action)
        self.nsteps = nsteps
    def run(self):
        """ Runs the Monte Carlo simulation
        """
        print(self.nsteps)
        self.mc.run(self.nsteps)

    def get_et_series(self):
        """ gets the array of energies at every iteration
        """
        return np.array(self.action.get_energy_time_series())
    
    
    def set_control(self, c):
        """
        sets the temperature or whichever control parameter that takes
        the role of the temperature, such as the stifness of an harmonic
        """
        self.temperature = c
