import numpy as np

from couzinswarm.objects import Fish

class Swarm:

    def __init__(self, 
                 number_of_fish=20,
                 repulsion_radius=1, 
                 orientation_width=10,
                 attraction_width=10,
                 angle_of_perception=340/360*np.pi, 
                 turning_rate=0.1,
                 speed=0.1,
                 noise_sigma=0.1,
                 dt=0.1,
                 box_lengths=[100,100,100],
                 reflect_at_boundary = [True, True, True],
                 verbose=False,
                 ):

         self.number_of_fish = number_of_fish
         self.repulsion_radius = repulsion_radius
         self.orientation_width = orientation_width
         self.attraction_width = attraction_width
         self.angle_of_perception = angle_of_perception
         self.turning_rate = turning_rate
         self.speed = speed
         self.noise_sigma = noise_sigma
         self.dt = dt
         self.box_lengths = np.array(box_lengths,dtype=float)
         self.reflect_at_boundary = reflect_at_boundary
         self.verbose = verbose


         self.fish = []

         self.init_random()


    def init_random(self):

        self.fish = [ Fish(position=self.box_lengths*np.random.random((3,)),
                           ID=i,
                           verbose=self.verbose
                           ) for i in range(self.number_of_fish) ]

    def simulate(self,N_time_steps):

        positions = np.empty((self.number_of_fish,N_time_steps+1,3))
        directions = np.empty((self.number_of_fish,N_time_steps+1,3))
        for i in range(self.number_of_fish):
            positions[i,0,:] = self.fish[i].position
            directions[i,0,:] = self.fish[i].direction
        

        for t in range(1,N_time_steps+1):

            for i in range(self.number_of_fish-1):
                F_i = self.fish[i]
                r_i = F_i.position
                v_i = F_i.direction

                for j in range(i+1,self.number_of_fish):
                    F_j = self.fish[j]
                    r_j = F_j.position
                    v_j = F_j.direction

                    r_ij = (r_j - r_i) 
                    distance = np.linalg.norm(r_ij) 
                    r_ij /= distance
                    r_ji = -r_ij

                    if distance < self.repulsion_radius:
                        F_i.zor_update(r_ij)
                        F_j.zor_update(r_ji)
                    elif distance < self.repulsion_radius + self.orientation_width + self.attraction_width:
                        angle_i = np.arccos(np.clip(np.dot(r_ij, v_i), -1.0, 1.0))
                        angle_j = np.arccos(np.clip(np.dot(r_ji, v_j), -1.0, 1.0))

                        if self.verbose:
                            print("angle_i", angle_i, self.angle_of_perception)
                            print("angle_j", angle_j, self.angle_of_perception)

                        if angle_i < self.angle_of_perception:
                            if distance < self.repulsion_radius + self.orientation_width:
                                F_i.zoo_update(v_j)
                            else:
                                F_i.zoa_update(r_ij)

                        if angle_j < self.angle_of_perception:
                            if distance < self.repulsion_radius + self.orientation_width:
                                F_j.zoo_update(v_i)
                            else:
                                F_j.zoa_update(r_ji)

            for i in range(self.number_of_fish):
                F_i = self.fish[i]
                F_i.evaluate_direction(self.turning_rate*self.dt,self.noise_sigma)

                new_v = F_i.new_d
                dr = self.speed * new_v 
                for dim in range(3):
                    if dr[dim]+F_i.position[dim] > self.box_lengths[dim] or \
                       dr[dim]+F_i.position[dim] < 0.0:
                        if not self.reflect_at_boundary[dim]:
                            if dr[dim] > self.box_lengths[dim]:
                                dr[dim] -= self.box_lengths[dim]
                            else:
                                dr[dim] += self.box_lengths[dim]
                        else:
                            dr[dim] *= -1
                            new_v[dim] *= -1

                F_i.position += dr
                F_i.direction = new_v

                positions[i,t,:] = F_i.position
                directions[i,t,:] = F_i.direction

                F_i.reset()

        return positions, directions


if __name__ == "__main__":

    swarm = Swarm(number_of_fish=2,speed=0.01,noise_sigma=0,turning_rate=0.1)

    #swarm.fish[0].position = np.array([50.,50.,50])
    #swarm.fish[0].direction = np.array([1.,0.,0.])
    #swarm.fish[1].position = np.array([50.,50.,50.3])
    #swarm.fish[1].direction = np.array([1.,0.,0.])

    swarm.fish[0].position = np.array([47,50.,50.])
    swarm.fish[0].direction = np.array([0.,0.,1.])
    swarm.fish[1].position = np.array([58.,50.,50])
    swarm.fish[1].direction = np.array([1.,0.,0.])



    N_t = 1000

    t = np.arange(N_t+1)
    r, v = swarm.simulate(N_t)
    print(
        swarm.fish[0].direction,
        swarm.fish[1].direction,
    )
    from bfmplot import pl
    from mpl_toolkits.mplot3d import Axes3D
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(swarm.number_of_fish):
        ax.plot(r[i,:,0], r[i,:,1], r[i,:,2])

    #ax.set_xlim([0,swarm.box_lengths[0]])
    #ax.set_ylim([0,swarm.box_lengths[1]])
    #ax.set_zlim([0,swarm.box_lengths[2]])

    pl.show()



