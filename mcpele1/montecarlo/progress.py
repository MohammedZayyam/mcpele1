import time

class Progress:
    inverse_of_total_iterations: float = None
    total_iterations: float = None
    curr= None
    prev = None
    start_time = None
    def __init__(self, totallin):
        self.inverse_of_total_iterations = 1/ totallin
        self.total_iterations = totallin
        self.curr = 0
        self.prev = 0
        self.start_time = time.time()

    def get_current_percentage(self):
        return self.curr
    
    def next(self, idx):
        self.curr = (idx/ self.total_iterations)*100
        if (self.curr != self.prev):
            self.print_time_percentage(idx -1)
            if(self.curr == 100):
                StopIteration

    def convertdatetimetoseconds(self, t):
        (h, m, s) = t.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    def print_time_percentage(self,smp):
        #update and print percentage complete
        print(self.curr, "%")
        self.prev = self.curr
        #get and print elapsed time
        #print("time :", self.start_time )
        print("time elapsed :", time.time()-self.start_time , "seconds")
        #estimate and print time to complete
        print("time to completion :", (self.total_iterations- smp - 1)/(smp + 1)*(time.time()- self.start_time), "seconds")
        #estimate and print time total time ot complete
        print("total time :", (self.total_iterations/(smp+1)*(time.time()- self.start_time)), "seconds")
        #estimate and print total local completetion time
        #have to do the last
        