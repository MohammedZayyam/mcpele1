from mcpele1.montecarlo.template import *

class Progress:
    m_inverse_of_total_itterations: float = None
    m_total_itterations: float = None
    m_curr: size_t = None
    m_prev: size_t = None
    m_start_time = None
    def __init__(self, totallin):
        self.m_inverse_of_total_itterations = 1/ totallin
        self.m_total_itterations = totallin
        self.m_curr = 0
        self.m_prev = 0
        self.m_start_time = time.time()

    
    def get_current_percentage(self):
        return self.m_curr
    

    def next(self, idx):
        self.m_curr = (idx/ self.m_total_itterations)*100
        if (self.m_curr != self.m_prev):
            self.print_time_percentage(idx -1)
            if(self.m_curr == 100):
                StopIteration

    def convertdatetimetoseconds(self, t):
        (h, m, s) = t.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    def print_time_percentage(self,smp):
        #update and print percentage complete
        print("{}%", self.m_curr)
        self.m_prev = self.m_curr
        #get and print elapsed time
        #print("time :", self.m_start_time )
        print("time elapsed in seconds :", time.time()-self.m_start_time )
        #estimate and print time to complete
        print("time to completion in seconds :", (self.m_total_itterations- smp - 1)/(smp + 1)*(time.time()- self.m_start_time))
        #estimate and print time total time ot complete
        print("total time in seconds :", (self.m_total_itterations/(smp+1)*(time.time()- self.m_start_time)) )
        #estimate and print total local completetion time
        """you have to do the last method
        """