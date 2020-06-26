import abc
from abc import ABC, abstractmethod
import numpy as np
from typing import List
import typing
from typing import Generic, TypeVar, NewType
import math
#from check_spherical_container import *

T = TypeVar('T')
class Action(ABC, Generic[T]):  
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


class MC(ABC):
    def __init__(self, potential: Base_Potential, coords, temperature: float):
        self.m_potential = potential
        self.m_coords = coords
        self.m_temperature = temperature

        #protected variables
    m_potential: Base_Potential = None
    m_coords: np.ndarray = None
    m_trial_coords: np.ndarray = None
    m_actions: list = None
    m_accept_tests: list = None
    m_conf_tests: list = None
    m_late_conf_tests: list = None
    m_take_step: float = None
    m_nitercount: size_t = 0
    m_accept_count: size_t = 0
    m_E_reject_count: size_t = 0
    m_conf_reject_count: size_t = 0
    m_success: bool = True
    m_last_success: bool = True
    m_print_progress: bool = False
    #public variables
    m_niter: size_t = 0
    m_neval: size_t = 0
    m_temperature: float = None
    m_energy: float = None # compute_energy(m_coords)
    m_trial_energy: float = None # m_energy
    #private variables
    m_report_steps: size_t = 0  
    m_enable_input_warnings: bool = True
    counters: List[size_t] = None
    #public methods
    def one_iteration(self):
        self.m_success = True
        self.m_niter = self.m_niter +1
        self.m_nitercount = self.m_nitercount +1
        self.m_trial_coords = m_coords
        #takestep(m_trial_coords)
        m_success = do_conf_test(m_trial_coords)
        if(m_success):
            #if configurtions test is successfull compute the trial energy
            m_trial_energy = compute_energy(m_trial_energy)
            #perform the acceptance test. Stop as one fails
            m_success = do_accept_tests(m_trial_coords, m_trial_energy, m_coords, m_energy)
        #do late configuration test to check the configuration is ok
        if(m_success):
            m_success = do_late_conf_test(m_trial_coords)
        
        if (get_iterations_count() <= m_report_steps):
            report(m_coords, m_energy, m_trial_coords, m_trial_energy, m_success, this)

        #if the step is accepted, copy the coordinates and energy
        if (m_success):
            m_coords.assign(m_trial_coords)
            m_energy = m_trial_energy
            m_accept_count= 1+ m_accept_count
    
        #perform the actions on the new configuration
        self.do_actions(m_coords, m_energy, m_success)

        self.m_last_success = m_success
}


    @abc.abstractmethod 
    def run(self, max_iter: size_t):
        return None

    @abc.abstractmethod 
    def set_temperature(self, T: float):
        self.m_temperature = T
    
    @abc.abstractmethod 
    def get_temperature(self) -> float:
        return self.m_temperature
    
    @abc.abstractmethod 
    def set_report_steps(self, report_steps: size_t):
        self.__m_report_steps= report_steps

    @abc.abstractmethod 
    def get_report_steps(self) -> size_t:
        return self.__m_report_steps

    @abc.abstractmethod 
    def add_action(self, action: list):
        self._m_actions.append(action) 

    @abc.abstractmethod  
    def add_accept_test(self, accept_test: list):
        self._m_accept_tests.append(accept_test)

    @abc.abstractmethod 
    def add_conf_test(self, conf_test: list):
        self._m_conf_tests.append(conf_test)

    @abc.abstractmethod 
    def add_late_conf_test(self, conf_test: list):
        self._m_late_conf_tests.append(conf_test)

    @abc.abstractmethod 
    def set_take_step(self, takestep: float):
        self._m_take_step = takestep

    @abc.abstractmethod 
    def get_take_step(self)-> float:
        return self._m_take_step

    @abc.abstractmethod 
    def set_coordinates(self, coords: np.ndarray, energy: float):
        return None

    @abc.abstractmethod 
    def get_energy(self) -> float:
        return self.m_energy

    @abc.abstractmethod 
    def reset_energy(self):
        return None

    @abc.abstractmethod 
    def get_trial_energy(self) -> float:
        return self.m_trial_energy

    @abc.abstractmethod 
    def get_coords(self):
        return self._m_coords

    @abc.abstractmethod 
    def get_trial_coords(self):
        return self._m_trial_coords

    @abc.abstractmethod 
    def get_norm_coords(self) -> float:
        return (math.sqrt((self._m_coords)^2))
    
    @abc.abstractmethod 
    def get_naccept(self) -> size_t:
        return m_accept_count

    @abc.abstractmethod 
    def get_nrehect(self) -> size_t:
        return m_nitercount -m_accept_count
    
    @abc.abstractmethod 
    def get_accepted_fraction(self) -> float:
        return m_accept_count/m_nitercount

    @abc.abstractmethod
    def get_conf_rejection_fraction(self) -> float:
        return m_conf_reject_count/m_nitercount 

    @abc.abstractmethod
    def get_E_rejection_fraction(self) -> float:
        return m_E_reject_count/m_nitercount

    @abc.abstractclassmethod
    def get_iterations_count(self) -> size_t:
        return m_nitercount
    
    @abc.abstractclassmethod
    def get_neval(self) -> size_t:
        return m_neval

    @abc.abstractclassmethod
    def get_potential_ptr(self) -> Base_Potential:
        return m_potential
    
    @abc.abstractclassmethod
    def take_step_specified(self) -> bool:
        return m_take_step != None

    @abc.abstractclassmethod
    def report_steps_specified(self) -> bool:
        return get_report_steps > 0
    
    @abc.abstractclassmethod
    def check_input(self):
        return None
    
    @abc.abstractclassmethod
    def set_print_progress(self, input: bool):
        m_print_progress = input

    @abc.abstractclassmethod
    def get_print_progress(self):
        set_print_progress(true)
    
    @abc.abstractclassmethod
    def get_success(self) -> bool:
        return m_success

    @abc.abstractclassmethod
    def get_last_success(self) -> bool:
        return m_get_last_success
    
    @abc.abstractclassmethod
    def get_counter(self, counters: List[size_t]) -> List[size_t]:
        counters[0] = m_nitercount
        counters[1] = m_accept_count
        counters[2] = m_E_reject_count
        counters[3] = m_conf_reject_count
        counters[4] = m_neval
        return counters

    @abc.abstractclassmethod
    def set_counters(self, counters: List[size_t]):
        m_nitercount = counters[0]
        m_accept_count = counter[1]
        m_E_reject_count = counters[2]
        c_conf_reject_count  = counters[3]
        m_neval = counters[4]

    @abc.abstractclassmethod
    def get_changed_atoms(self):
        return  TakeStep.get_changed_atoms()

    @abc.abstractclassmethod
    def get_changed_coords_old(self):
        return TakeStep.get_changed_coords_old()
    #not sure if we need these methods in python
    @abc.abstractclassmethod
    def abort(self):
        m_niter = sys.maxsize

    @abc.abstractclassmethod
    def enable_input_warnings(self):
        m_enable_input_warnings = True
    
    @abc.abstractclassmethod
    def disable_input_warning(self):
        m_enable_input_warnings = False
    #no such thing as protected methods in python
    # it is possible to duplicate. but is it needed?
    @abc.abstractclassmethod
    def compute_energy(self, x: np.ndarray) -> float:
        m_neval = m_neval +1
        return None
    
    @abc.abstractclassmethod
    def do_conf_tests(self, x: np.ndarray) -> bool:
        return None

    @abc.abstractclassmethod
    def do_accept_tests(self, xtrial: np.ndarray, etrial: float, xold: np.ndarray, eold: float ) -> bool:
        return None

    @abc.abstractclassmethod
    def do_late_conf_test(self, x: np.ndarray) -> bool:
        return None

    def do_actions(self, x: np.ndarray, energy: float, success: bool):
        return None
    
    @abc.abstractclassmethod
    def take_steps(self):
        return None


    



    






    
    







