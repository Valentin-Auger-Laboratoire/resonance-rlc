"""Régime libre d'un circuit RLC série : u_C(t) pour plusieurs facteurs de qualité.

Recréé en 2026 : le script d'origine (TP de physique, CPGE TSI, mars 2024) est perdu. Il traçait
« Évolution temporelle de u_C pour différents facteurs de qualité » avec Q = 0,1 ; 0,5 et 100
(voir images/ecran-script-2024.jpg). Cette version reprend la même figure avec les valeurs du montage
du TP (L = 0,1 H, C = 100 nF) : le condensateur, chargé sous E, se décharge dans le circuit.

Méthode : équation L·di/dt = −R·i − u_C, C·du_C/dt = i, résolue par Runge-Kutta d'ordre 4 et comparée
à la solution exacte (l'écart maximal est affiché).
"""
import numpy as np
import matplotlib.pyplot as plt

L, C, E = 0.1, 100e-9, 5.0
w0 = 1 / np.sqrt(L * C)


def rk4(R, t1, dt):
    n = int(round(t1 / dt))
    uc, i = E, 0.0
    t = np.linspace(0, n * dt, n + 1)
    out = np.empty(n + 1)
    out[0] = uc
    f = lambda u, j: (j / C, (-R * j - u) / L)
    for k in range(n):
        a = f(uc, i)
        b = f(uc + dt / 2 * a[0], i + dt / 2 * a[1])
        c = f(uc + dt / 2 * b[0], i + dt / 2 * b[1])
        d = f(uc + dt * c[0], i + dt * c[1])
        uc += dt / 6 * (a[0] + 2 * b[0] + 2 * c[0] + d[0])
        i += dt / 6 * (a[1] + 2 * b[1] + 2 * c[1] + d[1])
        out[k + 1] = uc
    return t, out


def exact(R, t):
    a = R / (2 * L)
    if a < w0:
        wd = np.sqrt(w0**2 - a**2)
        return E * np.exp(-a * t) * (np.cos(wd * t) + a / wd * np.sin(wd * t))
    if a > w0:
        s = np.sqrt(a**2 - w0**2)
        r1, r2 = -a + s, -a - s
        return E * (r1 * np.exp(r2 * t) - r2 * np.exp(r1 * t)) / (r1 - r2)
    return E * (1 + a * t) * np.exp(-a * t)


if __name__ == "__main__":
    t1, dt = 0.008, 1e-6
    plt.figure(figsize=(9, 5))
    for Q in (0.1, 0.5, 100):
        R = np.sqrt(L / C) / Q
        t, uc = rk4(R, t1, dt)
        err = np.max(np.abs(uc - exact(R, t)))
        print(f"Q = {Q:>5} : R = {R:8.1f} Ω, écart Runge-Kutta / solution exacte = {err:.1e} V")
        plt.plot(t * 1e3, uc, label=f"Q = {Q}")
    plt.title("Évolution temporelle de $u_C$ pour différents facteurs de qualité")
    plt.xlabel("t (ms)")
    plt.ylabel("$u_C$ (V)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("../images/regime-libre-2026.png", dpi=130)
