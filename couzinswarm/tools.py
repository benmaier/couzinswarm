"""
Tool module
===========

Contains some useful numerical tools
"""

import numpy as np

def rotate_towards(vi, vf, theta):
    """
    Rotate a vector `vi` towards another vector `vf` by angle `theta`.
    Return the rotated vector.
    """
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
    R = np.eye(3) + s * A + (1-c) * A.dot(A)

    return R.dot(vi)

def cart2sphere(v):
    """
    Return the spherical angles `theta` and `phi` associated with a unit vector `v`.
    """
    # v needs to be a unit vector
    x,y,z = v
    theta = np.arccos(np.clip(z,-1,1))
    phi = np.arctan2(x,y)

    return theta, phi


def sphere2cart(theta, phi):
    """
    Return the unit vector `v` associated with angles `theta` and `phi`.
    Adjusts `theta` and `phi` such that the transformation is valid
    """
    if theta < 0:
        theta = np.pi + theta
        phi += np.pi
    elif theta > np.pi:
        theta = theta - np.pi
        phi += np.pi
    st, sp = np.sin(theta), np.sin(phi)
    ct, cp = np.cos(theta), np.cos(phi)
    x = st * sp
    y = st * cp
    z = ct

    return np.array([x,y,z])
        

if __name__=="__main__":

    v = np.array([1.,0,0])

    th, ph = cart2sphere(v)
    print(th, ph)

    v_ = sphere2cart(th,ph)

    print(v, v_)

