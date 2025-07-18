# Women in Hadith: A Data-Driven Analysis of Female Narrators

This project provides a complete data pipeline to analyze the contributions and network of female narrators of hadith (muhaddithat). It automates the process of data collection, cleaning, analysis, and visualization to uncover insights into the roles these women played in the Islamic tradition.

The pipeline processes data from multiple sources, including biographical information and hadith chains (isnads), to build a network graph and perform topic modeling on the texts of hadiths narrated by women.

## Key Findings

### 1. Network Centrality: The Mothers of the Believers

The network analysis identifies the most influential female narrators by calculating their PageRank centrality. A higher PageRank score indicates a more central role in the network of hadith transmission. Our analysis reveals that the most central figures are overwhelmingly the wives of the Prophet Muhammad (ﷺ), known as the *Ummāhat al-Mu'minīn* (Mothers of the Believers).

The top 5 most influential narrators are:

| Name                      | PageRank Score |
| ------------------------- | :------------: |
| **ʿAʾishah bint Abi Bakr**    |    ~0.121      |
| **Umm Salamah**           |    ~0.112      |
| **Zaynab bint Jaḥsh**     |    ~0.092      |
| **Ramlah bint Abi Sufyān**|    ~0.083      |
| **Asmāʾ bint ʿUmays**     |    ~0.057      |

This finding quantitatively confirms the historical understanding that the wives of the Prophet were primary sources of knowledge about his life and teachings, with **ʿAʾishah bint Abi Bakr** being the most central figure in the network of female narrators.

You can explore these connections in detail using the interactive visualization file: `docs/muhaddithat_network.html`.

### 2. Thematic Analysis of Narrated Hadiths

Topic modeling was performed on the collected hadith texts to identify underlying themes. The analysis produced six distinct topics. Due to the formulaic nature of hadith narration, the topics primarily reflect common linguistic patterns and chains of transmission rather than distinct theological subjects. 

**Summary of Identified Topics:**

-   **Topic 1 & 5:** Focus heavily on pronouns (`he`, `she`, `it`, `him`) and common verbs (`said`, `is`, `was`), representing the core structure of narrative transmission.
-   **Topic 2 & 6:** Include conditional (`if`, `then`) and instructional (`should`) language, suggesting they may capture hadiths related to rulings, guidance, and obligations.
-   **Topic 3 & 4:** Contain words like `prophet`, `allah's`, and `ibn` (son of), indicating a focus on narrations that explicitly mention the Prophet or trace a lineage.

**Limitations and Future Work:**
This initial topic model provides a high-level view. A more granular analysis could be achieved by applying advanced NLP techniques such as:
-   **Lemmatization and Stemming:** Reducing words to their root forms.
-   **Stop-Word Removal:** Filtering out common words (e.g., "the", "a", "is") to focus on meaningful keywords.
-   **N-grams:** Analyzing word pairs (bigrams) or triplets (trigrams) to capture more complex concepts.

These steps would help move beyond structural patterns to uncover deeper theological, legal, and social themes within the hadiths narrated by women.

## Project Pipeline

This project is structured as a series of Python scripts that should be run sequentially:

1.  `D01_download.py`: Downloads all necessary raw data.
2.  `03_metadata.py`: Creates a clean metadata file of all female narrators.
3.  `04_network.py`: Builds the network graph, calculates PageRank, and generates the interactive visualization.
4.  `05_text_analysis.py`: Performs topic modeling on the hadith texts.

## How to Use This Project

### 1. Prerequisites

-   Python 3.9+
-   Git

### 2. Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shamsikhani/women-in-hadith.git
    cd women-in-hadith
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows: .venv\Scripts\activate
    # On macOS/Linux: source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Running the Pipeline

If you wish to regenerate the results, execute the scripts in order:

```bash
python scripts/D01_download.py
python scripts/03_metadata.py
python scripts/04_network.py
python scripts/05_text_analysis.py
```

All data and results are already included in the repository, so you can also explore the files in the `data/` and `docs/` directories directly.

## Project Structure

```
. 
├── scripts/      # All Python scripts for the pipeline 
├── data/         # Raw and processed data 
│   ├── raw/ 
│   └── processed/ 
├── docs/         # Output documentation and visualizations 
├── .gitignore    # Files to be ignored by Git 
├── requirements.txt # Python package dependencies 
└── README.md     # This file
