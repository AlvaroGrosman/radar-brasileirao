import sqlite3

import pandas as pd

ARQUIVO_BANCO = "data/brasileirao.db"


def executar(sql):
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    resultado = pd.read_sql_query(sql, conexao)
    conexao.close()
    return resultado


CONSULTAS = {
    "1. Quanto vale jogar em casa? (resultados de todos os jogos)": """
        SELECT
            resultado,
            COUNT(*) AS jogos,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM partidas), 1) AS percentual
        FROM partidas
        GROUP BY resultado
        ORDER BY jogos DESC;
    """,
    "2. Média de gols por jogo em cada temporada": """
        SELECT
            temporada,
            ROUND(AVG(total_gols), 2) AS media_gols
        FROM partidas
        GROUP BY temporada
        ORDER BY temporada;
    """,
    "3. Top 5 times com mais vitórias em casa": """
        SELECT
            mandante AS time,
            COUNT(*) AS vitorias_em_casa
        FROM partidas
        WHERE resultado = 'vitoria_mandante'
        GROUP BY mandante
        ORDER BY vitorias_em_casa DESC
        LIMIT 5;
    """,
        "4. Aproveitamento em casa (times com pelo menos 100 jogos como mandante)": """
        SELECT
            mandante AS time,
            COUNT(*) AS jogos_em_casa,
            SUM(CASE WHEN resultado = 'vitoria_mandante' THEN 1 ELSE 0 END) AS vitorias,
            ROUND(
                100.0 * SUM(CASE WHEN resultado = 'vitoria_mandante' THEN 1 ELSE 0 END) / COUNT(*),
                1
            ) AS percentual_vitorias
        FROM partidas
        GROUP BY mandante
        HAVING COUNT(*) >= 100
        ORDER BY percentual_vitorias DESC
        LIMIT 10;
    """,
    "5. Mando de campo por temporada (% de vitórias do mandante e do visitante)": """
        SELECT
            temporada,
            ROUND(100.0 * SUM(CASE WHEN resultado = 'vitoria_mandante' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_mandante,
            ROUND(100.0 * SUM(CASE WHEN resultado = 'vitoria_visitante' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_visitante
        FROM partidas
        GROUP BY temporada
        ORDER BY temporada;
    """,
}


def main():
    for titulo, sql in CONSULTAS.items():
        print(titulo)
        print(executar(sql).to_string(index=False))
        print()


if __name__ == "__main__":
    main()