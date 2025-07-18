# Women in Hadith: A Data-Driven Analysis of Female Narrators

This project provides a complete data pipeline to analyze the contributions and network of female narrators of hadith (muhaddithat). It automates the process of data collection, cleaning, analysis, and visualization to uncover insights into the roles these women played in the Islamic tradition.

The pipeline processes data from multiple sources, including biographical information and hadith chains (isnads), to build a network graph and perform topic modeling on the texts of hadiths narrated by women.

## Key Findings

1.  **Network Structure:** The generated network reveals a densely interconnected community of female scholars. The interactive visualization (`docs/muhaddithat_network.html`) allows for exploration of these connections, highlighting central figures and their relationships.
2.  **Influence Analysis:** By calculating the PageRank centrality for each narrator, we can identify the most influential women in the network. These are individuals who were highly connected and central to the transmission of knowledge.
3.  **Thematic Analysis:** Topic modeling on the hadith texts narrated by women reveals key themes and areas of focus in their teachings. The trained LDA model (`data/processed/lda_women_hadith_6topics.model`) can be used for further textual analysis.
- `scripts/`: Python scripts for each step of the analysis.
- `docs/`: Generated documentation and visualizations.
- `env.yml`: Conda environment specification.

## Reproducibility

To reproduce the analysis, install the environment and run the scripts in order:

```bash
conda env create -f env.yml
conda activate muhaddithat
python scripts/01_download.py
python scripts/02_ocr_clean.py
# ... and so on
```
