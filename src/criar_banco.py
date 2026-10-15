import sqlite3
from pathlib import Path

import pandas as pd

ARQUIVO_LIMPO = Path("data/processed/partidas_limpas.csv")
ARQUIVO_BANCO = Path("data/brasileirao.db")

SCHEMA = """
CREATE TABLE partidas (
    id INTEGER PRIMARY KEY,
    temporada INTEGER NOT NULL,
    rodada INTEGER NOT NULL,
    data TEXT NOT NULL,
    hora TEXT,
    mandante TEXT NOT NULL,
    visitante TEXT NOT NULL,
    formacao_mandante TEXT,
    formacao_visitante TEXT,
    tecnico_mandante TEXT,
    tecnico_visitante TEXT,
    vencedor TEXT,
    arena TEXT,
    mandante_placar INTEGER NOT NULL,
    visitante_placar INTEGER NOT NULL,
    mandante_estado TEXT,
    visitante_estado TEXT,
    total_gols INTEGER NOT NULL,
    resultado TEXT NOT NULL
        CHECK (resultado IN ('vitoria_mandante', 'empate', 'vitoria_visitante'))
);
"""


def main():
    partidas = pd.read_csv(ARQUIVO_LIMPO)
    partidas.columns = partidas.columns.str.lower()

    if ARQUIVO_BANCO.exists():
        ARQUIVO_BANCO.unlink()

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.executescript(SCHEMA)
    partidas.to_sql("partidas", conexao, if_exists="append", index=False)
    conexao.commit()

    total = conexao.execute("SELECT COUNT(*) FROM partidas").fetchone()[0]
    conexao.close()

    print(f"Banco criado em {ARQUIVO_BANCO} com {total} partidas")


if __name__ == "__main__":
    main()