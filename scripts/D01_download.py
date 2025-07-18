import os
import subprocess
import requests
import json
import time
import pathlib
from tqdm import tqdm

# --- Configuration ---
DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'raw'


# --- Helper Functions ---
def download_file(url, dest_path):
    """Downloads a file from a URL to a destination path."""
    print(f"Downloading {url} to {dest_path}...")
    response = requests.get(url, stream=True)
    if response.ok:
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    else:
        print(f"Error downloading {url}: {response.status_code}")

# --- Main Download Functions ---
def download_isnad_datasets():
    """Clones the isnad-datasets repository."""
    dest = DATA_DIR / 'isnad-datasets'
    if dest.exists():
        print("isnad-datasets already cloned.")
        return
    print("Cloning isnad-datasets repository...")
    subprocess.run(['git', 'clone', 'https://github.com/muhaddithat/isnad-datasets.git', str(dest)], check=True)

def download_kaggle_dataset():
    """Downloads the hadith-narrators dataset from Kaggle."""
    dest = DATA_DIR / 'hadith-narrators.zip'
    if dest.exists():
        print("Kaggle dataset already downloaded.")
        return
    print("Downloading Kaggle dataset...")
    print("Please ensure your Kaggle API token is configured.")

    # Construct the absolute path to the kaggle executable within the venv
    project_root = pathlib.Path(__file__).resolve().parent.parent
    kaggle_exe = project_root / '.venv' / 'Scripts' / 'kaggle.exe'

    if not kaggle_exe.exists():
        print(f"Error: kaggle.exe not found at {kaggle_exe}")
        print("Please ensure the virtual environment is set up correctly.")
        return

    subprocess.run([str(kaggle_exe), 'datasets', 'download', 'fahd09/hadith-narrators', '-p', str(DATA_DIR)], check=True)

from bs4 import BeautifulSoup

def fetch_hadith_texts_by_scraping(narrators):
    """Fetches hadith texts for a list of narrators by scraping Sunnah.com."""
    search_url = "https://sunnah.com/search"
    dest_dir = DATA_DIR / 'hadith_api'
    dest_dir.mkdir(exist_ok=True)

    print(f"Scraping Hadith texts for {len(narrators)} narrators...")
    for name in tqdm(narrators):
        dest_file = dest_dir / f"{name.replace(' ', '_')}.json"
        if dest_file.exists():
            continue

        try:
            response = requests.get(search_url, params={'q': name})
            if not response.ok:
                print(f"Failed to fetch search results for {name}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'lxml')
            results = soup.find_all('div', {'class': 'english_hadith_full'})
            
            hadiths = []
            for result in results:
                hadith_text = result.get_text(strip=True)
                # Structure mimics the original API to minimize downstream changes
                hadiths.append({'body': hadith_text})

            # The data is wrapped in a list of one element to match the structure
            # that the text analysis script expects: data -> list -> hadith -> list -> body
            output_data = {'data': [{'hadith': hadiths}]}
            dest_file.write_text(
            json.dumps(output_data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

            time.sleep(1)  # Be a responsible scraper

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while scraping data for {name}: {e}")

def download_reference_pdf():
    """Downloads the Al-Muhaddithat PDF from the Internet Archive."""
    url = "https://archive.org/download/131990735AlMuhaddithatTheWomenScholarsInIslam/131990735-Al-Muhaddithat-the-Women-Scholars-in-Islam.pdf"
    dest = DATA_DIR / 'Al-Muhaddithat.pdf'
    if dest.exists():
        print("Reference PDF already downloaded.")
        return
    download_file(url, dest)

if __name__ == '__main__':
    DATA_DIR.mkdir(exist_ok=True)
    download_isnad_datasets()
    download_kaggle_dataset()
    download_reference_pdf()

    # Example of how to run the hadith text fetching part
    # You would typically load the narrator names from the metadata file
    # For now, this is just a placeholder.
    # female_narrators = ['Aisha bint Abi Bakr', 'Umm Salamah'] 
    # fetch_hadith_texts(female_narrators)

    print("\nAll downloads complete.")
