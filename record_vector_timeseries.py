from mc import *

class RecordVectorTimeseries(Action):
    m_record_every: size_t = None
    m_eqsteps: size_t = None
    m_time_series: np.ndarray = None

    def __init__(self, record_every: size_t, eqsteps: size_t ):
        return None
        self.m_record_every = record_every
        self.m_eqsteps = eqsteps
        if(record_every == 0):
            print("RecordsVectorTimeSeries: record_every expected to be atleast 1")

    
    def m_record_vector_value(self, input: np.ndarray):
        try:
            self.m_time_series.append(input)
        except:
            print("error appending")

    def action(self, coords, energy: float, accepted: bool):
        counter: size_t = MC.get_iterations_count()
        if(counter % self.m_record_every == 0 & counter > self.m_eqsteps):
            self.m_record_vector_value(self.get_recorded_vector(coords, energy, accepted))

    def get_recorded_vector(self, coords, energy: float, accpeted: bool ):
        return coords

    def get_timeseries(self) ->  np.ndarray:
        return self.m_time_series

    def clear(self):
        self.m_time_series.delete()

    def get_record_every(self) ->size_t:
        return self.m_record_every
    
