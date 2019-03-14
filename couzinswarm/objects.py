import numpy as np

def rotate_towards(vi, vf, theta):
    x = np.cross(vi, vf)
    _x_ = np.linalg.norm(x)
    if _x_ < 1e-15:
        return vi
    else:
        x /= _x_
    A = np.array([[ 0, -x[2], x[1] ],
                  [ x[2], 0, -x[0] ],
                  [ -x[1], x[0], 0 ]])
    c, s = np.cos(theta), np.sin(theta)
    R = np.eye(3) + np.sin(theta) * A + (1-np.cos(theta)) * A.dot(A)

    return R.dot(vi)


class Fish:

    position = np.zeros(3)
    direction = np.zeros(3)
    d_r = np.zeros(3)
    d_o = np.zeros(3)
    d_a = np.zeros(3)

    n_r = 0
    n_a = 0
    n_o = 0

    def __init__(self,position,direction=None,ID=None,verbose=False):

        self.position = position

        if direction is None:
            self.direction = np.random.randn(3)
            self.direction /= np.linalg.norm(self.direction)
        else:
            self.direction = direction / np.linalg.norm(direction)

        self.ID = ID
        self.verbose = verbose

    def reset(self):

        self.d_r = np.zeros(3,dtype=float)
        self.d_o = np.zeros(3,dtype=float)
        self.d_a = np.zeros(3,dtype=float)
        self.n_r = 0
        self.n_a = 0
        self.n_o = 0

    def zor_update(self,r_ij):
        self.d_r = self.d_r - r_ij
        self.n_r += 1

    def zoo_update(self,v_j):
        self.d_o = self.d_o + v_j
        self.n_o += 1

    def zoa_update(self,r_ij):
        self.d_a += self.d_a + r_ij
        self.n_a += 1

    def evaluate_direction(self,thetatau,sigma):

        no_new_d = False

        if self.n_r > 0:
            new_d = self.d_r
        elif self.n_o > 0 and self.n_a > 0:
            new_d = 0.5*(self.d_o+self.d_a)
        elif self.n_o > 0:
            new_d = self.d_o
        elif self.n_a > 0:
            new_d = self.d_a
        else:
            new_d = self.direction

        if self.verbose:
            print("Fish", self.ID)
            print("    direction:", self.direction)
            print("    repulsion:", self.n_r, self.d_r)
            print("    orientation:", self.n_o, self.d_o)
            print("    attraction:", self.n_a, self.d_a)
            print("    new_d:",new_d)

        self.new_d = new_d + sigma * np.random.randn(3)
        self.new_d /= np.linalg.norm(self.new_d)

        angle = np.arccos(np.clip(np.dot(self.new_d, self.direction), -1.0, 1.0))
        if angle > thetatau:
            self.new_d = rotate_towards(self.direction, self.new_d, thetatau)


        if self.verbose:
            print("    after noise and rotation:",new_d)
