import math
import unittest
from dataclasses import FrozenInstanceError

from antenna.spherical import Point3, Point3CartesianData, Point3SphericalData


class TestPoint3DataClasses(unittest.TestCase):
    def test_cartesian_zero_helpers(self) -> None:
        z1 = Point3CartesianData.zero()
        z2 = Point3CartesianData.zero()
        self.assertEqual(z1, z2)
        self.assertEqual((z1.x, z1.y, z1.z), (0.0, 0.0, 0.0))

    def test_spherical_zero_helpers(self) -> None:
        z1 = Point3SphericalData.zero()
        z2 = Point3SphericalData.zero()
        self.assertEqual(z1, z2)
        self.assertEqual((z1.r, z1.theta, z1.phi), (0.0, 0.0, 0.0))

    def test_cartesian_frozen(self) -> None:
        p = Point3CartesianData(1.0, 2.0, 3.0)
        with self.assertRaises(FrozenInstanceError):
            p.x = 9.0  # type: ignore[misc]

    def test_spherical_frozen(self) -> None:
        s = Point3SphericalData(1.0, 2.0, 3.0)
        with self.assertRaises(FrozenInstanceError):
            s.r = 9.0  # type: ignore[misc]


class TestPoint3Conversions(unittest.TestCase):
    def assertAlmostEqualRel(
        self, a: float, b: float, *, rel: float = 1e-12, abs_: float = 1e-12
    ) -> None:
        self.assertTrue(
            math.isclose(a, b, rel_tol=rel, abs_tol=abs_), msg=f"{a} != {b}"
        )

    def test_default_constructor_is_origin(self) -> None:
        p = Point3()
        self.assertEqual((p.x, p.y, p.z), (0.0, 0.0, 0.0))
        self.assertEqual((p.r, p.theta, p.phi), (0.0, 0.0, 0.0))

    def test_cartesian_constructor_kwargs(self) -> None:
        p = Point3(x=1.0, y=2.0, z=3.0)
        self.assertEqual((p.x, p.y, p.z), (1.0, 2.0, 3.0))

    def test_cartesian_constructor_positional(self) -> None:
        p = Point3(1.0, 2.0, 3.0)
        self.assertEqual((p.x, p.y, p.z), (1.0, 2.0, 3.0))

    def test_spherical_to_cartesian_matches_generate_cartesian(self) -> None:
        r = 2.0
        theta = math.pi / 3
        phi = math.pi / 6
        p = Point3(r=r, theta=theta, phi=phi)

        x_exp = r * math.cos(phi) * math.cos(theta)
        y_exp = r * math.cos(phi) * math.sin(theta)
        z_exp = r * math.sin(phi)

        self.assertAlmostEqualRel(p.x, x_exp)
        self.assertAlmostEqualRel(p.y, y_exp)
        self.assertAlmostEqualRel(p.z, z_exp)

    def test_cartesian_to_spherical_matches_generate_spherical(self) -> None:
        x = 1.0
        y = 1.0
        z = math.sqrt(2.0)
        p = Point3(x=x, y=y, z=z)

        r_exp = math.sqrt(x * x + y * y + z * z)
        theta_exp = math.atan2(y, x) % (2 * math.pi)
        phi_exp = math.atan2(z, math.hypot(x, y))

        self.assertAlmostEqualRel(p.r, r_exp)
        self.assertAlmostEqualRel(p.theta, theta_exp)
        self.assertAlmostEqualRel(p.phi, phi_exp)

    def test_theta_wrapping_is_0_to_2pi(self) -> None:
        p = Point3(x=0.0, y=-1.0, z=0.0)
        self.assertAlmostEqualRel(p.theta, 3 * math.pi / 2)

    def test_round_trip_cartesian_spherical_cartesian(self) -> None:
        p1 = Point3(x=0.3, y=-0.4, z=0.5)
        p2 = Point3(r=p1.r, theta=p1.theta, phi=p1.phi)

        self.assertAlmostEqualRel(p2.x, p1.x)
        self.assertAlmostEqualRel(p2.y, p1.y)
        self.assertAlmostEqualRel(p2.z, p1.z)

    def test_scalar_mul_uses_cached_spherical_when_present(self) -> None:
        p = Point3(r=2.0, theta=0.7, phi=-0.4)
        self.assertIsNotNone(p._spherical)
        self.assertIsNone(p._cartesian)

        q = p * 3.0
        self.assertIsNotNone(q._spherical)
        self.assertIsNone(q._cartesian)
        self.assertAlmostEqualRel(q.r, 6.0)
        self.assertAlmostEqualRel(q.theta, p.theta)
        self.assertAlmostEqualRel(q.phi, p.phi)

    def test_scalar_div_uses_cached_spherical_when_present(self) -> None:
        p = Point3(r=8.0, theta=1.2, phi=0.3)
        self.assertIsNotNone(p._spherical)
        self.assertIsNone(p._cartesian)

        q = p / 2.0
        self.assertIsNotNone(q._spherical)
        self.assertIsNone(q._cartesian)
        self.assertAlmostEqualRel(q.r, 4.0)
        self.assertAlmostEqualRel(q.theta, p.theta)
        self.assertAlmostEqualRel(q.phi, p.phi)


if __name__ == "__main__":
    unittest.main()
