from mcpele1.montecarlo.template import Action



class RecordEnergyTimeSeries(Action):
    """ Records the Energy time Series

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
        return self.energylist
