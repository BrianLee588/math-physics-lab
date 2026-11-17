import math

class NewtonSecondLaw:
    def __init__(self,mass=5,force=10,initial_velocity=0): self.reset(mass,force,initial_velocity)
    def reset(self,mass=None,force=None,initial_velocity=None):
        if mass is not None: self.mass=float(mass)
        if force is not None: self.force=float(force)
        if initial_velocity is not None: self.initial_velocity=float(initial_velocity)
        if self.mass<=0: raise ValueError("質量必須大於 0")
        self.time=0.; self.position=0.; self.velocity=self.initial_velocity
        self.acceleration=self.force/self.mass
    def step(self,dt):
        self.position+=self.velocity*dt+.5*self.acceleration*dt**2
        self.velocity+=self.acceleration*dt; self.time+=dt
        return self.get_state()
    def get_state(self):
        return {"time":self.time,"position":self.position,"velocity":self.velocity,
                "acceleration":self.acceleration,"forces":{"applied_force":self.force}}
class InclinedPlane:
    G=9.81
    def __init__(self,mass=5,angle_degrees=30,mu_static=.5,mu_kinetic=.3):
        self.reset(mass,angle_degrees,mu_static,mu_kinetic)
    def reset(self,mass=None,angle_degrees=None,mu_static=None,mu_kinetic=None):
        if mass is not None:self.mass=float(mass)
        if angle_degrees is not None:self.angle_degrees=float(angle_degrees)
        if mu_static is not None:self.mu_static=float(mu_static)
        if mu_kinetic is not None:self.mu_kinetic=float(mu_kinetic)
        if self.mass<=0 or not 0<=self.angle_degrees<90 or self.mu_static<0 or self.mu_kinetic<0:
            raise ValueError("參數超出合理範圍")
        th=math.radians(self.angle_degrees)
        self.time=0.;self.position=0.;self.velocity=0.
        self.gravity_parallel=self.mass*self.G*math.sin(th)
        self.gravity_perpendicular=self.mass*self.G*math.cos(th)
        self.normal_force=self.gravity_perpendicular
        self.max_static_friction=self.mu_static*self.normal_force
        self.is_sliding=self.gravity_parallel>self.max_static_friction+1e-10
        self.static_friction=self.gravity_parallel if not self.is_sliding else self.max_static_friction
        self.kinetic_friction=self.mu_kinetic*self.normal_force
        self.acceleration=(self.gravity_parallel-self.kinetic_friction)/self.mass if self.is_sliding else 0.
    def step(self,dt):
        if self.is_sliding:
            self.position+=self.velocity*dt+.5*self.acceleration*dt**2
            self.velocity+=self.acceleration*dt
        self.time+=dt;return self.get_state()
    def get_state(self):
        return {"time":self.time,"position":self.position,"velocity":self.velocity,
                "acceleration":self.acceleration,"is_sliding":self.is_sliding,
                "forces":{"gravity_parallel":self.gravity_parallel,
                          "gravity_perpendicular":self.gravity_perpendicular,
                          "normal":self.normal_force,
                          "friction":self.kinetic_friction if self.is_sliding else self.static_friction,
                          "max_static_friction":self.max_static_friction}}
