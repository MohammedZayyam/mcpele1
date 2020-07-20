from mcpele1.montecarlo.template import Action, np
"""
Records vector time series, every m_record_every-th(variable) step
"""
class RecordVectorTimeseries(Action):
    m_record_every=1 
    m_eqsteps=0
    m_time_series: np.ndarray = []

    def __init__(self, record_every, eqsteps):
        self.m_record_every = record_every
        self.m_eqsteps = eqsteps
        if(record_every == 0):
            print("RecordsVectorTimeSeries: record_every expected to be atleast 1")

    
    def m_record_vector_value(self, input: np.ndarray):
        try:
            self.m_time_series.append(input)
        except:
            print("error appending")

    def action( self, coords, energy: float, accepted: bool, mcrunner):
        counter = mcrunner.get_iterations_count()
        if(counter % self.m_record_every == 0 & counter > self.m_eqsteps):
            self.m_record_vector_value(mcrunner.get_recorded_vector(coords, energy, accepted))



    def get_recorded_vector(self, coords, energy: float, accpeted: bool ):
        return coords

    def get_timeseries(self) ->  np.ndarray:
        """
        get a tragectory of at what steps in the simulation to record the vectors
        """
        return self.m_time_series

    def clear(self):
        self.m_time_series= []

    def get_record_every(self):
        return self.m_record_every
    
