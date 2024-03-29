import numpy as np
from scipy import linalg as LA
# import warnings 
import cmath
class Ray:
        
    def __init__(self, wavetype, F, p = (0,0,0), k = (0,0,0), A = 1, phase = 1,
                 **kwargs): 
        """
        Takes as arguments p, the current ray position coordinate and k, the 
        current ray direciton vector.
        """
        self._wavetype = wavetype
        self._F = F
        self._killed_rays = []
        self._p = np.array([p[0], p[1] , p[2]])
        #This allows for the position and direction coordinates to be given in
        #(), [], or as array.
        self._k = np.array([k[0], k[1], k[2]])
        self._A = A
        self._phase = phase
        
        self._Fs = [self._F]
        self._pos = [self._p]
        self._directs = [self._k]
        self._amps = [self._A]
        self._phases = [self._phase]
        
        self._distances = [np.zeros(3)]
        self._rdistances = [0]
        
        self._frameTpos = [np.zeros(3)]
        self._frameTdistances = [np.zeros(3)]
        self._frameTrdistances = [0]
        
        self._frameTscreen_xs = []
        self._frameTscreen_ys = []
        self._frameTscreen_zdistances = []
        # self._nindices = []
        
        
        
        global c
        c = 299792458

        if wavetype == "Gaussian":
            self._w0 = kwargs.get("w0")
            self._f = kwargs.get("f")
            self._E = self.EGauss(self._F, self._w0, self._f)
            
        
        self._Es = [self._E]
            
    def __repr__(self):
    
        return "%s: %s, %s: %s" %("position", self._p, "direction", self._k)
    
    def __str__(self):
        
        return "(%s, %s)"%(self._p, self._k)
    
    def __add__(self, other):
        self._p + other._p
        self._k + other._k
        
        return self
    
    def wavetype(self):
        """
        Returns the wavetype.
        """
        return self._wavetype
    
    def w0(self):
        return self._w0
    
    def f(self):
        return self._f
    
    def F(self):
        """
        Returns frequency.
        """
        return self._F
    
    def E(self):
        """
        Returns electric field magnitude.
        """
        if self._wavetype == "Gaussian":
            return self.EGauss(self._F, self._w0, self._f)
        
    def p(self):
        """
        Returns current ray position.
        """
        return self._p
    def k(self):
        """
        Returns current ray direction.
        """
        return self._k
    def A(self):
        """
        Returns current amplitude
        """
        return self._A
    def phase(self):
       """
       Returns current phase
       """
       return self._phase
    
    def setter(self, p, k):
        """
        Sets a new position and direction of ray.
        """
        self._p = np.array([p[0], p[1], p[2]])
        self._k = np.array([k[0], k[1], k[2]])
        
    def frameT(self, coordinates, direction):
        
        prop1 = direction
        prop2 = np.array([0,0,1])
        rotax = np.cross(prop1, prop2)/LA.norm(np.cross(prop1, prop2))
        theta = np.arccos(np.dot(prop1, prop2))
        if theta != 0.0:
        
            R1 = [rotax[0]*rotax[0]*(1-np.cos(theta)) + np.cos(theta), 
                  rotax[0]*rotax[1]*(1-np.cos(theta)) - rotax[2]*np.sin(theta), 
                  rotax[0]*rotax[2]*(1-np.cos(theta)) + rotax[1]*np.sin(theta)]
            R2 = [rotax[1]*rotax[0]*(1-np.cos(theta)) + rotax[2]*np.sin(theta),
                  rotax[1]*rotax[1]*(1-np.cos(theta)) + np.cos(theta),
                  rotax[1]*rotax[2]*(1-np.cos(theta)) - rotax[0]*np.sin(theta)]
            R3 = [rotax[2]*rotax[0]*(1-np.cos(theta)) - rotax[1]*np.sin(theta),
                  rotax[2]*rotax[1]*(1-np.cos(theta)) + rotax[0]*np.sin(theta),
                  rotax[2]*rotax[2]*(1-np.cos(theta)) + np.cos(theta)]
            R = np.array([R1, R2, R3])
            new_coordinates = np.matmul(R, coordinates) + self._frameTpos[-1]
        elif theta == 0.0:
            new_coordinates = coordinates + self._frameTpos[-1]

        return new_coordinates
        
    def append(self, F, p, k, A, phase, E):
        """
        Sets a new position and direction for ray and 
        appends this new position to a list containing all positions of the 
        ray.
        """
        # if p is not None:
        self._E = E
        self._Es.append(self._E)
        self._p = np.array([p[0], p[1], p[2]])
        self._pos.append(self._p)

        self._k = np.array([k[0], k[1], k[2]])
        self._directs.append(self._k)
        self._A = A
        self._amps.append(self._A)
        self._phase = phase
        self._phases.append(self._phase)
        self._F = F
        self._Fs.append(self._F)
        
        self._distances.append(abs(self._pos[-1]-self._pos[-2])+self._distances[-1])
        self._rdistances.append(LA.norm(abs(self._pos[-1]-self._pos[-2]))+self._rdistances[-1])
           
        return self
    
    def append2(self, frameTp): # PROVISIONAL
        
        self._frameTp = frameTp
        self._frameTpos.append(self._frameTp)
        
        self._frameTdistances.append(abs(self._frameTpos[-1]-self._frameTpos[-2])+self._frameTdistances[-1])
        self._frameTrdistances.append(LA.norm(abs(self._frameTpos[-1]-self._frameTpos[-2]))+self._frameTrdistances[-1])

    def append3(self, frameTscreen_x, frameTscreen_y, frameTscreen_zdistance): # PROVISIONAL
    
        self._frameTscreen_x = frameTscreen_x
        self._frameTscreen_y = frameTscreen_y
        self._frameTscreen_zdistance = frameTscreen_zdistance
        
        self._frameTscreen_xs.append(self._frameTscreen_x)
        self._frameTscreen_ys.append(self._frameTscreen_y)
        self._frameTscreen_zdistances.append(self._frameTscreen_zdistance)
        
    def frameTpositions(self):
        
        self._frameTxs = np.array([i[0] for i in self._frameTpos])
        self._frameTys = np.array([i[1] for i in self._frameTpos])
        self._frameTzs = np.array([i[2] for i in self._frameTpos])
        
        return self._frameTxs, self._frameTys, self._frameTzs, self._frameTpos
    
    def frameTscreenpositions(self):
        
        return self._frameTscreen_xs, self._frameTscreen_ys, self._frameTscreen_zdistances
        
    def coordinates(self): 
        """
        Extracts x,y and z coordinates from position arrays.
        """
        self._xs = np.array([i[0] for i in self._pos])
        self._ys = np.array([i[1] for i in self._pos])
        self._zs = np.array([i[2] for i in self._pos])
        
        return self._xs, self._ys, self._zs, self._pos, 
    
    def directions(self): 
        """
        Extracts kx, ky and kz directions from k arrays.
        """
        self._kxs = np.array([i[0] for i in self._directs])
        self._kys = np.array([i[1] for i in self._directs])
        self._kzs = np.array([i[2] for i in self._directs])
        
        return self._kxs, self._kys, self._kzs, self._directs
    
    def amplitudes(self):
        """
        Extracts amplitudes from amps 
        """
        self._ampsS = np.array([i for i in self._amps])
       
        return self._ampsS

    def phases(self):
        """
        Extracts amplitudes from amps 
        """
        self._phasesS = np.array([i for i in self._phases])
       
        return self._phasesS  
    
    def frameTdistances(self):
        """
        Extracts distance travelled in x, y and z direction.
        """
        self._frameTxdistances = np.array([i[0] for i in self._frameTdistances])
        self._frameTydistances = np.array([i[1] for i in self._frameTdistances])
        self._frameTzdistances = np.array([i[2] for i in self._frameTdistances])
        
        return (self._frameTxdistances, self._frameTydistances, self._frameTzdistances,
                self._frameTrdistances)
     
    def distances(self):
        """
        Extracts distance travelled in x, y and z direction.
        """
        self._xdistances = np.array([i[0] for i in self._distances])
        self._ydistances = np.array([i[1] for i in self._distances])
        self._zdistances = np.array([i[2] for i in self._distances])
        
        return (self._xdistances, self._ydistances, self._zdistances,
                self._rdistances)
    
    def Es(self):
        """
        Extracts amplitudes from amps 
        """
        self._EsS = np.array([i for i in self._Es])
       
        return self._EsS
        
    def intersection(self, ray2):
        """
        Returns the position of the point of intersection of two rays,
        one being the ray object that calls the method and the other the 
        the method argument."
        """
        vector_rays = ray2.p() - self.p()
        h = LA.norm(np.cross(ray2.k(), vector_rays))
        k = LA.norm(np.cross(ray2.k(), self.k()))
            
        if (h or k) < np.finfo(float).eps:
            intersection_pos = None
            print("The two rays with positions %s and %s do not intersect or " 
                  "are at the same position." % (self.p(), ray2.p()))
            
        else:
            intersection_pos = self.p() + h/k * self.k()
        
        return intersection_pos
   
    
