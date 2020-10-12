"""
Defines the Model class and methods. this is the model on which the Monte Carlo simulations are run
"""
import abc



class BasePotential(abc.ABC):
    """ Abstract Base class for Models over which monte carlo simulations can be run
    """
    
    use_change_in_energy: bool = False
    """
    flag to decide if changed_coordinated from Take_Steps should
    be used to calculate the potential
    """

    @abc.abstractmethod
    def get_energy(self, coords, mcrunner):
        """ returns energy can either submit new coordinates in which case the parameter set is 
            coords = present coords
            changed_coords = None
            or coords = previous coords 
            changed_coords = changed_coords
        """
    
    def set_changed_coords_flag(self, input:bool):
        self.use_change_in_energy = input
