from dataclasses import dataclass
import math


@dataclass(frozen=True, init=False)
class sphpoint:
    x: float
    y: float
    z: float
    R: float
    r: float
    theta: float
    phi: float

    def __init__(self, **kwargs):
        keys = set(kwargs.keys())

        # Cartesian
        if {"x", "y", "z"} <= keys:
            # Assign Cartesian
            x = kwargs["x"]
            y = kwargs["y"]
            z = kwargs["z"]
            
            # Assign Cylindrical
            phi = math.atan(y/x)
            r = math.sqrt(x**2 + y**2)
            
            # Assign Spherical
            R = math.sqrt(r**2 + z**2)
            theta = math.atan(r/z)
            

        # Cylindrical
        elif {"r", "phi", "z"} <= keys:
            r = kwargs["r"]
            phi = kwargs["phi"]
            z = kwargs["z"]

            if r < 0:
                raise ValueError("r must be non-negative")

            # Assign Cartesian
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            
            # Assign Spherical
            R = math.sqrt(r**2 + z**2)
            theta = math.atan(r/z)
            
        # Spherical
        elif {"R", "theta", "phi"} <= keys:
            R = kwargs["R"]
            theta = kwargs["theta"]
            phi = kwargs["phi"]

            if R < 0:
                raise ValueError("R must be non-negative")

            # Assign Cartesian
            x = R * math.sin(theta) * math.cos(phi)
            y = R * math.sin(theta) * math.sin(phi)
            z = R * math.cos(theta)
            
            # Assign Cylindrical
            r = math.sqrt(x**2 + y**2)

        else:
            raise TypeError(
                "Invalid constructor arguments. "
                "Use (x,y,z), (r,theta,z), or (R,theta,phi)."
            )

        if R == 0:
            theta = 0.0
            phi = 0.0
        else:
            theta = math.acos(z / R)
            phi = math.atan2(y, x) % (2 * math.pi)

        # Validation
        if not (0.0 <= theta <= math.pi):
            raise ValueError("theta must be in [0, pi]")
        if not (0.0 <= phi < 2 * math.pi):
            raise ValueError("phi must be in [0, 2*pi)")

        # Assign (bypassing frozen=True)
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "z", z)
        object.__setattr__(self, "r", r)
        object.__setattr__(self, "R", R)
        object.__setattr__(self, "theta", theta)
        object.__setattr__(self, "phi", phi)

    def __repr__(self) -> str:
        return (
            f"sphpoint("
            f"x={self.x:.6g}, y={self.y:.6g}, z={self.z:.6g}, "
            f"R={self.R:.6g}, r={self.r:.6g}, "
            f"theta={self.theta:.6g}, phi={self.phi:.6g})"
        )

 
@dataclass(frozen=True)
class sphvec:
    r: complex = 0.0 + 0.0j
    theta: complex = 0.0 + 0.0j
    phi: complex = 0.0 + 0.0j

    def magnitude(self) -> float:
        return abs(self.r)**2 + abs(self.theta)**2 + abs(self.phi)**2

    def __repr__(self) -> str:
        return (
            f"sphvec(Vr={self.r}, "
            f"Vtheta={self.theta}, "
            f"Vphi={self.phi})"
        )       