couzinswarm
===========

Simulate fish swarming behavior with the model by `Iain Couzin et
al. <https://www.sciencedirect.com/science/article/pii/S0022519302930651>`__

Example
-------

.. code:: python

    from couzinswarm import Swarm

    swarm = Swarm()
    r, v = swarm.simulate(1000)

Install
-------

.. code:: bash

    pip install couzinswarm

Elaborate example
-----------------

.. code:: python

    import numpy as np
    import matplotlib.pyplot as pl
    from mpl_toolkits.mplot3d import Axes3D
    from couzinswarm import Swarm

    # note: the dimension of space is measure in fish length,
    # such that r = 1 means a length of one fish

    swarm = Swarm(
                 number_of_fish=20,
                 repulsion_radius=1,
                 orientation_width=10,
                 attraction_width=10,
                 # this angle is given in radians
                 # up to np.pi (not 360 degrees as in
                 # the paper)
                 angle_of_perception=np.pi,
                 # radians per unit of time
                 turning_rate=0.1,
                 # fish lengths per unit of time
                 speed=0.1,
                 # in units of fish length
                 noise_sigma=0.1,
                 dt=0.1,
                 # geometry of box
                 box_lengths=[100,100,100],
                 # boundary conditions
                 reflect_at_boundary = [True, True, True],
                 verbose=False,
                 )



    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')

    N_t = 1000

    t = np.arange(N_t+1)

    # Note that r.shape = v.shape = ( N_fish, N_t+1, 3 )
    positions, directions = swarm.simulate(N_t)
    r, v = positions, directions

    for i in range(swarm.number_of_fish):
        ax.plot(r[i,:,0], r[i,:,1], r[i,:,2])

    pl.show()

