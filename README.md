# Experimento: reproducibilidad de modelos financieros con Docker

Este proyecto contiene los dos casos del experimento:

- **Caso A** (`scripts/black_scholes.py`): valuación de una opción call
  europea con Black-Scholes.
- **Caso B** (`scripts/var_historico.py`): cálculo de VaR histórico
  sobre una serie de precios.

## Paso 1 — Correr en tu entorno local "sin control"

Esto simula el escenario de un investigador que corre el modelo tal
como tiene instalado Python en su máquina, sin fijar versiones.

```bash
cd docker-repro-finanzas
python3 -m venv venv_local
source venv_local/bin/activate      # en Windows: venv_local\Scripts\activate

# Sin fijar versiones - instala lo último disponible
pip install numpy pandas scipy yfinance

python scripts/black_scholes.py > resultados_local.txt
python scripts/var_historico.py >> resultados_local.txt

cat resultados_local.txt
```

Guardá `resultados_local.txt` — es tu primer punto de comparación.
Repetí este mismo paso en otra máquina (o en varios momentos del
tiempo, si en el medio actualizás alguna librería) para tener más
de un "entorno no controlado" con el que comparar.

## Paso 2 — Correr en el contenedor Docker (entorno controlado)

```bash
docker build -t docker-repro-finanzas .
docker run --rm docker-repro-finanzas > resultados_docker.txt
cat resultados_docker.txt
```

Repetí este `docker run` en otra máquina con Docker instalado (o
incluso varias veces en la misma) — la hipótesis es que
`resultados_docker.txt` debería ser idéntico en todos los casos,
porque la imagen fija el sistema operativo base, la versión exacta
de Python y las versiones exactas de cada librería.

## Paso 3 — Comparar

```bash
diff resultados_local.txt resultados_docker.txt
```

Para el paper, lo que te interesa documentar es:

1. **Divergencia numérica**: ¿en qué cifra decimal empiezan a diferir
   los resultados de Black-Scholes y del VaR entre el entorno local y
   el contenedor (o entre dos corridas locales en distintos momentos)?
2. **Versiones detectadas**: cada script imprime las versiones de
   NumPy/SciPy/Pandas que usó — comparalas entre corridas.
3. **Tiempo de setup**: cronometrá cuánto tarda cada método
   (`time pip install ...` vs `time docker build ...`) — es una
   métrica de reproducibilidad práctica, no solo numérica.

## Nota sobre `yfinance`

Si no hay conexión a internet disponible (o Yahoo Finance no
responde), `var_historico.py` genera automáticamente una serie de
precios sintética con semilla fija, para que el experimento pueda
correrse igual. Esto queda indicado en la salida del script
(campo "Fuente de datos").