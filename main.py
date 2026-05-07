import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from system import MDSys
from pid import PID

fig, (ax_pos, ax_err) = plt.subplots(2, 1, figsize=(10, 7))
plt.subplots_adjust(bottom=0.45, hspace=0.4)

ax_kp  = plt.axes([0.2, 0.32, 0.6, 0.03])
ax_ki  = plt.axes([0.2, 0.26, 0.6, 0.03])
ax_kd  = plt.axes([0.2, 0.20, 0.6, 0.03])
ax_sp  = plt.axes([0.2, 0.12, 0.6, 0.03])
ax_btn = plt.axes([0.4, 0.04, 0.2, 0.06])

slider_kp = Slider(ax_kp, 'Kp',       0.0, 10.0, valinit=2.0)
slider_ki = Slider(ax_ki, 'Ki',       0.0, 5.0,  valinit=0.5)
slider_kd = Slider(ax_kd, 'Kd',       0.0, 5.0,  valinit=1.0)
slider_sp = Slider(ax_sp, 'Setpoint', 0.0, 10.0, valinit=5.0)
button    = Button(ax_btn, 'Start')

system = MDSys()
pid    = PID(kp=2.0, ki=0.5, kd=1.0)

t_data   = []
pos_data = []
err_data = []
step     = [0]
running  = [False]

line_pos, = ax_pos.plot([], [], color='#CCCCFF', label='position')
line_sp,  = ax_pos.plot([], [], color='r', linestyle='--', label='setpoint')
line_err, = ax_err.plot([], [], color='orange', label='error')
ax_err.axhline(y=0, color='k', linestyle='--', alpha=0.3)

ax_pos.set_xlim(0, 10)
ax_pos.set_ylim(-2, 12)
ax_pos.set_ylabel('position')
ax_pos.set_title('PID controller visualizer')
ax_pos.legend()

ax_err.set_xlim(0, 10)
ax_err.set_ylim(-6, 6)
ax_err.set_ylabel('error')
ax_err.set_xlabel('time (s)')
ax_err.legend()

def reset_sim():
    system.reset()
    pid.reset()
    pid.kp = slider_kp.val
    pid.ki = slider_ki.val
    pid.kd = slider_kd.val
    t_data.clear()
    pos_data.clear()
    err_data.clear()
    step[0] = 0
    line_pos.set_data([], [])
    line_sp.set_data([], [])
    line_err.set_data([], [])
    ax_pos.set_xlim(0, 10)
    ax_err.set_xlim(0, 10)
    fig.canvas.draw_idle()

def on_button(event):
    if running[0]:
        running[0] = False
        button.label.set_text('Start')
        reset_sim()
    else:
        reset_sim()
        running[0] = True
        button.label.set_text('Stop')
    fig.canvas.draw_idle()

button.on_clicked(on_button)

def animate(frame):
    if not running[0]:
        return line_pos, line_sp, line_err

    setpoint = slider_sp.val

    for _ in range(5):
        force = pid.compute(setpoint, system.position, system.dt)
        system.step(force)
        t_data.append(step[0] * system.dt)
        pos_data.append(system.position)
        err_data.append(setpoint - system.position)
        step[0] += 1

    line_pos.set_data(t_data, pos_data)
    line_sp.set_data(t_data, [setpoint] * len(t_data))
    line_err.set_data(t_data, err_data)

    if t_data[-1] > 10:
        ax_pos.set_xlim(t_data[-1] - 10, t_data[-1])
        ax_err.set_xlim(t_data[-1] - 10, t_data[-1])

    return line_pos, line_sp, line_err

ani = FuncAnimation(fig, animate, interval=20, blit=True)

plt.show()