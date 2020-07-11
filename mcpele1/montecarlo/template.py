import abc
from abc import ABC
from typing import NewType
from typing import List
import numpy as np
import math 
import time
import datetime


class Action(ABC):  
    def action(self, coords: np.ndarray, energy: float, accepted: bool):
        return None

class AcceptTest(ABC):
    def test(self,  trialcoords: np.ndarray, energy: float, old_coords: np.ndarray, old_energy: float, temperature: float) -> bool:
        return None

class ConfTest(ABC):
    @abc.abstractmethod
    def conf_test(self, trial_coords: np.ndarray):
        return None


class TakeStep(ABC):#define all the function
    @abc.abstractmethod 
    def displace(self, coords: np.ndarray):
        return None
    
    @abc.abstractmethod 
    def report(self, old_coords: np.ndarray, old_energy: float, new_coords: np.ndarray, new_energy: float,
    success: bool):
        return None

    @abc.abstractmethod   
    def increase_acceptance(self):
        return None
    
    @abc.abstractmethod 
    def decrease_acceptance(self):
        return None

    @abc.abstractmethod 
    def get_changed_atoms(self) -> List[int]:
        return List[int]
    
    @abc.abstractmethod 
    def get_changed_coords_old(self) -> np.ndarray:
        return np.ndarray

#dataa types
size_t = NewType('size_t', int)
#function(Log likilyh)
Base_Potential = NewType('Base_Potential', float)
#from check_spherical_container import *