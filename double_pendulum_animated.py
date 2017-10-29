#!/usr/bin/env python3
"""
===========================
The double pendulum problem
===========================

This animation illustrates the double pendulum problem.
"""

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

# Modified to show subplots comparing double pendulums with the same initial
# conditions, and then after that is closed, a second figure with the initial
# theta 1 modified by 1 degree

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

class double_pendulum(object):
    def __init__(self, fig, ax, th1=120.0):
        self.fig = fig
        self.ax = ax
        self.G = 9.8  # acceleration due to gravity, in m/s^2
        self.L1 = 1.0  # length of pendulum 1 in m
        self.L2 = 1.0  # length of pendulum 2 in m
        self.M1 = 1.0  # mass of pendulum 1 in kg
        self.M2 = 1.0  # mass of pendulum 2 in kg

        self.dt = 0.05
        t = np.arange(0.0, 20, self.dt)

        # th1 and th2 are the initial angles (degrees)
        # w10 and w20 are the initial angular velocities (degrees per second)
        th1 = th1
        w1 = 0.0
        th2 = -20.0
        w2 = 0.0

        # initial state
        state = np.radians([th1, w1, th2, w2])

        # integrate your ODE using scipy.integrate.
        self.y = integrate.odeint(self.derivs, state, t)

        self.x1 = self.L1*sin(self.y[:, 0])
        self.y1 = -self.L1*cos(self.y[:, 0])

        self.x2 = self.L2*sin(self.y[:, 2]) + self.x1
        self.y2 = -self.L2*cos(self.y[:, 2]) + self.y1

        self.line, = ax.plot([], [], 'o-', lw=2)
        self.time_template = 'time = %.1fs'
        self.time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

        self.line.set_data([], [])
        self.time_text.set_text('')

        self.ax.set_title('Initial angle 1 = {}'.format(th1))

    def derivs(self, state, t):
        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        del_ = state[2] - state[0]
        den1 = (self.M1 + self.M2)*self.L1 - self.M2*self.L1*cos(del_)*cos(del_)
        dydx[1] = (self.M2*self.L1*state[1]*state[1]*sin(del_)*cos(del_) +
                self.M2*self.G*sin(state[2])*cos(del_) +
                self.M2*self.L2*state[3]*state[3]*sin(del_) -
                (self.M1 + self.M2)*self.G*sin(state[0]))/den1

        dydx[2] = state[3]

        den2 = (self.L2/self.L1)*den1
        dydx[3] = (-self.M2*self.L2*state[3]*state[3]*sin(del_)*cos(del_) +
                (self.M1 + self.M2)*self.G*sin(state[0])*cos(del_) -
                (self.M1 + self.M2)*self.L1*state[1]*state[1]*sin(del_) -
                (self.M1 + self.M2)*self.G*sin(state[2]))/den2

        return dydx

    def animate(self, i):
        thisx = [0, self.x1[i], self.x2[i]]
        thisy = [0, self.y1[i], self.y2[i]]

        self.line.set_data(thisx, thisy)
        self.time_text.set_text(self.time_template % (i*self.dt))
        return self.line, self.time_text

class ani_wrapper(object):
    def __init__(self, iterable):
        self.fns = iterable
        self.called = 0
        self.n = len(iterable)

    def animate(self, *args, **kwargs):
        fn = self.fns[self.called % self.n]
        self.called += 1
        return fn(*args, **kwargs)

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,6))
ax1.grid()
ax1.set_xlim(-2,2)
ax1.set_ylim(-2,2)
ax2.grid()
ax2.set_xlim(-2,2)
ax2.set_ylim(-2,2)
dp1 = double_pendulum(f, ax1)
dp2 = double_pendulum(f, ax2)
aw = ani_wrapper((dp1.animate, dp2.animate))
ani = animation.FuncAnimation(f, aw.animate, np.arange(1, len(dp1.y)), interval=1000/30, blit=False)
# ani.save('double_pendulum.mp4', fps=15)
plt.show()

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,6))
ax1.grid()
ax1.set_xlim(-2,2)
ax1.set_ylim(-2,2)
ax2.grid()
ax2.set_xlim(-2,2)
ax2.set_ylim(-2,2)
dp1 = double_pendulum(f, ax1)
dp2 = double_pendulum(f, ax2, th1=119)
aw = ani_wrapper((dp1.animate, dp2.animate))
ani = animation.FuncAnimation(f, aw.animate, np.arange(1, len(dp1.y)), interval=1000/30, blit=False)
# ani.save('double_pendulum.mp4', fps=15)
plt.show()
