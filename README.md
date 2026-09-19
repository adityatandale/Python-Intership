# Python-Intership
# Python Internship Projects

A collection of six small, interactive Python applications built with [Streamlit](https://streamlit.io/) as part of an internship. Each task lives in its own folder with its source code, a task-level README, and a screenshot of the running app.

## Projects at a Glance

| # | Project | What it does | Key libraries |
|---|---------|--------------|---------------|
| 1 | [To-Do List Application](#task-1--to-do-list-application) | Add, complete, delete, and filter tasks | `streamlit` |
| 2 | [Guess the Number Game](#task-2--guess-the-number-game) | Number guessing with hints and difficulty levels | `streamlit`, `random` |
| 3 | [Basic File Handling](#task-3--basic-file-handling) | Read a text file, find and replace text, save the result | `streamlit`, `re`, `os` |
| 4 | [Basic Web Scraper](#task-4--basic-web-scraper) | Extract headlines or text from a webpage | `requests`, `beautifulsoup4`, `pandas` |
| 5 | [Currency Converter](#task-5--currency-converter) | Convert currencies using live exchange rates | `requests` |
| 6 | [Word Count Tool](#task-6--word-count-tool) | Word, line, and character counts plus a frequency chart | `pandas`, `collections` |

## Repository Structure

```
Intership/
├── Task 1 To-Do List Application/
│   ├── todo_list.py
│   ├── README_todo_list.md
│   └── Screenshot 2026-08-08 222207.png
├── Task 2 Guess The Number Game/
│   ├── guess_number.py
│   ├── README_guess_number.md
│   └── Screenshot 2026-08-08 222301.png
├── Task 3 Basic File Handling/
│   ├── file_handler.py
│   ├── README_file_handler.md
│   └── Screenshot 2026-08-08 222400.png
├── Task 4 Basic Web Scraper/
│   ├── web_scraper.py
│   ├── README_web_scraper.md
│   └── Screenshot 2026-08-08 222843.png
├── Task 5 Currency Converter/
│   ├── currency_converter.py
│   ├── README.md
│   └── Screenshot 2026-08-08 223002.png
└── Task 6 Word Count Tool/
    ├── word_count_app.py
    ├── requirements_streamlit.txt
    └── Screenshot 2026-08-08 223202.png
```

## Prerequisites

- Python 3.8 or newer
- `pip`
- An internet connection for Tasks 4 and 5 (they fetch data from external sites and APIs)

It's a good idea to use a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

## Quick Start

Every project is a standalone Streamlit app. Install its dependencies, then run it from inside its folder:

```bash
cd "Task 1 To-Do List Application"
pip install streamlit
streamlit run todo_list.py
```

The app opens in your browser at `http://localhost:8501`. To install everything for all six tasks at once:

```bash
pip install streamlit requests beautifulsoup4 pandas
```

---

## Task 1 – To-Do List Application

![To-Do List screenshot](Task%201%20To-Do%20List%20Application/Screenshot%202026-08-08%20222207.png)

A task manager where each task is a `Task` dataclass (description, completion status, creation timestamp, and a unique ID).

**Features**
- Add tasks (empty input and duplicate active tasks are rejected)
- Mark tasks complete or incomplete with a checkbox
- Delete individual tasks
- Filter by All / Active / Completed
- Bulk actions: clear completed tasks, delete all tasks
- Live counters for total, active, and completed tasks

**Run**
```bash
cd "Task 1 To-Do List Application"
pip install streamlit
streamlit run todo_list.py
```

**Limitations:** Tasks are held in `st.session_state`, so they are lost when the app restarts or the tab is closed. Existing tasks cannot be edited.

More details: [`README_todo_list.md`](Task%201%20To-Do%20List%20Application/README_todo_list.md)

---

## Task 2 – Guess the Number Game

![Guess the Number screenshot](Task%202%20Guess%20The%20Number%20Game/Screenshot%202026-08-08%20222301.png)

The app picks a random number and gives higher/lower hints until you find it.

**Features**
- Three difficulty levels: Easy (1–50), Medium (1–100), Hard (1–500)
- Higher/lower hints and an attempt counter
- Full guess history shown on screen
- Input validation for non-numbers and out-of-range guesses
- Play again with the same range, or change difficulty without restarting

**Run**
```bash
cd "Task 2 Guess The Number Game"
pip install streamlit
streamlit run guess_number.py
```

**Implementation note:** Streamlit reruns the whole script on every interaction, so the target number, attempts, and history are kept in `st.session_state`.

**Limitations:** No leaderboard or best-score tracking across sessions.

More details: [`README_guess_number.md`](Task%202%20Guess%20The%20Number%20Game/README_guess_number.md)

---

## Task 3 – Basic File Handling

![File Handler screenshot](Task%203%20Basic%20File%20Handling/Screenshot%202026-08-08%20222400.png)

Reads a text file, lets you find and replace text, previews the result, and saves it.

**Features**
- Two load modes: **upload a file** (works anywhere) or **read from a local file path** (works when running locally)
- Find and replace with case-sensitive and whole-word options
- Preview of the modified text before anything is saved
- Save by downloading a new file, or overwrite the original (local path mode only)
- Handles missing files, permission errors, directories, non-UTF-8 encodings, empty files, and invalid patterns

**Run**
```bash
cd "Task 3 Basic File Handling"
pip install streamlit
streamlit run file_handler.py
```

**Limitations:** Text files only (`.txt`, `.csv`, `.log`, `.md`). There is no undo after overwriting a file on disk, so check the preview first.

More details: [`README_file_handler.md`](Task%203%20Basic%20File%20Handling/README_file_handler.md)

---

## Task 4 – Basic Web Scraper

![Web Scraper screenshot](Task%204%20Basic%20Web%20Scraper/Screenshot%202026-08-08%20222843.png)

Extracts headlines or other text from a public webpage using Requests and BeautifulSoup.

**Features**
- Choose a common tag (`h1`, `h2`, `h3`, `h2 a`, `h3 a`, `a`) or write a custom CSS selector
- Removes duplicate results and resolves relative links to full URLs
- Adjustable maximum number of results
- Download results as CSV
- Handles invalid URLs, timeouts, connection failures, HTTP errors, and bad selectors
- Results are cached for 10 minutes to avoid repeated requests

**Run**
```bash
cd "Task 4 Basic Web Scraper"
pip install streamlit requests beautifulsoup4 pandas
streamlit run web_scraper.py
```

**Limitations:** Only scrapes static HTML (no JavaScript rendering) and a single page at a time. Always check a site's `robots.txt` and terms of service before scraping. This tool is for educational use.

More details: [`README_web_scraper.md`](Task%204%20Basic%20Web%20Scraper/README_web_scraper.md)

---

## Task 5 – Currency Converter

![Currency Converter screenshot](Task%205%20Currency%20Converter/Screenshot%202026-08-08%20223002.png)

Converts between currencies using live exchange rates.

**Features**
- Convert between any two supported currencies
- Uses the free, no-key [open.er-api.com](https://open.er-api.com) by default
- Optional [Open Exchange Rates](https://openexchangerates.org) support: paste an App ID into the sidebar
- Swap button to flip the From and To currencies
- Rejects non-numeric, negative, and zero amounts
- Handles network failures and bad API responses
- Rates are cached for 1 hour

**Run**
```bash
cd "Task 5 Currency Converter"
pip install streamlit requests
streamlit run currency_converter.py
```

**Limitations:** No automatic retry if the API is down. Restricted networks (school, office) may block the API calls.

More details: [`README.md`](Task%205%20Currency%20Converter/README.md)

---

## Task 6 – Word Count Tool

![Word Count Tool screenshot](Task%206%20Word%20Count%20Tool/Screenshot%202026-08-08%20223202.png)

Paste text or upload a `.txt` file to get instant text statistics and a word-frequency chart.

**Features**
- Paste text or upload a `.txt` file
- Counts for words, lines, characters (with and without spaces), and unique words
- Average word length and longest word
- Top-N most frequent words (5–25) as a table and bar chart
- Optional exclusion of common stop words (the, and, of, …)

**Run**
```bash
cd "Task 6 Word Count Tool"
pip install -r requirements_streamlit.txt
streamlit run word_count_app.py
```

Pinned dependencies: `streamlit==1.38.0`, `pandas==2.2.2`.

---

## Troubleshooting

- **`streamlit: command not found`** – Make sure your virtual environment is active and Streamlit is installed, or run `python -m streamlit run <file>.py`.
- **Port already in use** – Run on another port: `streamlit run <file>.py --server.port 8502`.
- **Tasks 4 or 5 show a connection error** – Check your internet connection. Some school and corporate networks block outbound requests.
- **Task 3 "file not found" in local path mode** – Use the full absolute path. Relative paths resolve from the folder where you ran `streamlit run`, not from the script's location.

## Author

_Add your name, links, and contact details here._

## License

_Add a license here (for example, MIT) or remove this section._
- Changing the feature set or the train/test split resets any model you've already trained — you'll need to retrain after either change.
- Random Forest with all features typically lands around 80% accuracy and 0.83–0.84 ROC-AUC on this dataset, with no hyperparameter tuning. Recall on the churn class is the weaker metric — worth keeping in mind if the business priority is catching as many at-risk customers as possible rather than overall accuracy.
