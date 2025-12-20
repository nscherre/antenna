from __future__ import annotations
from dataclasses import dataclass
from typing import overload
import math


@dataclass(frozen=True)
class Point3CartesianData:
    x: float
    y: float
    z: float

    @staticmethod
    def zero() -> Point3CartesianData:
        return Point3CartesianData(0, 0, 0)


@dataclass(frozen=True)
class Point3SphericalData:
    r: float
    theta: float
    phi: float

    @staticmethod
    def zero() -> Point3SphericalData:
        return Point3SphericalData(0, 0, 0)


class Point3:
    @overload
    def __init__(self, x: float, y: float, z: float) -> None: ...

    @overload
    def __init__(self, r: float, theta: float, phi: float) -> None: ...

    @overload
    def __init__(self) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        self._cartesian: Point3CartesianData | None = None
        self._spherical: Point3SphericalData | None = None

        keys = set(kwargs.keys())

        # Overload 2
        if {"r", "theta", "phi"} <= keys:
            self._spherical: Point3SphericalData | None = Point3SphericalData(
                r=kwargs.get("r"),
                theta=kwargs.get("theta"),
                phi=kwargs.get("phi"),
            )

        # Overload 1
        elif {"x", "y", "z"} <= keys:
            self._cartesian = Point3CartesianData(
                kwargs.get("x"), kwargs.get("y"), kwargs.get("z")
            )

        # Positional Args -> Cartesian
        elif len(args) == 3:
            self._cartesian = Point3CartesianData(args[0], args[1], args[2])

        # Zeros constructor
        elif len(args) == 0:
            self._cartesian = Point3CartesianData.zero()

        else:
            raise ValueError("No constructor signatures match the arguments provided.")

    def _generate_cartesian(self):
        if self._cartesian:
            return

        if self._spherical:
            x = (
                self._spherical.r
                * math.cos(self._spherical.phi)
                * math.cos(self._spherical.theta)
            )
            y = (
                self._spherical.r
                * math.cos(self._spherical.phi)
                * math.sin(self._spherical.theta)
            )
            z = self._spherical.r * math.sin(self._spherical.phi)
            self._cartesian = Point3CartesianData(x, y, z)
        else:
            self._cartesian = Point3CartesianData.zero()

    def _generate_spherical(self):
        if self._spherical:
            return

        if self._cartesian:
            x = self._cartesian.x
            y = self._cartesian.y
            z = self._cartesian.z

            r_xy = math.hypot(x, y)
            r = math.hypot(r_xy, z)

            if r == 0.0:
                theta = 0.0
                phi = 0.0
            else:
                theta = math.atan2(y, x) % (2 * math.pi)
                phi = math.atan2(z, r_xy)

            self._spherical = Point3SphericalData(r=r, theta=theta, phi=phi)
        else:
            self._spherical = Point3SphericalData.zero()

    @property
    def x(self) -> float:
        if not self._cartesian:
            self._generate_cartesian()

        return self._cartesian.x

    @property
    def y(self) -> float:
        if not self._cartesian:
            self._generate_cartesian()

        return self._cartesian.y

    @property
    def z(self) -> float:
        if not self._cartesian:
            self._generate_cartesian()

        return self._cartesian.z

    @property
    def r(self) -> float:
        if not self._spherical:
            self._generate_spherical()

        return self._spherical.r

    @property
    def theta(self) -> float:
        if not self._spherical:
            self._generate_spherical()

        return self._spherical.theta

    @property
    def phi(self) -> float:
        if not self._spherical:
            self._generate_spherical()

        return self._spherical.phi

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.z)

    @classmethod
    def from_cartesian(cls, x: float, y: float, z: float) -> Point3:
        return cls(x=x, y=y, z=z)

    @classmethod
    def from_spherical(
        cls, r: float, theta: float, phi: float, center: Point3 | None = None
    ) -> Point3:
        center = center or Point3(0, 0, 0)
        return cls(r=r, theta=theta, phi=phi)

    def clone(self) -> Point3:
        if self._cartesian or not self._spherical:
            return Point3(x=self.x, y=self.y, z=self.z)
        else:
            return Point3(r=self.r, theta=self.theta, phi=self.phi)

    def __add__(self, other: Point3) -> Point3:
        return Point3(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __sub__(self, other: Point3) -> Point3:
        return Point3(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def __mul__(self, other: Point3 | float) -> Point3:
        if isinstance(other, Point3):
            return Point3(
                x=self.x * other.x,
                y=self.y * other.y,
                z=self.z * other.z,
            )
        if self._spherical:
            return Point3(
                r=self._spherical.r * other,
                theta=self._spherical.theta,
                phi=self._spherical.phi,
            )
        return Point3(
            x=self.x * other,
            y=self.y * other,
            z=self.z * other,
        )

    def __truediv__(self, other: Point3 | float) -> Point3:
        if isinstance(other, Point3):
            return Point3(
                x=self.x / other.x,
                y=self.y / other.y,
                z=self.z / other.z,
            )
        if self._spherical:
            return Point3(
                r=self._spherical.r / other,
                theta=self._spherical.theta,
                phi=self._spherical.phi,
            )
        return Point3(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other,
        )

    def __div__(self, other: Point3 | float) -> Point3:
        return self.__truediv__(other)
