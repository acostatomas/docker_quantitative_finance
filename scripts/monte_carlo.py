import sys
import platform
import json
import struct
from pathlib import Path

import numpy as np
import pandas as pd


NIVEL_CONFIANZA = 0.95
N_SIMULACIONES = 1_000_000
SEMILLA = 42
VALOR_PORTAFOLIO = 1_000_000.0

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "aapl_prices.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def cargar_retornos():
    data = pd.read_csv(DATA_FILE)
    precios = pd.to_numeric(data["Close"], errors="raise").dropna()
    return precios.pct_change().dropna()


def calcular_var_montecarlo(retornos):
    media = float(retornos.mean())
    sigma = float(retornos.std())

    rng = np.random.default_rng(SEMILLA)

    simulaciones = rng.normal(
        loc=media,
        scale=sigma,
        size=N_SIMULACIONES
    ).astype(np.float64)

    perdidas = -VALOR_PORTAFOLIO * simulaciones

    var_mc = np.percentile(
        perdidas,
        NIVEL_CONFIANZA * 100,
        method="linear"
    )

    return {
        "media": media,
        "sigma": sigma,
        "var_mc": float(var_mc),
        "n_simulaciones": N_SIMULACIONES,
        "semilla": SEMILLA,
    }


def guardar_resultados(resultados):
    with open(
        OUTPUT_DIR / "var_montecarlo_result.json",
        "w",
        encoding="utf-8",
        newline="\n"
    ) as f:
        json.dump(
            resultados,
            f,
            sort_keys=True,
            separators=(",", ":")
        )
        f.write("\n")

    with open(
        OUTPUT_DIR / "var_montecarlo_result.bin",
        "wb"
    ) as f:
        f.write(struct.pack(">d", resultados["media"]))
        f.write(struct.pack(">d", resultados["sigma"]))
        f.write(struct.pack(">d", resultados["var_mc"]))


def main():
    retornos = cargar_retornos()
    resultados = calcular_var_montecarlo(retornos)
    guardar_resultados(resultados)

    print("=" * 60)
    print("CASO C: VaR Monte Carlo")
    print("=" * 60)
    print(f"Simulaciones       : {resultados['n_simulaciones']}")
    print(f"Semilla            : {resultados['semilla']}")
    print(f"Media              : {resultados['media']!r}")
    print(f"Desvío             : {resultados['sigma']!r}")
    print(f"VaR Monte Carlo    : {resultados['var_mc']!r}")
    print("-" * 60)
    print(f"Python             : {sys.version}")
    print(f"Plataforma         : {platform.platform()}")
    print(f"NumPy              : {np.__version__}")
    print(f"Pandas             : {pd.__version__}")


if __name__ == "__main__":
    main()