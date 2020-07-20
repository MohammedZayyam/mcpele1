import math
from mcpele1.montecarlo.template import np
from mcpele1.montecarlo.mc import MC
from mcpele1.takestep.gaussian_coords_displacement import SimpleGaussian
from mcpele1.action.record_energy_time_series import RecordEnergyTimeSeries

"""
create a Option class to define the potential of the Monte Carlo simulation
"""
#potential
class Option:
    def __init__(self, stock_price, strike_price, risk, volatility, tenor, CorP, Steps):
        self.S= stock_price
        self.K = strike_price
        self.r = risk
        self.v = volatility
        self.T = tenor
        self.CorP = CorP
        self.Steps = Steps#dimension

    def get_energy(self, x):
        deltaT = self.T/self.Steps
        y = self.S
        for i in range(0, len(x)):

            y= y*math.exp(((self.r-((self.v*self.v)/2))*deltaT)+   (self.v*math.sqrt(deltaT)*x[i]))

        return y
        
        

class Option_Price:
    energy_list: np.ndarray
    S= 50
    K = 50
    r = 0.05
    v =0.5
    T =1
    CorP = "C"
    Steps = 100 
    samples = 10000

    def __init__(self):
        #steps and dimension
        self.ndim = self.Steps #proxy for number of time steps, linearly the system in one dimensional
        self.samples = self.samples
        self.potential =  Option(self.S, self.K, self.r, self.v, self.T, self.CorP, self.Steps)
        #setting up the simulator
        self.mc = MC(self.potential, np.zeros(self.ndim), 1)
        #generating coords(normal random numbers)
        self.takestep =  SimpleGaussian(42, self.ndim)
        self.mc.set_take_step(self.takestep)
        self.Recorded_Energy = RecordEnergyTimeSeries(1,1)
        #collecting all energies of each simulation
        self.mc.add_action(self.Recorded_Energy)
        self.mc.run(self.samples)
        self.energy_list = np.array(self.Recorded_Energy.get_energy_time_series())

if __name__ == "__main__":
    optprc = Option_Price()
    energy_l =optprc.energy_list
    #Substract with stock price and remove all negatives
    energy_l = energy_l - optprc.K
    energy_l[energy_l<0]=0
    ans = np.sum(energy_l)/optprc.samples*math.exp(-optprc.r*optprc.T )
    print("option price:",ans )



