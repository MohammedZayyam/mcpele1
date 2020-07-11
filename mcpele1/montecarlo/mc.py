from mcpele1.montecarlo.template import *
from mcpele1.montecarlo.progress import *


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
    m_accept_tests: list = []
    m_conf_tests: list = []
    m_late_conf_tests: list =[]
    m_take_step = 0
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
    m_temperature: float =0 
    m_energy: float = 0 # compute_energy(m_coords)
    m_trial_energy: float = 0 # m_energy
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
        #self.check_input()
        #print(self.m_success, self.m_niter, self.m_nitercount, self.m_trial_coords)
        #self.take_step()
        self.m_take_step.displace(self.m_trial_coords)

        self.m_success=self.do_conf_tests(self.m_trial_coords)
        #self.m_success  #self.do_conf_test(self.m_trial_coords)
        if(self.m_success == True):
            #if configurtions test is successfull compute the trial energy
            self.m_trial_energy = self.compute_energy(self.m_trial_coords)
            #perform the acceptance test. Stop as one fails
            self.m_success = self.do_accept_tests(self.m_trial_coords, self.m_trial_energy, self.m_coords, self.m_energy)
        #do late configuration test to check the configuration is ok
        if(self.m_success):
            self.m_success = self.do_late_conf_test(self.m_trial_coords)
        """
        if (self.get_iterations_count() <= self.m_report_steps):
            #adaptive take_step
            #AdaptiveTakeStep.report(self, self.m_coords, self.m_energy, self.m_trial_coords, self.m_trial_energy, self.m_success)
        #if the step is accepted, copy the coordinates and energy
        """
        if(self.m_success):
            self.m_coords= self.m_trial_coords
            self.m_energy = self.m_trial_energy
            self.m_accept_count= 1+ self.m_accept_count
    
        #perform the actions on the new configurati
        """
        self.do_actions(self.m_coords, self.m_energy, self.m_success)
"""
        self.m_last_success = self.m_success


    def run(self, max_iter: size_t):
        self.check_input()
        progress1 = Progress(max_iter)
        while(self.m_niter< max_iter):
            self.one_iteration()
            if(self.m_print_progress):
                progress1.next(self.m_niter)
        self.m_niter = 0

    def set_temperature(self, T: float):
        self.m_temperature = T
    
    def get_temperature(self) -> float:
        return self.m_temperature
    
    def set_report_steps(self, report_steps: size_t):
        self.__m_report_steps= report_steps

    def get_report_steps(self) -> size_t:
        return self.__m_report_steps

    def add_action(self, action: list):
        self.m_actions.append(action) 

    def add_accept_test(self, accept_test: list):
        self.m_accept_tests.append(accept_test)

    def add_conf_test(self, conf_test):
        self.m_conf_tests.append(conf_test)

    def add_late_conf_test(self, conf_test: list):
        self.m_late_conf_tests.append(conf_test)

    def set_take_step(self, takestep):
        self.m_take_step = takestep
        #print("here")

    def get_take_step(self):
        return self.m_take_step

    def set_coordinates(self, coords: np.ndarray, energy: float):
        self.m_coords = coords
        self.m_energy = energy

    def get_energy(self) -> float:
        return self.m_energy

    def reset_energy(self):
        try:
            self.m_niter>0
            self.m_energy = self.compute_energy(self.m_coords)
        except:
            print("reset energy after first itteration is forbidden")
        
        

    def get_trial_energy(self) -> float:
        return self.m_trial_energy

    def get_coords(self):
        return self.m_coords

    def get_trial_coords(self):
        return self.m_trial_coords

    def get_norm_coords(self) -> float:
        return (math.sqrt((self.m_coords)^2))

    def get_naccept(self) -> size_t:
        return self.m_accept_count

    def get_nrehect(self) -> size_t:
        return self.m_nitercount -self.m_accept_count

    def get_accepted_fraction(self) -> float:
        return self.m_accept_count/self.m_nitercount

    def get_conf_rejection_fraction(self) -> float:
        return self.m_conf_reject_count/self.m_nitercount 

    def get_E_rejection_fraction(self) -> float:
        return self.m_E_reject_count/self.m_nitercount

    def get_iterations_count(self) -> size_t:
        return self.m_nitercount

    def get_neval(self) -> size_t:
        return self.m_neval

    def get_potential_ptr(self) -> Base_Potential:
        return self.m_potential

    def take_step_specified(self) -> bool:
        if(self.m_take_step == None):
            return False
        else:
            return True


    def report_steps_specified(self) -> bool:
        return self.get_report_steps > 0
    
    def check_input(self):
        #print("yes")
        try:
            self.m_take_step == None
        except:
            print("takestep not set")
        if (self.m_enable_input_warnings):
            try:
                len(self.m_conf_tests)==0 & len(self.m_late_conf_tests)==0
            except:
                print("warning: no conf tests set")
            try:
                len(self.m_actions)==0 
            except:
                print("warning: no actions set" )
            try:
                len(self.m_accept_tests)==0
            except:
                print("warning: no accept tests set")
        

    def set_print_progress(self, input: bool):
        self.m_print_progress = input

    def get_print_progress(self):
        self.set_print_progress(True)

    def get_success(self) -> bool:
        return self.m_success

    def get_last_success(self) -> bool:
        return self.m_last_success

    def get_counter(self, counters: List[size_t]) -> List[size_t]:
        counters[0] = self.m_nitercount
        counters[1] = self.m_accept_count
        counters[2] = self.m_E_reject_count
        counters[3] = self.m_conf_reject_count
        counters[4] = self.m_neval
        return counters

    def set_counters(self, counters: List[size_t]):
        self.m_nitercount = counters[0]
        self.m_accept_count = counters[1]
        self.m_E_reject_count = counters[2]
        self.c_conf_reject_count  = counters[3]
        self.m_neval = counters[4]
    """
    def get_changed_atoms(self):
        return  get_changed_atoms()

    def get_changed_coords_old(self):
        return get_changed_coords_old()


    def abort(self):
        self.m_niter = sys.maxsize
    """
    def enable_input_warnings(self):
        self.m_enable_input_warnings = True

    def disable_input_warning(self):
        self.m_enable_input_warnings = False

    def compute_energy(self, x: np.ndarray) -> float:
        self.m_neval = self.m_neval +1
        return 0    
    
    def do_conf_tests(self, x: np.ndarray) -> bool:
        try:
            len(self.m_conf_tests) == 0 
            i=0
            while(i < len(self.m_conf_tests)) :
                result: bool = self.m_conf_tests[i].conf_test(x)
                if(result == False):
                    self.m_conf_reject_count = self.m_conf_reject_count + 1
                    return False
                i= i+1
            return True
        except:
            print("no conf test specified")
        
        return True   


    def do_accept_tests(self, xtrial: np.ndarray, etrial: float, xold: np.ndarray, eold: float ) -> bool:
        try:
            len(self.m_accept_tests) == 0
            i=0
            while(i < len(self.m_accept_tests) ):
                result: bool =  self.m_accept_tests[i].test(xtrial, etrial, xold, eold, self.m_temperature) 
                if(result == False):
                    self.m_E_reject_count = self.m_E_reject_count + 1
                    return False
                i = i+1
            return True  
        except:
            print("no accept test specified")

    def do_late_conf_test(self, x: np.ndarray) -> bool:
        try:
            i=0
            len(self.m_conf_tests) == 0
            while(i < len(self.m_conf_tests)) :
                result: bool =  self.m_conf_tests[i].conf_test(x)
                if(result == False):
                    self.m_conf_reject_count = self.m_conf_reject_count + 1
                    return False
                i=i+1
            return True 
        except:
            print("no config test specified")
          
        

    def do_actions(self, x: np.ndarray, energy: float, success: bool):
        try:
            len(self.m_actions) ==0
            i=0
            while(i<len(self.m_actions)):
                self.m_actions[i].action(x, energy, success)
                i=i+1
        except:
            print("no action specified")
            


    def take_step(self):
        x= self.m_take_step
        x.displace(self.m_trial_coords)




    



    






    
    







