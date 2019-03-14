from couzinswarm import Swarm
import numpy as np

import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    swarm = Swarm(number_of_fish=100,
                  speed=3,
                  orientation_width=2,
                  attraction_width=14,
                  noise_sigma=0.001,
                  angle_of_perception=270/360*np.pi,
                  turning_rate = 40/180*np.pi,
                  box_lengths=[200,200,200],
                  reflect_at_boundary = [False, False, False]
                  )


    N_t = 400

    t = np.arange(N_t+1)
    r, v = swarm.simulate(N_t)
    print(
            swarm.fish[0].direction,
            swarm.fish[1].direction,
         )
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')

    #for i in range(swarm.number_of_fish):
    #    ax.plot(r[i,:,0], r[i,:,1], r[i,:,2],'k-',lw=1.4)
    for i in range(swarm.number_of_fish):
        ax.plot(
                [ r[i,-1,0], r[i,-1,0]+3*v[i,-1,0]],
                [ r[i,-1,1], r[i,-1,1]+3*v[i,-1,1]],
                [ r[i,-1,2], r[i,-1,2]+3*v[i,-1,2]],
                )

    pl.show()
