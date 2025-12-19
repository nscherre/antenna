import math
import cmath
from antenna.spherical import sphpoint, sphvec


def halfwave_dipole_E(
    p: sphpoint,
    I0: complex,
    k: float
) -> sphvec:

    r = p.r
    theta = p.theta

    if r <= 0:
        raise ValueError("r must be positive")

    if theta == 0.0 or theta == math.pi:
        return sphvec()

    pattern = math.cos((math.pi / 2) * math.cos(theta)) / math.sin(theta)
    phase = cmath.exp(-1j * k * r) / r

    E_theta = 1j * 60 * I0 * pattern * phase

    return sphvec(
        r=0.0 + 0.0j,
        theta=E_theta,
        phi=0.0 + 0.0j
    )