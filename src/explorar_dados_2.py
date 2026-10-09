import pandas as pd

partidas = pd.read_csv("data/raw/campeonato-brasileiro-full.csv")

# Converte a coluna data de texto para data de verdade
partidas["data"] = pd.to_datetime(partidas["data"], format="%d/%m/%Y")
partidas["ano"] = partidas["data"].dt.year

print("Primeira data:", partidas["data"].min())
print("Última data:", partidas["data"].max())
print()

print("Jogos por ano:")
print(partidas["ano"].value_counts().sort_index())
print()

print("IDs repetidos:", partidas["ID"].duplicated().sum())
print("Linhas totalmente repetidas:", partidas.duplicated().sum())
print()

times = sorted(set(partidas["mandante"]) | set(partidas["visitante"]))
print(len(times), "nomes diferentes de times:")
print(times)
print()

print(partidas[["mandante_Placar", "visitante_Placar"]].describe())