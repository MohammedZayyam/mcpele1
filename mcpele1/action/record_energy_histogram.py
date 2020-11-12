from mcpele1.montecarlo.template import Action
import numpy as np
import sys
import math 

class Histogram():
    def __init__(self, minimum, maximum, bin):
        self.minimum = math.floor((minimum / bin)) * bin
        self.maximum = math.floor((maximum / bin) + 1) * bin
        self.bin = bin
        self.eps = sys.float_info.epsilon
        self.N = int((maximum-minimum)/bin)
        self.hist = np.zeros(self.N +1)
        self.niter = 0
        self.mean = 0
        self.variance = 0
        self.moments = 0

    def get_maximum(self):
        return self.maximum

    def get_minimum(self):
        return self.minimum

    def bin(self):
        return self.bin
    
    def size(Self):
        return self.N
    
    def get_count(self):
        return self.niter
    
    def get_mean(self):
        temp = np.array(self.hist)
        self.mean = temp.sum()/len(temp)
        return self.mean
    
    def get_variance(self):
        temp = np.array(self.hist)
        self.variance = np.var(temp)
        return self.variance
    
    def begin(self):
        return self.hist[0]
    
    def end(self):
        return self.hist[-1]

    def get_position(self, bin_index):
        return self.minimum +(0.5+bin_index)*self.bin
    
    def get_vectdata(self):
        return self.hist
    
    def resize(self, E, i):
        newlen= 0
        if i >= self.N:
            newlen = (i+1)- self.N
            np.append(self.hist, newlen -1)
            self.niter += 1
            self.maximum = math.floor(E/self.bin + 1)*self.bin
            self.N = round(self.maximum - self.minimum)/self.bin
            if len(self.hist) != self.N:
                print("E:", E, "|niter:", self.niter, "|size:", len(self.hist), "|minimum:", self.minimum, "|maximum:", self.maximum, "|i:", i, "|N:", self.N)
                assert(len(self.hist) == self.N)
                exit
            print("resized below at niter:", self.niter)
        if i <0:
            newlens = -1*i
            self.hist.insert(0, newlens -1)
            self.hist.insert(0, 1)
            self.niter +=1
            self.minimum = math.floor((E/self.bin))*self.bin
            self.N =round((self.maximum -self.minimum)/self.bin)
            if len(self.hist)!= self.N:
                print("E:", E, "|niter:", self.niter, "|size:", len(self.hist), "|minimum:", self.minimum, "|maximum:", self.maximum, "|i:", i, "|N:", self.N)
                assert(len(self.hist) == self.N)
                exit
            print("resized below at niter:", self.niter)
        else:
            print("histogram encountered unexpected condition")
            print("E:", E, "|niter:", self.niter, "|size:", len(self.hist), "|minimum:", self.minimum, "|maximum:", self.maximum, "|i:", i, "|N:", self.N) 


    def add_entry(self, E):
        self.moments = E
        E += self.eps
        i = math.floor((E - self.minimum)/self.bin)
        if (i < self.N and i >= 0):
            self.hist[i] +=1
            self.niter+= 1
        else:
            self.resize(E, i)



    

class RecordEnergyHistogram(Action):
        def __init__(self, minimum, maximum, bin, eqsteps):
            """
            """
            self.hist = Histogram(minimum, maximum, bin)
            self.eqsteps = eqsteps
            self.count = 0

        def action(self, coords, energy, accepted, mcrunner):
            self.count  = mcrunner.get_iterations_count()
            if self.count > self.eqsteps:
                self.hist.add_entry(energy)


        def get_histogram(self):
            histogram = self.hist.get_vectdata()
            return histogram


        
