# IAL D1 Papers

This sorts Edexcel IAL Decision Mathematics 1 (D1) past papers by topic. It was put together during IAS exams, with substantial help from Gemini, so the questions for one topic can be revised together instead of sitting by sitting.

The papers come from [Physics & Maths Tutor](https://www.physicsandmathstutor.com/a-level-maths-papers/d1-edexcel/). Each file is the question paper followed by the answer book.

*Unfortunately, the original program was lost. The .ipynb in this folder currently is a recreation of the original.

## Process

1. Collect the sittings from January 2020 to June 2024, including October 2021. That is 11 papers in `Past Papers`.
2. Take each numbered question as one item. Eight sittings have 7 questions, January 2023 has 6, and June 2020 and June 2023 have 8.
3. File that question, and the matching pages from the answer book, under one topic. Cover sheets and blank pages stay in the original paper.
4. Save one PDF per topic in `D1_Sorted_Final`.

`D1management.ipynb` reads the source PDFs in `Past Papers`, files each question by the verified topic map, and rebuilds the packs in `D1_Sorted_Final` (matching the existing products).

## Results

All **78** questions were filed, and each question appears in exactly one pack. Nothing was left in the original papers only, and nothing was copied into two topics.

The five packs are:

| Topic file | What was grouped here | Questions | Share | Pages |
| --- | --- | ---: | ---: | ---: |
| `Algorithms.pdf` | Sorting, bin packing, searching, and tracing an algorithm | 14 | 17.9% | 56 |
| `Critical Path Analysis.pdf` | Activity networks, precedence, early and late times, cascade charts | 19 | 24.4% | 60 |
| `Graph I.pdf` | Trees, Kruskal, Prim, and minimum spanning trees | 8 | 10.3% | 31 |
| `Graph II.pdf` | Shortest paths, route inspection, and the travelling salesperson problem | 20 | 25.6% | 81 |
| `Linear Programming.pdf` | Constraints, feasible regions, and optimisation | 17 | 21.8% | 68 |
| **Total** | | **78** | **100%** | **296** |

Graph II is the largest pack. Graph I is the smallest: four of the eleven sittings have no question in that pack.

Questions by sitting:

| Sitting | Questions | Algorithms | Critical path | Graph I | Graph II | Linear programming |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Jan 2020 | 7 | 1 | 2 | 1 | 2 | 1 |
| Jun 2020 | 8 | 1 | 2 | 1 | 2 | 2 |
| Jan 2021 | 7 | 2 | 1 | 0 | 2 | 2 |
| Jun 2021 | 7 | 2 | 2 | 1 | 2 | 0 |
| Oct 2021 | 7 | 1 | 1 | 1 | 2 | 2 |
| Jan 2022 | 7 | 1 | 2 | 1 | 2 | 1 |
| Jun 2022 | 7 | 1 | 2 | 1 | 1 | 2 |
| Jan 2023 | 6 | 1 | 1 | 1 | 2 | 1 |
| Jun 2023 | 8 | 2 | 2 | 0 | 2 | 2 |
| Jan 2024 | 7 | 1 | 2 | 0 | 2 | 2 |
| Jun 2024 | 7 | 1 | 2 | 1 | 1 | 2 |
| **Total** | **78** | **14** | **19** | **8** | **20** | **17** |

## Folder contents

- `Past Papers/`, the 11 source PDFs named by sitting (`Jan2020.pdf` through `Jun2024.pdf`, plus `Oct2021.pdf`)
- `D1_Sorted_Final/`, the five topic packs
- `D1management.ipynb`, which lists the source papers
