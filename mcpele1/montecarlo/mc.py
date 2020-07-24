from mcpele1.montecarlo.template import ABC, np
from mcpele1.montecarlo.progress import Progress
import copy, sys, math

class MC(ABC):
    """Abstract base class for MC runners, all MC runners should derive from this base class.

    .. note :: Complex or Additional feature to an MC class can be added on easily
                using this MC base class

    .. warning :: install all requirements for python3 before implementation

    Parameters
    ----------
    potential : class
        the potential (or cost function) return energy, gradient and hessian
        information given a set of coordinates
        potential must be a class and have a method named get_energy()
    coords : numpy.array
        these are the initial coordinates for the system
    temperature : float
        temperature or equivalent control parameter

    Attributes
    ----------
    potential : class
        the potential (or cost function) return energy, gradient and hessian
        information given a set of coordinates
    start_coords : numpy.array
        initial coordinates array
    temperature : float
        temperature or equivalent control parameter
    niter : int
        number of Monte Carlo iteration to perform
    ndim : int
        number of degrees of freedom (which is ``len(coords)``)
    res : :class:`Result <pele:pele.optimize.Result>` container
        dictionary-like container for the results
    """
    def __init__(self, potential_function, coords, temperature):
        self.pot_func = potential_function
        self.coords = coords
        self.temperature = temperature
        self.trial_coords= coords
        self.actions: list = []
        self.accept_tests: list = []
        self.conf_test: list = []
        self.late_conf_test: list =[]
        self.take_steps = 0
        self.nitercount = 0
        self.accept_count = 0
        self.E_reject_count= 0
        self.conf_reject_count = 0
        self.success: bool = True   
        self.last_success: bool = True
        self.niter = 0
        self.neval = 0
        self.energy: float = 0 
        self.trail_energy: float = 0 
        self.report_steps = 0  
        self.enable_input_warning = True
        self.counters = []
        self.print_progress = False
    
    def one_iteration(self):
        """perform a single iteration of the MC loop
        1. starts with displacing the coords with :class 'TakeStep'
        2. Perform configuration test with coords from step.1
        3.a. if one of the conf_test fail the iteration is a fail
        3.b. If all the configuration test pass successfullt,compute the 
           energy of the coords, 
        4.a. Perform all accept tests and late configuration test
        4.b. If one of the tests in the last step fail the iteration is a fail
        5. Perform all the actions mentioned
         """
        success = True
        self.niter = self.niter +1
        self.nitercount = self.nitercount +1
        self.take_step()  
        success = self.do_conf_tests(self.trial_coords)
        if success:
            self.trail_energy = self.compute_energy(self.trial_coords)
            success = self.do_accept_tests(self.trial_coords, self.trail_energy, self.coords, self.energy)
        if success:
            success = self.do_late_conf_test(self.trial_coords)
        # if the step is accepted, copy the coordinates and energy
        if success:
            self.coords = self.trial_coords
            self.energy = self.trail_energy
            self.accept_count+=1
        #perform the actions on the new configurations
        self.do_actions(self.coords, self.energy, success)
        self.last_success = success

    def run(self, max_iter):
        """perform ``niter`` iterations of the MC loop"""
        self.check_input()
        progress1 = Progress(max_iter)
        while(self.niter< max_iter):
            self.one_iteration()
            if(self.print_progress):
                progress1.next(self.niter)
        self.niter = 0

    def set_temperature(self, T: float):
        """set the temperature

        Parameters
        ----------
        T : double
            temperature or equivalent control parameter
        """
        self.temperature = T
    
    def get_temperature(self) -> float:
        """get the temperature

        Returns
        -------
        T : double
            temperature or equivalent control parameter
        """
        return self.temperature
    
    def set_report_steps(self, report_steps):
        """ set number of steps for which the MC loop should report to :class`TakeStep`

        Parameters
        ----------
        steps : int
            number of steps out of `niter_count`, which is the total count of the MCrunner
            which accumulates the number of iterations for many :func:`run` calls
        """
        self.report_steps= report_steps

    def get_report_steps(self):
        """ set number of steps for which the MC loop should report to :class`TakeStep`"""
        return self.report_steps

    def add_action(self, action):
        """add :class:`Action` 

        order in which multiple actions are added matters

        Parameters
        ----------
        action : :class:`Action`
            class of type :class:`Action`, constructed beforehand. Few action classes
            can be found in the actions directory
        """
        self.actions.append(action) 

    def add_accept_test(self, accept_test):
        """add :class:`AcceptTest` to MCrunner

        order in which multiple accept tests are added matters

        Parameters
        ----------
        test : :class:`AcceptTest`
            class of type :class:`AcceptTest`, constructed beforehand. Few accept test
            are in the accept_test directory
        """
        self.accept_tests.append(accept_test)

    def add_conf_test(self, conf_test):
        """add :class:`ConfTest` to MCrunner

        to be executed before the energy evaluation (potential call).
        These should be configurational tests that are faster to evaluate
        than the potential call, so that fast rejections save computational
        time. The order in which multiple conf tests are added matters.

        Parameters
        ----------
        test : :class:`ConfTest`
            class of type :class:`ConfTest`, constructed beforehand.Few configuration
            test can be found in the conf_test directory
        """
        self.conf_test.append(conf_test)

    def add_late_conf_test(self, conf_test):
        """add :class:`ConfTest` to MCrunner

        to be executed after the energy evaluation (potential call).
        These should be configurational tests that are slower to evaluate
        than the potential call, so that configurations that have been rejected
        by the :class:`AcceptTest` don't need to be tested in order to save
        computational time. The order in which multiple conf tests are added matters.

        Parameters
        ----------
        test : :class:`ConfTest`
            class of type :class:`ConfTest`, constructed beforehand. Configurations
            test can be found in the conf_test directory
        """
        self.late_conf_test.append(conf_test)

    def set_take_step(self, takestep):
        """add :class:`TakeStep` to MCrunner

        Multiple takestep should be combined using the appropriate
        classes designed to combined them, such as :class:`TakeStepPattern`
        and :class:`TakeStepProbabilities`

        Parameters
        ----------
        test : :class:`TakeStep`
            class of type :class:`TakeStep`, constructed beforehand. Take Step classes
            are in the take_step directory

        """
        self.take_steps = takestep


    def get_take_step(self):
        """ returns the take step used in MC Runner of :class`TakeStep`

        Return
        ----------
        take_steps : :class 'TakeStep'
            class used to displace 'coords'
        """
        return self.take_steps

    def set_coordinates(self, coords: np.ndarray, energy: float):
        """ set the coordinates

        Parameters
        ----------
        coords : numpy.array
            coordinates of the system
        energy: double
            associated energy with coords
        """
        self.coords = coords
        self.trial_coords = coords
        self.energy = energy
        self.trail_energy = energy

    def get_energy(self) -> float:
        """get the energy

        Returns
        -------
        energy : double
            energy for current coordinates
        """
        return self.energy

    def reset_energy(self):
        """recomputes and resets the energy of the system"""
        try:
            self.niter>0
            self.energy = self.compute_energy(self.coords)
        except:
            print("Resetting energy after first itteration is forbidden")
        
        
    def get_trial_energy(self) -> float:
        """get the energy of the previous coordinates

        Returns
        -------
        energy : float
            potential/energy of 'trial_coords'
        """

        return self.trail_energy

    def get_coords(self):
        """get the coordinates

        Returns
        -------
        x : numpy.array
            array of coordinates
        """
        return self.coords

    def get_trial_coords(self):
        """get the trial coordinates

        Returns
        -------
        x : numpy.array
            array of coordinates
        """
        return self.trial_coords

    def get_norm_coords(self) -> float:
        """get the norm of the coordinates

        Returns
        -------
        norm : double
            norm of coordinates

            .. math:: \sqrt{x \cdot x}
        """
        return (math.sqrt((self.coords)^2))

    def get_naccept(self):
        """get the total number of accepted 'run' iterations

        Returns
        -------
        accept_count : int
            number of accepted mc iterations
        """
        return self.accept_count

    def get_nreject(self):
        """get the total number of rejected 'run' iterations

        Returns
        -------
        accept_count : int
            number of accepted mc iterations
        """
        return self.nitercount -self.accept_count

    def get_accepted_fraction(self) -> float:
        """get the accepted fraction of steps

        Returns
        -------
        f : double
            accepted fraction of steps
        """
        return self.accept_count/self.nitercount

    def get_conf_rejection_fraction(self) -> float:
        """get the fraction of steps rejected by configuration tests

        Returns
        -------
        f : double
            fraction of steps rejected by the configuration tests
        """
        return self.conf_reject_count/self.nitercount 

    def get_E_rejection_fraction(self) -> float:
        """get the fraction of steps rejected by accept tests

        Returns
        -------
        f : double
            fraction of steps rejected by the accept tests
        """
        return self.E_reject_count/self.nitercount

    def get_iterations_count(self):
        """get the total number of iterations

        accumulates the number of iterations for many :func:`run` calls

        Returns
        -------
        n : int
            total number of iteration (accumulated over multiple :func:`run` calls)
        """
        return self.nitercount

    def get_neval(self):
        """get the total number of energy evaluation (per run)

        Returns
        -------
        neval : int
            total number of energy evaluation accumulated over
            a single run
        """
        return self.neval

    def get_potential(self):
        """get the potential of MC Runner

        Returns
        -------
        potential : class 'Potential'
            return energy, gradient and hessian
            information class
        """
        return self.pot_func

    def take_step_specified(self) -> bool:
        """Check if a :class 'TakeStep' has been specified to the MC Runner

        Returns
        -------
        x: bool
            True, if 'TakeStep' is specified. False, if 'TakeStep' is not specified 
        """
        if(self.take_step == None):
            return False
        else:
            return True

    def report_steps_specified(self) -> bool:
        """get the potential of MC Runner

        Returns
        -------
        potential : class 'Potential'
            return energy, gradient and hessian
            information class
        """
        return self.get_report_steps > 0
    
    def check_input(self):
        """Reports if :class 'ConfTest', :class 'AcceptTest' and, :class Action
        are specified, if not appropriate warnings are printed on the console
        """
        try:
            self.take_step == None
        except:
            print("takestep not set")
        if (self.enable_input_warnings):
            try:
                len(self.conf_test)==0 & len(self.late_conf_test)==0
            except:
                print("warning: no conf tests set")
            try:
                len(self.actions)==0 
            except:
                print("warning: no actions set" )
            try:
                len(self.accept_tests)==0
            except:
                print("warning: no accept tests set")
        
    def set_print_progress(self, input: bool):
        """enables display of progress bar for MC simulation"""
        self.print_progress = input

    def get_print_progress(self):
        """returns whether the 'print_progress' is set

        Returns
        -------
        success : bool
            tests outcome
        """ 
        print(self.print_progress)

    def get_success(self) -> bool:
        """test whether last steps has passed all tests

        Returns
        -------
        success : bool
            tests outcome
        """ 
        return self.success

    def get_last_success(self) -> bool:
        """check if last iteration was a success

        Returns
        -------
        bool
            True if sucess, False if not a success
        """ 
        return self.last_success

    def get_counter(self, counters):
        """get all counters

        Returns
        -------
        NumPy array
            Counters: 0: m_nitercount, 1: m_accept_count, 2: m_E_reject_count,
                      3: m_conf_reject_count, 4: m_neval
        """ 
        counters[0] = self.nitercount
        counters[1] = self.accept_count
        counters[2] = self.E_reject_count
        counters[3] = self.conf_reject_count
        counters[4] = self.neval
        return counters

    def set_counters(self, counters):
        """set all counters

        Parameters
        -------
        input : NumPy array
            Counters: 0: m_nitercount, 1: m_accept_count, 2: m_E_reject_count,
                      3: m_conf_reject_count, 4: m_neval
        """
        self.nitercount = counters[0]
        self.accept_count = counters[1]
        self.E_reject_count = counters[2]
        self.c_conf_reject_count  = counters[3]
        self.neval = counters[4]

    def get_changed_atoms(self):
        return self.take_steps.get_changed_atoms()

    def get_changed_coords_old(self):
        return self.take_steps.get_changed_coords_old()

    def abort(self):
        """abort :func:`run`"""
        sys.exit(0)

    def enable_input_warnings(self):
        """enables warnings about MC inputs, such as actions and configurational tests"""
        self.enable_input_warning = True

    def disable_input_warning(self):
        """disables warnings about MC inputs, such as actions and configurational tests"""
        self.enable_input_warning = False

    def compute_energy(self, x: np.ndarray) -> float:
        """get all counters

        Parameters
        ----------
        x : NumPy array
            coordinates of the system

        Returns
        -------
        energy: float
            The energy/potential from the :class 'Potential' method od 'get_energy'
        """ 
        self.neval += 1
        return self.pot_func.get_energy(x)  
    
    def do_conf_tests(self, x: np.ndarray) -> bool:
        """Performs the configurations tests specified for the beginning of the 
        'run'

        Parameters
        ----------
        x: NumPy array
            coordinates of the system

        Returns
        -------
        bool
            True if all the configuration tests passed successfully
            False if one or more of the configuration tests failed
        """ 
        for c_t in self.conf_test:
            result: bool = c_t.conf_test(x)
            if(result == False):
                self.conf_reject_count +=1 
                return False
        return True

    def do_accept_tests(self, xtrial, etrial, xold, eold):
        """Performs the accept tests specified for the MC Runner 
        'run'

        Parameters
        ----------
        x: NumPy array
            coordinates of the system

        Returns
        -------
        bool
            True if all the accept tests passed successfully
            False if one or more of the accept tests failed
        """ 
        for a_t in self.accept_tests:
            result = a_t.test(etrial, eold, self.temperature)
            if result is False:
                self.E_reject_count += 1
                return False
        return True
        

    def do_late_conf_test(self, x):
        """Performs the configurations tests specified for the end of the MC
        'run'

        Parameters
        ----------
        x: NumPy array
            coordinates of the system

        Returns
        -------
        bool
            True if all the configuration tests passed successfully
            False if one or more of the configuration tests failed
        """ 
        for lc_t in self.late_conf_test:
            result: bool = lc_t.conf_test(x)
            if(result == False):
                self.conf_reject_count +=1
                return False
        return True
        
    def do_actions(self, x: np.ndarray, energy: float, success: bool):
        """Performs the actions specified at the end of the MC
        'run'

        Parameters
        ----------
        x: NumPy array
            coordinates of the system
        
        energy: float
            Potential of parameter 'x'

        success: bool
            True if the iteration passed all the test, otherwise false
        """ 
        for act in self.actions:
            act.action(x, energy, success, self)

    def take_step(self):
        """Performs function 'displace' in the :class 'TakeStep'"""
        self.take_steps.displace(self.trial_coords, self)


    






    
    







