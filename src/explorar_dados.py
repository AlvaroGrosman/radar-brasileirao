import pandas as pd

partidas = pd.read_csv("data/raw/campeonato-brasileiro-full.csv")

print("Formato (linhas, colunas):", partidas.shape)
print()
print(partidas.head())
print()
partidas.info()
print()
print("Valores vazios por coluna:")
print(partidas.isna().sum())