"""Courbes de résonance d'un circuit RLC série (régime sinusoïdal forcé), recréées en 2026.

u_C = E / (1 − x² + j·x/Q), x = ω/ω₀ ; i = jCω·u_C.
- résonance en intensité en x = 1 quel que soit Q, bande passante Δx = 1/Q ;
- résonance en tension seulement si Q > 1/√2, en x = √(1 − 1/(2Q²)).
Valeurs du montage du TP : L = 0,1 H, C = 100 nF, R_t = R + 50 Ω (générateur) ; R = 100 Ω → Q ≈ 6,67, R = 10 kΩ → Q ≈ 0,1.
"""
import numpy as np
import matplotlib.pyplot as plt

L, C, RG = 0.1, 100e-9, 50.0
w0 = 1 / np.sqrt(L * C)
x = np.linspace(1e-3, 3, 3000)

if __name__ == "__main__":
    for R in (100, 10_000):
        Q = np.sqrt(L / C) / (R + RG)
        res = f"x_r = {np.sqrt(1 - 1 / (2 * Q * Q)):.4f}" if Q > 1 / np.sqrt(2) else "pas de résonance en tension"
        print(f"R = {R:>6} Ω : f0 = {w0 / (2 * np.pi):.1f} Hz, Q = {Q:.4f}, bande passante = {w0 / Q / (2 * np.pi):.1f} Hz, {res}")
    fig, ax = plt.subplots(1, 3, figsize=(14, 4))
    for Q in (0.1, 0.5, 1, 2, 3, 5, 6.67):
        g = 1 / np.sqrt((1 - x**2) ** 2 + (x / Q) ** 2)
        ax[0].plot(x, g, label=f"Q = {Q}")
        ax[1].plot(x, 1 / np.sqrt(1 + Q**2 * (x - 1 / x) ** 2))
        ax[2].plot(x, -np.arctan2(x / Q, 1 - x**2))
    ax[0].set_title("$U_{Cm}/E_m$"); ax[1].set_title("$I_m/I_{max}$"); ax[2].set_title("déphasage de $u_C$ (rad)")
    ax[1].axhline(1 / np.sqrt(2), ls="--", c="k", lw=0.8)
    for a in ax:
        a.set_xlabel("$x = \\omega/\\omega_0$"); a.grid(alpha=0.3)
    ax[0].legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("../images/resonance-2026.png", dpi=130)
