import json
import glob
import pathlib
from gensim import corpora, models
import pandas as pd

# Import the function from the download script to fetch hadiths if needed
from D01_download import fetch_hadith_texts_by_scraping

def run_topic_modeling(num_topics=6, passes=10):
    """Performs topic modeling on the women-narrated hadith texts."""
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    raw_data_dir = base_dir / 'data' / 'raw'
    processed_data_dir = base_dir / 'data' / 'processed'
    processed_data_dir.mkdir(exist_ok=True)

    # Define paths
    hadith_api_dir = raw_data_dir / 'hadith_api'
    metadata_file = processed_data_dir / 'muhaddithat_metadata.csv'
    model_file = processed_data_dir / f'lda_women_hadith_{num_topics}topics.model'

    # --- Step 1: Ensure Hadith texts are downloaded ---
    # This part makes the script runnable by first fetching the required data.
        # --- Step 1: Ensure Hadith texts are available ---
    # This part makes the script runnable by first fetching the required data via scraping.
    if not hadith_api_dir.exists() or not any(hadith_api_dir.iterdir()):
        print("Hadith text files not found.")
        if not metadata_file.exists():
            print("Metadata file not found. Please run script 03 first. Exiting.")
            return
        
        print("Scraping hadith texts now...")
        meta = pd.read_csv(metadata_file)
        # Use unique names to avoid redundant scraping
        female_narrators = meta['name'].unique().tolist()
        fetch_hadith_texts_by_scraping(female_narrators)

    # --- Step 2: Load and process texts ---
    print("Loading hadith texts for topic modeling...")
    texts = []
    json_files = glob.glob(str(hadith_api_dir / '*.json'))
    
    if not json_files:
        print("No JSON files found in the hadith_api directory. Nothing to process.")
        return

    for f in json_files:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'data' in data:
                for hadith_entry in data['data']:
                    # Assuming the structure is a list of hadiths
                    for hadith_text_info in hadith_entry.get('hadith', []):
                        if 'body' in hadith_text_info:
                            # Basic preprocessing: lowercase and split
                            texts.append(hadith_text_info['body'].lower().split())

    if not texts:
        print("No hadith texts could be extracted. Cannot perform topic modeling.")
        return

    # --- Step 3: Create dictionary and corpus ---
    print("Building dictionary and corpus...")
    dictionary = corpora.Dictionary(texts)
    # Filter out very rare and very common words
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # --- Step 4: Train LDA model ---
    print(f"Training LDA model with {num_topics} topics...")
    lda = models.LdaModel(
        corpus,
        num_topics=num_topics,
        id2word=dictionary,
        passes=passes,
        random_state=42
    )

    # --- Step 5: Print and save results ---
    print("\n--- Identified Topics ---")
    lda.print_topics()

    lda.save(str(model_file))
    print(f"\nLDA model saved to {model_file}")

if __name__ == '__main__':
    run_topic_modeling()
