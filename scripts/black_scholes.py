"""
Caso A: Valuación de una opción call europea mediante Black-Scholes.

Parámetros fijos:
S0 = 100
K = 105
T = 1.0
r = 0.05
sigma = 0.20
"""

import sys
import platform
import json
import struct
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import norm


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def black_scholes_call(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float
):
    """Precio de una opción call europea según Black-Scholes."""

    d1 = (
        np.log(S0 / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * np.sqrt(T))

    d2 = d1 - sigma * np.sqrt(T)

    precio = (
        S0 * norm.cdf(d1)
        - K * np.exp(-r * T) * norm.cdf(d2)
    )

    return precio, d1, d2


def guardar_resultados(precio, d1, d2):
    """
    Guarda los resultados en:
    - JSON: formato legible.
    - BIN: representación binaria float64 para comparar bit-a-bit.
    """

    resultado_exportable = {
        "d1": float(d1),
        "d2": float(d2),
        "precio_call": float(precio),
    }

    # Archivo legible
    with open(
        OUTPUT_DIR / "black_scholes_result.json",
        "w",
        encoding="utf-8",
        newline="\n"
    ) as f:
        json.dump(
            resultado_exportable,
            f,
            sort_keys=True,
            separators=(",", ":")
        )
        f.write("\n")

    # Archivo binario determinístico
    with open(
        OUTPUT_DIR / "black_scholes_result.bin",
        "wb"
    ) as f:
        f.write(
            struct.pack(
                ">ddd",
                float(d1),
                float(d2),
                float(precio)
            )
        )


def main():
    # Parámetros fijos del experimento
    S0 = 100.0
    K = 105.0
    T = 1.0
    r = 0.05
    sigma = 0.20

    precio, d1, d2 = black_scholes_call(
        S0,
        K,
        T,
        r,
        sigma
    )

    # Generación de outputs experimentales
    guardar_resultados(precio, d1, d2)

    print("=" * 60)
    print("CASO A: Black-Scholes - Valuación de opción call europea")
    print("=" * 60)
    print(
        f"Parámetros: S0={S0}, K={K}, T={T}, "
        f"r={r}, sigma={sigma}"
    )
    print("-" * 60)

    print(f"d1                  = {d1!r}")
    print(f"d2                  = {d2!r}")
    print(f"Precio de la opción = {precio!r}")

    print("-" * 60)
    print("Entorno de ejecución:")
    print(f"  Python    : {sys.version}")
    print(f"  Plataforma: {platform.platform()}")
    print(f"  NumPy     : {np.__version__}")
    print(f"  SciPy     : {scipy.__version__}")
    print("=" * 60)


if __name__ == "__main__":
    main()