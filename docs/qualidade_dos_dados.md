# Notas sobre a qualidade dos dados

Fonte: [adaoduque/Brasileirao_Dataset](https://github.com/adaoduque/Brasileirao_Dataset) (Brasileirão 2003–2024).

## Verificações feitas
- 8.785 partidas, sem IDs ou linhas duplicadas.
- Jogos por temporada conferem com o formato de cada época: 552 (2003–2004), 462 (2005) e 380 (2006–2024), com exceção de 2016, que tem 379.
- Nomes de times padronizados (45 nomes distintos).
- Placares sem valores absurdos (mínimo 0, máximo 7).

## Decisões e limitações conhecidas
- A coluna `rodata` foi renomeada para `rodada`.
- O ano da data não é igual à temporada: 112 jogos da temporada 2020 foram disputados em 2021. Criamos a coluna `temporada`.
- Formações e técnicos têm mais da metade dos valores vazios (concentrados nos anos mais antigos). Foram mantidos vazios.
- `Barueri` e `Gremio Prudente` parecem ser o mesmo clube em fases diferentes; foram mantidos separados.
- Brasiliense 0 x 1 Vasco (24/04/2005): o jogo terminou 2 x 2 em campo, mas o STJD alterou o resultado para 1 x 0. A coluna `vencedor` indica empate, enquanto `resultado` (derivada do placar) segue o resultado oficial. Usamos `resultado`.