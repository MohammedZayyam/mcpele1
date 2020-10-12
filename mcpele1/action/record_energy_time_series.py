from mcpele1.montecarlo.template import Action



class RecordEnergyTimeSeries(Action):
    """Record a time series of the energy
    
    This class is the Python interface for the c++ bv::RecordEnergyTimeseries 
    :class:`Action` class implementation.
    
    Parameters
    ----------
    niter: int, Deprecated
        expected number of steps (to preallocate)
    record_every : int
        interval every which the energy is recorded
    """
    def __init__(self, record_every, startsteps):
        self.record_every = record_every
        self.startsteps = startsteps
        self.energylist = []

    def action(self, coords, energy, accepted, mcrunner):
        niter = mcrunner.get_iterations_count()
        if (niter > self.startsteps and niter % self.record_every == 0):
            self.energylist.append(energy)     

    def get_energy_time_series(self):
        """get a energy time series array
        
        Returns
        -------
        numpy.array
            array containing the energy time series
        """
        return self.energylist
