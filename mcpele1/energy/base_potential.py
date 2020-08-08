"""
Defines the Model class and methods. this is the model on which the Monte Carlo simulations are run
"""
import abc



class Model(abc.ABC):
    """ Abstract Base class for Models over which monte carlo simulations can be run
    """
    @abc.abstractmethod
    def get_energy(self, coords):
        """ returns energy can either submit new coordinates in which case the parameter set is 
            coords = present coords
            changed_coords = None
            or coords = previous coords 
            changed_coords = changed_coords
        """
        return None
