# Simple Gravity Simulator
This is a simple gravity simulator on pygame. You can use this for simulating planets' movement.

**How does it work?**

Config params stored in *config.json*:

- **G** is a [physical constant](https://en.wikipedia.org/wiki/Gravitational_constant)
- **T** shows an amount of time that one iteration takes, the lower T is, the more accurate the simulator is
- **scale** shows the number of meters in one pixel
- **iterationsPerFrame** helps increase the speed of simulator, drawing only every *n* frame

To add a body you have to create an object `Body()` and add it to the list in `__init__` of object `System()`.