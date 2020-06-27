from template import *
from check_spherical_container import *
from metropolis_test import *
#from check_spherical_container import *

class MC(ABC):
    def __init__(self, potential: Base_Potential, coords, temperature: float):
        self.m_potential = potential
        self.m_coords = coords
        self.m_temperature = temperature

        #protected variables
    m_potential: Base_Potential = None
    m_coords= None
    m_trial_coords= None
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
        self.m_trial_coords = self.m_coords
        #takestep(m_trial_coords)

        self.m_success=self.do_conf_tests(self.m_trial_coords)
        #self.m_success  #self.do_conf_test(self.m_trial_coords)
        if(self.m_success == True):
            #if configurtions test is successfull compute the trial energy
            self.m_trial_energym_trial_energy = self.compute_energy(self.m_trial_energy)
            #perform the acceptance test. Stop as one fails
            self.m_success = self.do_accept_tests(self.m_trial_coords, self.m_trial_energy, self.m_coords, self.m_energy)
        #do late configuration test to check the configuration is ok
        if(self.m_success):
            self.m_success = self.do_late_conf_test(self.m_trial_coords)
        
        if (self.get_iterations_count() <= self.m_report_steps):
            mt.report(self.m_coords, self.m_energy, self.m_trial_coords, self.m_trial_energy, self.m_success)

        #if the step is accepted, copy the coordinates and energy
        if (self.m_success):
            self.m_coords.assign(self.m_trial_coords)
            self.m_energy = self.m_trial_energy
            self.m_accept_count= 1+ self.m_accept_count
    
        #perform the actions on the new configuration
        self.do_actions(self.m_coords, self.m_energy, self.m_success)

        self.m_last_success = self.m_success


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
        self.m_actions.append(action) 

    @abc.abstractmethod  
    def add_accept_test(self, accept_test: list):
        self.m_accept_tests.append(accept_test)

    @abc.abstractmethod 
    def add_conf_test(self, conf_test: list):
        self.m_conf_tests.append(conf_test)

    @abc.abstractmethod 
    def add_late_conf_test(self, conf_test: list):
        self.m_late_conf_tests.append(conf_test)

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
        return self.m_coords

    @abc.abstractmethod 
    def get_trial_coords(self):
        return self.m_trial_coords

    @abc.abstractmethod 
    def get_norm_coords(self) -> float:
        return (math.sqrt((self.m_coords)^2))
    
    @abc.abstractmethod 
    def get_naccept(self) -> size_t:
        return self.m_accept_count

    @abc.abstractmethod 
    def get_nrehect(self) -> size_t:
        return self.m_nitercount -self.m_accept_count
    
    @abc.abstractmethod 
    def get_accepted_fraction(self) -> float:
        return self.m_accept_count/self.m_nitercount

    @abc.abstractmethod
    def get_conf_rejection_fraction(self) -> float:
        return self.m_conf_reject_count/self.m_nitercount 

    @abc.abstractmethod
    def get_E_rejection_fraction(self) -> float:
        return self.m_E_reject_count/self.m_nitercount

    @staticmethod
    def get_iterations_count(self) -> size_t:
        return self.m_nitercount
    
    @abc.abstractclassmethod
    def get_neval(self) -> size_t:
        return self.m_neval

    @abc.abstractclassmethod
    def get_potential_ptr(self) -> Base_Potential:
        return self.m_potential
    
    @abc.abstractclassmethod
    def take_step_specified(self) -> bool:
        return self.m_take_step != None

    @abc.abstractclassmethod
    def report_steps_specified(self) -> bool:
        return self.get_report_steps > 0
    
    @abc.abstractclassmethod
    def check_input(self):
        return None
    
    @abc.abstractclassmethod
    def set_print_progress(self, input: bool):
        self.m_print_progress = input

    @abc.abstractclassmethod
    def get_print_progress(self):
        self.set_print_progress(True)
    
    @abc.abstractclassmethod
    def get_success(self) -> bool:
        return self.m_success

    @abc.abstractclassmethod
    def get_last_success(self) -> bool:
        return self.m_last_success
    
    @abc.abstractclassmethod
    def get_counter(self, counters: List[size_t]) -> List[size_t]:
        counters[0] = self.m_nitercount
        counters[1] = self.m_accept_count
        counters[2] = self.m_E_reject_count
        counters[3] = self.m_conf_reject_count
        counters[4] = self.m_neval
        return counters

    @abc.abstractclassmethod
    def set_counters(self, counters: List[size_t]):
        self.m_nitercount = counters[0]
        self.m_accept_count = counters[1]
        self.m_E_reject_count = counters[2]
        self.c_conf_reject_count  = counters[3]
        self.m_neval = counters[4]

    @abc.abstractclassmethod
    def get_changed_atoms(self):
        return  mt.get_changed_atoms()

    @abc.abstractclassmethod
    def get_changed_coords_old(self):
        return mt.get_changed_coords_old()
    #not sure if we need these methods in python
    @abc.abstractclassmethod
    def abort(self):
        self.m_niter = sys.maxsize

    @abc.abstractclassmethod
    def enable_input_warnings(self):
        self.m_enable_input_warnings = True
    
    @abc.abstractclassmethod
    def disable_input_warning(self):
        self.m_enable_input_warnings = False
    #no such thing as protected methods in python
    # it is possible to duplicate. but is it needed?
    @abc.abstractclassmethod
    def compute_energy(self, x: np.ndarray) -> float:
        self.m_neval = self.m_neval +1
        return None
    
    def do_conf_tests(self, x: np.ndarray) -> bool:
        if (len(self.m_conf_tests) == 0 ):
            print("no conf test specified")
        i=0
        while(i < len(self.m_conf_tests)) :
            result: bool =  CheckSphericalContainer.conf_test(x)
            if(result == False):
                self.m_conf_reject_count = self.m_conf_reject_count + 1
                return False
            i= i+1
        return True   


    def do_accept_tests(self, xtrial: np.ndarray, etrial: float, xold: np.ndarray, eold: float ) -> bool:
        i=0
        while(i < len(self.m_accept_tests) ):
            result: bool =  MetropolisTest.test(xtrial, etrial, xold, eold, self.m_temperature) 
            if(result == False):
                self.m_E_reject_count = self.m_E_reject_count + 1
                return False
            i = i+1
        return True  

    def do_late_conf_test(self, x: np.ndarray) -> bool:
        if (len(self.m_conf_tests) == 0 ):
            print("no conf test specified")
        i=0
        while(i < len(self.m_conf_tests)) :
            result: bool =  CheckSphericalContainer.conf_test(x)
            if(result == False):
                self.m_conf_reject_count = self.m_conf_reject_count + 1
                return False
            i=i+1
        return True 

    def do_actions(self, x: np.ndarray, energy: float, success: bool):
        i=0
        while(i<len.(self.m_actions)):
            action(x, energy, success)
            i=i+1
    
    @abc.abstractclassmethod
    def take_steps(self):
        return None




    



    






    
    







