### Double Pendulum Demo: side by side double pendulums with different initial conditions 
(using matplotlib subplots)

I was looking for a simple python-based tool to demo the concepts of chaos / predictive nondeterminism but wasn't able to find any such code online. To build this demo I (hastily and sloppily) modified code from the [matplotlib examples](https://matplotlib.org/examples/animation/double_pendulum_animated.html) to support two side by side simulations with the option to tune the initial conditions (here, I only added the option to change theta 1 to the object init, but any other parameters could be added as well). 

The key insight in modifying the example code is that the animation function has to return the matplotlib artists each time that are to be updated, so we can't update both plots simultaneously (and if we run two independent animations the timesteps drift out of sync). Instead, I created a class called `ani_wrapper` which steps through an iterable of animation functions, updating only one of the possible functions each time it's called, then wrapping back to the beginning when it reaches the end of the iterator. Note that `blit=False` must be set to disable optimizations getting rid of flickering of the resulting animation since we aren't updating the entire animation at every time step.

If executed as-is, the script will first show two side by side double pendulums with identical initial conditions, then when that figure is closed, a second animation will launch with one of the initial conditions perturbed by one degree. 
