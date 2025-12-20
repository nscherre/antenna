from antenna.spherical import sphpoint
from antenna.halfwave_dipole import halfwave_dipole_E
import math
import numpy as np
import matplotlib.pyplot as plt


# Dipole / wave parameters
I0 = 1.0 + 0.0j        # feed current (phasor)
lam = 1.0             # wavelength (meters)
k = 2 * math.pi / lam

# Observation radius (far-field)
r = 100.0

# Theta sweep (avoid singularities at 0 and pi)
theta = np.linspace(1e-3, math.pi - 1e-3, 1000)

E_mag = np.zeros_like(theta)

for i, th in enumerate(theta):
    p = sphpoint(r=r, theta=th, phi=0.0)
    E = halfwave_dipole_E(p, I0, k)
    E_mag[i] = abs(E.theta)

E_mag /= E_mag.max()

plt.figure()
ax = plt.subplot(111, polar=True)

ax.plot(theta, E_mag)
ax.set_title("Half-Wave Dipole Radiation Pattern (Normalized)", pad=20)

plt.savefig("plot.png")