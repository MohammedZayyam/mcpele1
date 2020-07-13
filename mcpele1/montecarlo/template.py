import abc
from abc import ABC
from typing import NewType
from typing import List
import numpy as np
import math 
import time
import datetime


class Action(ABC):
    @abc.abstractmethod
    def action(self, coords, energy: float, accepted: bool, MC_method):
        return None

class AcceptTest(ABC):
    @abc.abstractmethod
    def test(self,  trial_energy, old_energy, temperature) -> bool:
        return None

class ConfTest(ABC):
    @abc.abstractmethod
    def conf_test(self, coords):
        return None


class TakeStep(ABC):#define all the function
    @abc.abstractmethod 
    def displace(self, coords):
        return None
    

    def report(self, old_coords: np.ndarray, old_energy: float, new_coords: np.ndarray, new_energy: float,
    success: bool):
        return None

    def increase_acceptance(self):
        return None
    

    def decrease_acceptance(self):
        return None
    
    def get_changed_coords_old(self) -> np.ndarray:
        return np.ndarray

#dataa types
size_t = NewType('size_t', int)
#function(Log likilyh)
Base_Potential = NewType('Base_Potential', float)
#from check_spherical_container import *