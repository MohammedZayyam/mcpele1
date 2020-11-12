from mcpele1.montecarlo.mc import MC
from mcpele1.accepttest.metropolis_test import MetropolisTest
from mcpele1.action.record_energy_time_series import RecordEnergyTimeSeries
from mcpele1.action.record_energy_histogram import RecordEnergyHistogram
from mcpele1.takestep.gaussian_coords_displacement import SimpleGaussian
from mcpele1.conftest.check_spherical_container import CheckSphericalContainer
import numpy as np
import copy, sys, math
import random
import matplotlib.pyplot as plt
# python raises too many arguments error
# proper fix?
class IsingMetropolisMonteCarlo(MC):
    """ Single flip montecarlo runner for the ising model

    """
    def __init__(self, potential, initial_coords, temperature, niter, 
                 hEmin= 0, hEmax=100, hbinsize=0.01, radius=2.5, acceptance=0.5, 
                 adjustf=0.9, adjustf_niter=1e4, adjustf_navg=100, bdim=3, 
                 single=False, seeds=None):
        #calling the base class
        hEmin  =0
        print("initial", hEmin)
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
        self.accepttest = MetropolisTest(seeds)
        self.mc.take_steps = SimpleGaussian(43, 4)
        self.conftest = CheckSphericalContainer(radius, bdim)
        print("Here", self.mc.take_steps)
        # action
        self.binsize = hbinsize
        # record_energy
        print("min1", hEmin, "max1", hEmax)
        self.histogram = RecordEnergyHistogram(hEmin, hEmax, self.binsize, adjustf_niter)

        #self.action = RecordEnergyTimeSeries(record_every, stepskip)
        self.config = 0
        
        self.mc.set_take_step(self.mc.take_steps)
        self.mc.add_accept_test(self.accepttest)
        self.mc.add_action(self.histogram)
        self.mc.add_conf_test(self.conftest)    
        self.mc.set_report_steps(adjustf_niter)
        self.nsteps = niter
    def run(self):
        """ Runs the Monte Carlo simulation
        """
        #print(self.nsteps)
        #print(self.mc.trial_coords)
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

    def get_stepsize(self):
        return self.step.get_stepsize()
    
    
    

    def dump_histogram(self, fname):
        """write histogram to fname"""
        Emin, Emax = self.histogram.get_bounds_val()
        histl = self.histogram.get_histogram()
        hist = np.array(histl)
        Energies, step = np.linspace(Emin,Emax,num=len(hist),endpoint=False,retstep=True)
        assert(abs(step - self.binsize) < self.binsize/100)
        np.savetxt(fname, np.column_stack((Energies,hist)), delimiter='\t')
        mean, variance = self.histogram.get_mean_variance()
        return mean, variance
    
    def get_histogram(self):
        """returns a energy list and a histogram list"""
        Emin, Emax = self.histogram.get_bounds_val()
        histl = self.histogram.get_histogram()
        hist = np.array(histl)
        Energies, step = np.linspace(Emin,Emax,num=len(hist),endpoint=False,retstep=True)
        mean, variance = self.histogram.get_mean_variance()
        assert(abs(step - self.binsize) < self.binsize/100)
        return Energies, hist, mean, variance
        
    def show_histogram(self):
        """shows the histogram"""
        hist = self.histogram.get_histogram()
        val = [i*self.binsize for i in xrange(len(hist))]
        plt.hist(val, weights=hist,bins=len(hist))
        plt.show()