class Bundle(Ray):
    """
    This class contains an array of appended ray object.
    """
    
    def __init__(self, ray):

        self._ray = ray
        
    def manyray(self, N):
        if self._ray.wavetype() == "Gaussian":
            
            wavetype = [self._ray.wavetype()]*N
            F = [self._ray.F()]*N
            p = [self._ray.p()]*N
            k = [self._ray.k()]*N
            A = [self._ray.A()]*N
            phase = [self._ray.phase()]*N
            w0 = [self._ray.w0()]*N
            f = [self._ray.f()]*N
        
            rays = ([Ray(wavetype, F, p, k, A, phase, w0=w0, f=f) 
                     for wavetype, F, p, k, A, phase, w0, f 
                     in zip(wavetype, F, p, k, A, phase, w0, f)])
            return rays
    
class Uniform(Bundle):
    """
    This class contains the required method to creat a uniform collimated 
    light beam from a bundle of rays.
    """
    
    def __init__(self, n = 19, r = 5, bundle_z = 0):
        """
        Parameters:
        
        n: number of rays in the bundle.
        
        r: he radius of the beam.
        
        bundle_z: the z coordinate of the ray positions.
        """
        self._n = n
        self._r = r
        self._bundle_z = bundle_z
        
        self._bundle_pos = []

        counter= 0
        for i in range(0, int(10e12)):# arbitrarily large number.
        
            # for Loop calculates the number of rays in the outer ring of the 
            # bundle.
            
            counter += (6*i + 6)
            
            if counter > self._n - 1:
                # The rings of rays can have a number of rays that is a 
                # multiple of 6 only.
                
                raise ValueError("The number of rays, n, does not allow for a " 
                                 "uniform circular beam to be created. The "
                                 "allowed number of rays are: 1+6=7, "
                                 "1+6+12=19, 1+6+12+18=37, 1+6+12+18+24=61, "
                                 "etc.")
            
            if abs(counter - (self._n - 1)) < np.finfo(float).eps:# number of 
            # rays in outer ring is matched by counter value.
                self._outer_ring = 6*i + 6
                
                break
            
        if self._r <= 0:
            raise ValueError("The beam radius must be greater than zero.")
       
        
        self._z_k = [(0 + 0j)]#Included point for central ray.
        
        for N in np.arange(6, self._outer_ring + 1, 6):
            #Uniform beam achieved by calculating the Nth roots of a complex 
            # number.
            #There are N equally spaced points on a circle radius
            #N/(number rays in outer ring) * r, separated by an angle 2pi/n.
            for k in range(0, N):
                
               
                zk = ((self._r*N/self._outer_ring) 
                      * cmath.exp(cmath.sqrt(-1) * (2*k*cmath.pi/N)))
                #Were zk is the nth root of a complex number
                self._z_k.append(zk)
                                       
        for i in self._z_k:
            self._bundle_pos.append(np.array([i.real, i.imag, self._bundle_z]))
            
    def translate(self, position):
        """
        Translates each ray in a bundle to a position in space.
        """
        position = np.array([position[0], position[1], position[2]])
        
        shift = position - self._bundle_pos[0]
        self._bundle_pos = self._bundle_pos + shift
           
        return self._bundle_pos
        
        
    def spots(self): 
        """
        Returns the list containing the nested initial position arrays of the 
        rays.
        """
        return self._bundle_pos
    
