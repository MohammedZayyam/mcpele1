from template import *
class FindLowestEigenValue(abc.ABCMeta):
    m_lowesteigpot: list
    m_ranvec: np.ndarray
    m_lbfgs: float #check the type for this variable
    
    def __init__(self, landscape_potential: List[size_t], boxdimension: size_t, ranvec: np.ndarray,
    lbfgsniter: size_t ):
        self.landscape_potential = landscape_potential
        self.boxdimension = boxdimension
        self.ranvec = ranvec
        self.lbfgsniter = lbfgsniter

    @abc.abstractclassmethod
    def compute_lowest_eigenvalue(coords) -> float:
        return None