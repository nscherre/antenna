from dataclasses import dataclass
import math

@dataclass(frozen = True)
class sphpoint:
    r: float
    theta: float
    phi: float
    
    def __post_init__(self):
        if self.r < 0:
            raise ValueError("Radius r must be non-negative")
        if not (0.0 <= self.theta <= math.pi):
            raise ValueError("Theta must be in [0, pi]")
        if not (0.0 <= self.phi < 2 * math.pi):
            raise ValueError("Phi must be in [0, 2*pi)")
    
    def __repr__(self) -> str:
        return (
            f"SphericalVector(r={self.r:.6g}, "
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