import numpy as np

from tools import rotation_matrix_weave

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
    R = np.eye(3) + np.sin(theta) * A + (1-np.cos(theta)) * A.dot(A)

    return R.dot(vi)


class Fish:

    self.position = np.zeros([0.,0.,0.])
    self.direction = np.zeros([0.,0.,0.])
    self.d_r = np.zeros([0.,0.,0.])
    self.d_o = np.zeros([0.,0.,0.])
    self.d_a = np.zeros([0.,0.,0.])

    self.n_r = 0
    self.n_a = 0
    self.n_o = 0

    def __init__(self,position=None,direction=None):

        if position is None:
            self.position = position
        else:
            self.position = np.random.randn(3)

        if direction is None:
            self.direction = direction / np.linalg.norm(direction)
        else:
            self.direction = np.random.randn(3)
            self.direction /= np.linalg.norm(self.direction)

    def reset(self):

        self.d_r = np.zeros([0.,0.,0.])
        self.d_o = np.zeros([0.,0.,0.])
        self.d_a = np.zeros([0.,0.,0.])
        self.n_r = 0
        self.n_a = 0
        self.n_o = 0

    def zor_update(self,r_ij):
        self.d_r += r_ij
        self.n_r += 1

    def zoo_update(self,v_j):
        self.d_o -= v_j
        self.n_o += 1

    def zoa_update(self,r_ij):
        self.d_a += r_ij
        self.n_a += 1

    def evaluate_diretion(self,thetatau,sigma):

        no_new_d = False

        if self.n_r > 0:
            new_d = self.d_r
        elif self.n_o > 0 and self.n_a > 0:
            new_d = 0.5*(self.d_o+self.d_a)
        else self.n_o > 0:
            new_d = self.d_o
        else self.n_a > 0:
            new_d = self.d_a
        else new_d == 0:
            no_new_d = True

        if no_new_d:
            new_d = self.direction

        self.new_d += sigma * np.random.randn(3)
        self.new_d /= np.linalg.norm(self.new_d)

        angle = np.arccos(np.clip(np.dot(self.new_d, self.direction), -1.0, 1.0))
        if angle < thetatau:
            self.direction = self.new_d
        else:
            self.direction = rotate_towards(vi, vf, thetatau)


    def make_step(self,speedtau):
        self.position += self.direction * speedtau



class simulation:

    def __init__(self,N,speed,tau,sigma):
        pass
