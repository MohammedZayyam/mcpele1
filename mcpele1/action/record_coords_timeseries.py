from mcpele1.action.record_vector_timeseries import RecordVectorTimeseries, np
"""
mvc = mean coordinate vector
mvc2 = mean coordinate vector squared
ndof: int
    dimensionality of coordinate array
"""

class RecordsCoordsTimeSeries(RecordVectorTimeseries):
    """Record time series of the average root mean square displacement per particle at each step
    
    This class is the Python interface for the c++ RecordDisplacementPerParticleTimeseries 
    :class:`Action` class implementation.
    
    Parameters
    ----------
    niter: int, Deprecated
        expected number of steps (to preallocate)
    record_every : int
        interval every which the energy is recorded
    initial_coords : numpy.array
        initial system coordinates, used to compute rms distance
    boxdimension: int
        dimensionality of the space (dimensionality of box)
    """
    mcv = []
    mcv2 = []
    mdof = 0
    count = 0

    def __init__(self, ndof, record_every, eqsteps):
        self.mcv = np.zeros(ndof)
        self.mcv2 = np.zeros(ndof)
        self.ndof = ndof
        self.count = 0

    def update_average(self, avg, x):
        """ updates the average given the new  'coords'

        Paramteres
        ----------
        x: NumPy array
            coordinates
        avg: float
            current average of the coordinates
        
        Return
        ------
        float
            new average
        """
        n= self.count
        return ((avg*n +x)/(n+1))

    def update_mean_coord_vector(self, new_coords):
        """ updates the average given the new  'coords'

        Paramteres
        ----------
        new_coords: NumPy array
            new coordinates
        """
        i =0
        while(i<self.ndof):
            newx = new_coords[i]
            self.mcv[i] = self.update_average(self.mcv[i],newx )
            self.mcv2[i] = self.update_average(self.mcv2[i],newx*newx )
            i +=1
        self.count +=1
            

    def get_recorded_vector(self, coords, energy, accepted):
        """ get the coordinates

        Paramteres
        ----------
        coords: NumPy array
            coordinates
        energy: float
            energy of coords
        accepted: Bool
            iteration sucess
        
        Return
        ------
        NumPy array
            coords
        """
        return coords

    #a pointer to mc-> m_get_iteration_count,  needed instead of get_iteration
    def action(self, coords, energy, accepted, mcrunner):
        try:
            len(coords) == self.ndof
            counter = mcrunner.get_iterations_count()
            if(counter>self.m_eqsteps):
                self.update_mean_coord_vector(coords)
                if(counter %self.m_record_every == 0):
                    #is this an extra bit of code?
                    self.m_record_vector_value(self.get_recorded_vector(coords, energy, accepted))
        except:
            print("ndof and coords have different size")
    
    def get_mean_coordinate_vector(self):
        return self.mcv

    def get_mean2_coordinate_vector(self):
        return self.mcv2
    
    def get_variance_coordinate_vector(self):
        var = self.mcv2
        i = 0
        while(i<self.ndof):
            var[i] = self.mcv[i]*self.mcv[i]
            i+=1
        return var
    
    def get_count(self):
        return self.count

            