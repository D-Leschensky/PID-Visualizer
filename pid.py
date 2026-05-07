class PID:
    def __init__(self, kp = 2.0, ki = 0.01, kd = 1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prevError = 0.0

    def compute(self, setpoint, current, dt):
        error = setpoint - current
        self.integral = error * dt
        derivative = (error - self.prevError)/dt
        self.prevError = error
        return (self.kp * error) + (self.kd * derivative) + (self.ki * self.integral)
    def reset(self):
        self.integral = 0
        self.prevError = 0

