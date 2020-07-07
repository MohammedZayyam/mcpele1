from template import *

class RecordVectorTimeseries(mc.Action):
    m_record_every: mc.size_t = None
    m_eqsteps: mc.size_t = None
    m_time_series: np.ndarray = None

    def __init__(self, record_every: mc.size_t, eqsteps: mc.size_t ):
        self.m_record_every = record_every
        self.m_eqsteps = eqsteps
        if(record_every == 0):
            print("RecordsVectorTimeSeries: record_every expected to be atleast 1")

    
    def m_record_vector_value(self, input: np.ndarray):
        try:
            self.m_time_series.append(input)
        except:
            print("error appending")
    @staticmethod
    def action( coords, energy: float, accepted: bool):
        counter: size_t = .get_iterations_count()
        if(counter % self.m_record_every == 0 & counter > self.m_eqsteps):
            self.m_record_vector_value(self.get_recorded_vector(coords, energy, accepted))

    def get_recorded_vector(self, coords, energy: float, accpeted: bool ):
        return coords

    def get_timeseries(self) ->  np.ndarray:
        return self.m_time_series

    def clear(self):
        self.m_time_series.delete()

    def get_record_every(self) ->mc.size_t:
        return self.m_record_every
    
