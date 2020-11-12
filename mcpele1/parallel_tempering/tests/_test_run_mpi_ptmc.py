from __future__ import division
import numpy as np
import argparse
from mcpele1.montecarlo.mcrunner import IsingMetropolisMonteCarlo
from mcpele1.parallel_tempering import MPI_PT_RLhandshake
from mcpele1.takestep.gaussian_coords_displacement import SimpleGaussian
class NoTakeStep:
    def displace(self, coords, mcrunner):
        print("yes")
        mcrunner.trial_coords = coords

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
    
    def get_energy(self, x, mcrunner):
        self.get_distance(x)
        return 0.5*self.k*np.dot(self.distance, self.distance)


        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="do nested sampling on a Lennard Jones cluster")
    parser.add_argument("base_directory", type=str, help="directory in which to save results")
    parser.add_argument("-K", "--nreplicas", type=int, help="number of replicas", default=300)
    args = parser.parse_args()

    natoms = 4
    bdim = 3
    k=1
    origin = np.zeros(natoms * bdim)
    potential = Harmonic(origin, k, bdim)
    path = args.base_directory
    
    #Parallel Tempering
    temperature = 1.0
    stepsize = 1
    niter = 1e4
    mcrunner = IsingMetropolisMonteCarlo(potential, origin, temperature, stepsize, niter)
    mcrunner.set_take_step(SimpleGaussian(42, 3))
    print("He1re", mcrunner.take_steps)
    ptrunner = MPI_PT_RLhandshake(mcrunner, 0.2, 1.6, max_ptiter=501, pfreq=10, base_directory=path,  suppress_histogram=False)
    ptrunner.run()
            
            