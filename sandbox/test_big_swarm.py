from couzinswarm import Swarm
import numpy as np

import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    swarm = Swarm(number_of_fish=100,
                  speed=1,
                  noise_sigma=0.05,
                  turning_rate=0.1,
                  verbose=False,
                  angle_of_perception=np.pi)

    swarm.fish[0].position = np.array([50.,50.,50])
    swarm.fish[0].direction = np.array([1.,0.,0.])
    swarm.fish[1].position = np.array([50.,50.,50.3])
    swarm.fish[1].direction = np.array([1.,0.,0.])


    N_t = 1000

    t = np.arange(N_t+1)
    r, v = swarm.simulate(N_t)
    print(
            swarm.fish[0].direction,
            swarm.fish[1].direction,
         )
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(swarm.number_of_fish):
        ax.plot(r[i,:,0], r[i,:,1], r[i,:,2])

    pl.show()
