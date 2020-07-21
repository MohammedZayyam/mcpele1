"""
This example computes the numerical value of Pi by Monte Carlo.
Points are sampled uniformly at random from an n-dimensional cube of
side length 2R. By measuring the fraction of points contained within
a ball of radius R contained in the cube, we determine Pi.
"""
import numpy as np
import copy
from scipy.special import gamma
from mcpele1.montecarlo.mc import MC
from mcpele1.takestep.uniform_rectangle_sampling import UniformRectangularSampling
from mcpele1.conftest.check_spherical_container_config import CheckSphericalContainerConfig

def volume_nball(radius, n):
    return np.power(np.pi, n / 2) * np.power(radius, n) / gamma(n / 2 + 1)

def get_pi(accepted_fraction, ndim):
    return np.power(2 ** ndim * accepted_fraction * gamma(ndim / 2 + 1), 2 / ndim)
"""
class MC(MC):
    def set_temperature(self, temp):
        self.set_temperature(temp)
"""


class nullpotential():
    def get_energy(self):
        return 0


class ComputePi(object):
    def __init__(self, ndim=2, nsamples=1e4):
        #
        self.ndim = ndim
        self.nsamples = nsamples
        #
        self.radius = 44
        self.potential = nullpotential #NullPotential()
        self.mc = MC(self.potential, np.ones(ndim), 1)
        self.step = UniformRectangularSampling(42, self.radius)
        self.mc.set_take_step(self.step)
        self.mc.set_report_steps(0)
        self.conftest_check_spherical_container = CheckSphericalContainerConfig(self.radius)
        #no problem till here
        self.mc.add_conf_test(self.conftest_check_spherical_container)
        self.mc.set_print_progress(False)
        self.mc.run(nsamples)
        self.p = self.mc.get_accepted_fraction()
        self.pi = get_pi(self.p, self.ndim)
        
if __name__ == "__main__":
    nsamples = 10000
    ndim_ = []
    res = []
    for ndim in range(2, 5):
        print("computing pi in {} dimensions".format(ndim))
        c = ComputePi(ndim=ndim, nsamples=nsamples)
        res.append(c.pi)
        ndim_.append(ndim)
    for (i, p) in zip(ndim_, res):
        print("dimension", i)
        print("pi", p)
        print("pi / np.pi", p / np.pi)
