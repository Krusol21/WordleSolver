<!-- README.md -->

# **Wordle‑AI — Python Playground for Solvers and Statistics**

Wordle‑AI is a self‑contained collection of scripts that

* emulate the original **Wordle** game in the terminal,  
* provide two interchangeable solver bots  
  * **Entropy Guesser** – Expected‑information minimizer  
  * **Heuristic Guesser** – “use new letters first, favor yellows” with random tie‑break  
* prune candidate word lists with a fast, standalone filter,  
* benchmark thousands of start words in parallel and plot the results, and  
* ship the full **NYT target list** (`wordle_targets.txt`) plus the extended **valid‑guess list** (`wordle_possibles.txt`).

Everything runs on plain Python ≥ 3.12—no web APIs, no obscure native extensions.

---

## 📂 Project layout

| Path                                | Purpose                                                                                                 |
|-------------------------------------|---------------------------------------------------------------------------------------------------------|
| **`wordle.py`**                     | Interactive “human‑plays‑vs‑secret” emulator with color feedback.                                      |
| **`guesser_entropy.py`**            | Bot #1 — exhaustive expected‑survivor search with memoization.                                          |
| **`guesser.py`**                    | Bot #2 — lightweight heuristic: maximize new letters, prefer words containing confirmed yellows.        |
| **`pruning.py`**                    | Core pruning routine (green/yellow/gray logic).                                                         |
| **`word_lists.py`**                 | Helpers: pick random target, validate guesses.                                                          |
| **`wordle_heavy_computation.py`**   | Multiprocessing simulator — produces pickle stats & PNG bar charts.                                     |
| **`wordle_viz*.ipynb`**             | Jupyter notebooks for ad‑hoc visual exploration (optional).                                             |
| **`wordle_targets.txt`**            | 2309 official answer words.                                                                            |
| **`wordle_possibles.txt`**          | 10k + allowable guess words (answers + NYT “plausible” list).                                           |

---

## 🛠 Installation

```bash
git clone https://github.com/Krusol21/WordleSolver
pip install -r requirements.txt