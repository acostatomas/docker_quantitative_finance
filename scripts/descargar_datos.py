from pathlib import Path
import yfinance as yf
import pandas as pd

TICKER = "AAPL"
DIAS_HISTORIA = 500

# Ruta del proyecto/data
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARCHIVO = DATA_DIR / "aapl_prices.csv"

DATA_DIR.mkdir(exist_ok=True)

print(f"Descargando {TICKER}...")

data = yf.download(
    TICKER,
    period=f"{DIAS_HISTORIA}d",
    progress=False,
    auto_adjust=False
)

if data.empty:
    raise RuntimeError("No se pudieron descargar datos de Yahoo Finance.")

# yfinance puede devolver distintas estructuras según su versión.
# Nos aseguramos de quedarnos solamente con Close como serie 1D.
close = data["Close"]

if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

close = close.dropna()
close.name = "Close"

close.to_csv(ARCHIVO, index=True)

print(f"Datos guardados en: {ARCHIVO}")
print(f"Observaciones: {len(close)}")