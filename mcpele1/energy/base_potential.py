"""
Defines the Model class and methods. this is the model on which the Monte Carlo simulations are run
"""
import abc



class Base_Potential(abc.ABC):
    """ Abstract Base class for Models over which monte carlo simulations can be run
    """
    
    use_changed_coords: bool = False
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
        TakeStep=mcrunner.take_step
        changed_coords= TakeStep.get_changed_coords()
        
