class MDSys:
    def __init__(self, mass=1.0,damping = 0.5,dt = 0.01):
        self.mass = mass
        self.damping = damping
        self.dt = dt
        self.position = 0.0
        self.velocity = 0.0
    def step(self, force):
        accel = (force - self.damping * self.velocity) / self.mass
        self.velocity += accel *self.dt
        self.position += self.velocity * self.dt
        return self.position
    def reset(self):
        self.position = 0
        self.velocity = 0
        #self.accel = 0

