"""
Simulation module
=================

Contains the `Swarm` class, which is used for simulation.
"""
import numpy as np

from couzinswarm.objects import Fish

from progressbar import ProgressBar as PB

class Swarm:
    """A class for a swarm simulation.
    
    Attributes
    ----------
    number_of_fish : int, default : 20
        The number of fish to be simulated
    fish : list of :mod:`couzinswarm.objects.Fish`
        Contains the `Fish` objects which are simulated in this setup.
    repulsion_radius : float, default : 1.0
        Fish within this radius will repel each other
        (unit: length of a single fish).
    orientation_width : float, default : 10.0
        The width of the hollow ball in which fish adjust their
        orientation.
        (unit: length of a single fish).
    attraction_width : float, default : 10.0
        The width of the hollow ball in which fish attract
        each other
        (unit: length of a single fish).
    angle_of_perception : float, default : 340/360*pi
        angle in which a fish can see other fish
        (unit: radians, with a maximum value of :math:`\pi`.
    turning_rate : float, default : 0.1
        Rate at which the new direction is approached.
        The maximum angle change per time step is hence ``turning_rate * dt``
        (unit: radians per unit time).
    speed : float, default : 0.1
        Speed of a fish.
        (unit: fish length per unit time).
    noise_sigma : float, default : 0.01
        Standard deviation of radial noise whith 
        which each direction adjustment is shifted
        (unit: radians).
    dt : float, default : 0.1
        how much time passes per step
        (unit: unit time).
    box_lengths : list or numpy.ndarray of float, default : [100,100,100]
        Dimensions of the simulation box in each dimension
        (unit: fish length)
    reflect_at_boundary list of bool, default : [True, True, True]
        for each spatial dimension decided whether boundaries should reflect.
        If they don't reflect they're considered to be periodic (not implemented yet)
    verbose : bool, default : False
        be chatty.
    show_progress : bool, default : False
        Show the progress of the simulation.

    """

    def __init__(self, 
                 number_of_fish=20,
                 repulsion_radius=1, 
                 orientation_width=10,
                 attraction_width=10,
                 angle_of_perception=340/360*np.pi, 
                 turning_rate=0.1,
                 speed=0.1,
                 noise_sigma=0.01,
                 dt=0.1,
                 box_lengths=[100,100,100],
                 reflect_at_boundary = [True, True, True],
                 verbose=False,
                 show_progress=False,
                 ):
        """
        Setup a simulation with parameters as defined in the paper.
        https://www.sciencedirect.com/science/article/pii/S0022519302930651

        Fish will be created at random positions with random directions.

        Parameters
        ----------
        number_of_fish : int, default : 20
            The number of fish to be simulated
        repulsion_radius : float, default : 1.0
            Fish within this radius will repel each other
            (unit: length of a single fish).
        orientation_width : float, default : 10.0
            The width of the hollow ball in which fish adjust their
            orientation.
            (unit: length of a single fish).
        attraction_width : float, default : 10.0
            The width of the hollow ball in which fish attract
            each other
            (unit: length of a single fish).
        angle_of_perception : float, default : 340/360*pi
            angle in which a fish can see other fish
            (unit: radians, with a maximum value of :math:`\pi`.
        turning_rate : float, default : 0.1
            Rate at which the new direction is approached.
            The maximum angle change per time step is hence ``turning_rate * dt``
            (unit: radians per unit time).
        speed : float, default : 0.1
            Speed of a fish.
            (unit: fish length per unit time).
        noise_sigma : float, default : 0.01
            Standard deviation of radial noise whith 
            which each direction adjustment is shifted
            (unit: radians).
        dt : float, default : 0.1
            how much time passes per step
            (unit: unit time).
        box_lengths : list or numpy.ndarray of float, default : [100,100,100]
            Dimensions of the simulation box in each dimension
            (unit: fish length)
        reflect_at_boundary list of bool, default : [True, True, True]
            for each spatial dimension decided whether boundaries should reflect.
            If they don't reflect they're considered to be periodic
        verbose : bool, default : False
            be chatty.

        """
        

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
        self.show_progress = show_progress

        self.box_copies = [[0.],[0.],[0.]]

        for dim, reflect in enumerate(self.reflect_at_boundary):
            if not reflect:
                self.box_copies[dim].extend([-self.box_lengths[dim],+self.box_lengths[dim]])


        self.fish = []

        self.init_random()


    def init_random(self):
        """
        Initialize the fish list
        """

        self.fish = [ Fish(position=self.box_lengths*np.random.random((3,)),
                           ID=i,
                           verbose=self.verbose
                           ) for i in range(self.number_of_fish) ]

    def simulate(self,N_time_steps):
        """Simulate a swarm according to the rules.

        Parameters
        ----------
        N_time_steps : int
            Number of time steps to simulate.

        Returns
        -------
        positions : numpy.ndarray of shape ``(self.number_of_fish, N_time_steps+1, 3_)``
            Keeping track of the fish's positions for each time step.
        directions : numpy.ndarray of shape ``(self.number_of_fish, N_time_steps+1, 3_)``
            Keeping track of the fish's directions for each time step.
        """


        # create result arrays and fill in initial positions
        positions = np.empty((self.number_of_fish,N_time_steps+1,3))
        directions = np.empty((self.number_of_fish,N_time_steps+1,3))
        for i in range(self.number_of_fish):
            positions[i,0,:] = self.fish[i].position
            directions[i,0,:] = self.fish[i].direction
        

        bar = PB(max_value=N_time_steps)
        # for each time step
        for t in range(1,N_time_steps+1):

            # iterate through fish pairs
            for i in range(self.number_of_fish-1):
                F_i = self.fish[i]
                r_i = F_i.position
                v_i = F_i.direction

                for j in range(i+1,self.number_of_fish):

                    F_j = self.fish[j]
                    relationship_counted = False

                    for X in self.box_copies[0]:

                        if relationship_counted:
                            break

                        for Y in self.box_copies[1]:
                            for Z in self.box_copies[2]:


                                r_j = F_j.position + np.array([X,Y,Z])
                                v_j = F_j.direction

                                # get their distance, and unit distance vector
                                r_ij = (r_j - r_i) 
                                distance = np.linalg.norm(r_ij) 
                                r_ij /= distance
                                r_ji = -r_ij

                                # if their are within the repulsion zone, just add each other to
                                # the repulsion events
                                if distance < self.repulsion_radius:
                                    F_i.zor_update(r_ij)
                                    F_j.zor_update(r_ji)
                                    relationship_counted = True
                                elif distance < self.repulsion_radius + self.orientation_width + self.attraction_width:

                                    # if they are within the hollow balls of orientation and attraction zone, 
                                    # decide whether the fish can see each other
                                    angle_i = np.arccos(np.clip(np.dot(r_ij, v_i), -1.0, 1.0))
                                    angle_j = np.arccos(np.clip(np.dot(r_ji, v_j), -1.0, 1.0))

                                    if self.verbose:
                                        print("angle_i", angle_i, self.angle_of_perception)
                                        print("angle_j", angle_j, self.angle_of_perception)

                                    # if i can see j, add j's influence
                                    if angle_i < self.angle_of_perception:
                                        if distance < self.repulsion_radius + self.orientation_width:
                                            F_i.zoo_update(v_j)
                                        else:
                                            F_i.zoa_update(r_ij)

                                    # if j can see i, add i's influence
                                    if angle_j < self.angle_of_perception:
                                        if distance < self.repulsion_radius + self.orientation_width:
                                            F_j.zoo_update(v_i)
                                        else:
                                            F_j.zoa_update(r_ji)

                                    relationship_counted = True

            # for each fish
            for i in range(self.number_of_fish):

                F_i = self.fish[i]

                # evaluate the new demanded direction and reset the influence counters
                new_v = F_i.evaluate_direction(self.turning_rate*self.dt,self.noise_sigma)

                # evaluate the demanded positional change according to the direction
                dr = self.speed * new_v * self.dt

                # check for boundary conditions
                for dim in range(3):

                    # if new position would be out of boundaries
                    if dr[dim]+F_i.position[dim] > self.box_lengths[dim] or \
                       dr[dim]+F_i.position[dim] < 0.0:

                        # if this boundary is periodic
                        if not self.reflect_at_boundary[dim]:
                            if dr[dim]+F_i.position[dim] > self.box_lengths[dim]:
                                dr[dim] -= self.box_lengths[dim]
                            else:
                                dr[dim] += self.box_lengths[dim]
                        else:
                            # if this boundary is reflective
                            dr[dim] *= -1
                            new_v[dim] *= -1

                # update the position and direction
                F_i.position += dr
                F_i.direction = new_v

                # save position and direction
                positions[i,t,:] = F_i.position
                directions[i,t,:] = F_i.direction

            bar.update(t)

        return positions, directions


if __name__ == "__main__":

    swarm = Swarm(number_of_fish=2,speed=0.01,noise_sigma=0,turning_rate=0.1)

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



