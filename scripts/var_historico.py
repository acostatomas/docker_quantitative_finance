"""
Caso B: Value at Risk (VaR) histórico sobre una serie de precios.

Objetivo del experimento: a diferencia de Black-Scholes, acá la
posible divergencia entre entornos no viene de la aleatoriedad ni
de funciones trascendentales, sino del propio *método de cálculo
del percentil*. Tanto NumPy como Pandas ofrecen varios métodos de
interpolación para calcular percentiles (linear, lower, higher,
midpoint, nearest), y el método por defecto puede cambiar entre
versiones de la librería sin que el usuario lo note, ya que el
código luce idéntico.

Por defecto, este script intenta descargar una serie real de
precios con `yfinance`. Si no hay conexión a internet disponible
(por ejemplo, corriendo en un entorno restringido), genera una
serie sintética con una semilla fija, de forma que el experimento
pueda correrse igual en cualquier entorno.
"""

import sys
import platform
from pathlib import Path

import numpy as np
import pandas as pd

import json
import struct


NIVEL_CONFIANZA = 0.95

BASE_DIR = Path(__file__).resolve().parent.parent
ARCHIVO_DATOS = BASE_DIR / "data" / "aapl_prices.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def cargar_precios() -> pd.Series:
    """Carga el dataset fijo utilizado en todas las ejecuciones."""

    data = pd.read_csv(ARCHIVO_DATOS)

    if "Close" not in data.columns:
        raise ValueError("El archivo no contiene una columna 'Close'.")

    precios = pd.to_numeric(data["Close"], errors="raise")

    return precios.dropna()


def calcular_var_historico(
    precios: pd.Series,
    nivel_confianza: float
) -> dict:

    retornos = precios.pct_change().dropna()

    percentil = (1 - nivel_confianza) * 100

    # Tres implementaciones para observar posibles diferencias
    # entre versiones de las librerías.
    var_numpy_default = np.percentile(
        retornos,
        percentil
    )

    var_numpy_linear = np.percentile(
        retornos,
        percentil,
        method="linear"
    )

    var_pandas_default = retornos.quantile(
        1 - nivel_confianza
    )

    return {
        "n_observaciones": len(retornos),
        "media_retorno": retornos.mean(),
        "desvio_retorno": retornos.std(),
        "var_numpy_default": var_numpy_default,
        "var_numpy_linear": var_numpy_linear,
        "var_pandas_default": var_pandas_default,
    }


def main():

    precios = cargar_precios()

    resultados = calcular_var_historico(
        precios,
        NIVEL_CONFIANZA
    )
    # Resultado legible
    resultado_exportable = {
        "n_observaciones": resultados["n_observaciones"],
        "media_retorno": float(resultados["media_retorno"]),
        "desvio_retorno": float(resultados["desvio_retorno"]),
        "var_numpy_default": float(resultados["var_numpy_default"]),
        "var_numpy_linear": float(resultados["var_numpy_linear"]),
        "var_pandas_default": float(resultados["var_pandas_default"]),
    }

    with open(
        OUTPUT_DIR / "var_result.json",
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


    # Resultado binario para comparación bit-a-bit
    with open(OUTPUT_DIR / "var_result.bin", "wb") as f:
        f.write(struct.pack(">q", resultados["n_observaciones"]))

        for clave in (
            "media_retorno",
            "desvio_retorno",
            "var_numpy_default",
            "var_numpy_linear",
            "var_pandas_default",
        ):
            f.write(struct.pack(">d", float(resultados[clave])))
    print("=" * 60)
    print("CASO B: VaR histórico")
    print("=" * 60)

    print("Fuente de datos     : dataset fijo (AAPL)")
    print(f"Archivo             : {ARCHIVO_DATOS.name}")
    print(f"Observaciones       : {resultados['n_observaciones']}")
    print(
        f"Nivel de confianza  : "
        f"{NIVEL_CONFIANZA * 100:.0f}%"
    )

    print("-" * 60)

    print(
        f"Media retorno diario  = "
        f"{resultados['media_retorno']!r}"
    )

    print(
        f"Desvío retorno diario = "
        f"{resultados['desvio_retorno']!r}"
    )

    print("-" * 60)

    print(
        f"VaR (np.percentile, default) = "
        f"{resultados['var_numpy_default']!r}"
    )

    print(
        f"VaR (np.percentile, linear)  = "
        f"{resultados['var_numpy_linear']!r}"
    )

    print(
        f"VaR (pandas .quantile)       = "
        f"{resultados['var_pandas_default']!r}"
    )

    print("-" * 60)

    print("Entorno de ejecución:")
    print(f"  Python    : {sys.version}")
    print(f"  Plataforma: {platform.platform()}")
    print(f"  NumPy     : {np.__version__}")
    print(f"  Pandas    : {pd.__version__}")

    print("=" * 60)


if __name__ == "__main__":
    main()