from mcpele1.montecarlo.template import TakeStep, np, abc, ABC
import random

class RandomCoordsDisplacement(TakeStep):
    stepsize: float = 0
    count: int = 0
    seed: int = 0
    

    @abc.abstractmethod
    def displace(self):
        pass

    def get_seed(self):
        return self.seed
    
    def set_generator_seed(self, input):
        self.seed = input
    
    def expected_mean(self):
        return 0

    def get_stepsize(self):
        return self.stepsize
    
    def expected_variance(self, ss):
        return (ss*ss/12)
    
    def increase_acceptance(self, factor):
        self.stepsize *= factor
    
    def decreade_acceptance(self, factor):
        self.stepsize /= factor
    
    def get_count(self):
        return self.count
    
    def set_count(self, input):
        self.count = input

class RandomCoordsDisplacementAll(RandomCoordsDisplacement):
    changed_atoms: np.ndarray = []
    changed_coords_old: np.ndarray = []

    def __init__(self, rseed, stepsize, nparticles, ndim):
        self.seed = rseed
        self.stepsize = stepsize
        self.count = 0
        self.changed_atoms = nparticles
        self.changed_coords_old = nparticles*ndim
        random.seed(rseed)

    def displace(coords, mcrunner):
        i =0
        for i in range(0, len(self.changed_atoms)):
            changed_atoms[i] =i
        if(len(self.changed_coords_old != 0)):
            self.changed_coords_old = coords
        j = 0
        for j in range(0, len(coords)):
            rand = random.uniform(0,1)
            coords[j] += (0.5 - rand)*self.stepsize
        count+=1
        mcrunner.trial_coords = coords

    def get_changed_atoms(self):
        return self.changed_atoms

    def get_changed_coords_cold(self):
        return self.get_changed_coords_cold

class RandomCoordsDisplacementSingle(RandomCoordsDisplacement):
    particles: int =0
    ndim: int = 0
    changed_atoms: np.ndarray = []
    changed_coords_old: np.ndarray = []

    def displace(self, coords, mcrunner):
        self.changed_atoms[0] = random.randint(0, self.particles - 1)
        offset = self.changed_atoms[0] *self.ndim
        i = 0
        for i in range(0, ndim):
            rand = random.randint(0, self.particles - 1)
            self.changed_coords_old[i] = coords[offset + i]
            coords[offset + i] += (0.5 - rand) * self.stepsize
        mcrunner.trial_coords = coords
        count += 1

    def get_rand_particle(self):
        return self.changed_atoms[0]

    def get_changed_atoms(self):
        return self.changed_atoms

    def get_changed_coords_cold(self):
        return self.get_changed_coords_old

    

    
