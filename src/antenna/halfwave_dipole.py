import cmath
import math

from dataclasses import dataclass

from antenna.spherical import Point3


@dataclass(frozen=True)
class sphvec:
    r: complex = 0.0 + 0.0j
    theta: complex = 0.0 + 0.0j
    phi: complex = 0.0 + 0.0j


def halfwave_dipole_E(p: Point3, I0: complex, k: float) -> sphvec:
    r = p.r

    if r <= 0:
        raise ValueError("r must be positive")

    # Polar angle from +z axis (dipole convention)
    cos_theta = p.z / r
    if cos_theta > 1.0:
        cos_theta = 1.0
    elif cos_theta < -1.0:
        cos_theta = -1.0
    theta = math.acos(cos_theta)

    if theta == 0.0 or theta == math.pi:
        return sphvec()

    pattern = math.cos((math.pi / 2) * math.cos(theta)) / math.sin(theta)
    phase = cmath.exp(-1j * k * r) / r

    E_theta = 1j * 60 * I0 * pattern * phase

    return sphvec(r=0.0 + 0.0j, theta=E_theta, phi=0.0 + 0.0j)
