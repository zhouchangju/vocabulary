#!/usr/bin/env python3
"""
Automatically download all required linguistic databases.
Run: python toefl_classifier/download_data.py
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def download_file(url, dest, description):
    """Download file with progress bar."""
    print(f"Downloading {description}...")
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    downloaded = 0

    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                print(f"\rProgress: {percent:.1f}%", end='', flush=True)

    print(f"\r✓ Downloaded {description}")
    return dest


def download_nrc_emotion_lexicon():
    """
    Download NRC Emotion Lexicon.
    Source: https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm
    """
    url = "https://saifmohammad.com/WebPages/Downloadlexicon.zip"
    zip_path = DATA_DIR / "NRC-Emotion-Lexicon.zip"
    extract_dir = DATA_DIR / "temp_nrc"

    try:
        download_file(url, zip_path, "NRC Emotion Lexicon")

        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Find and rename the text file
        for file in extract_dir.rglob("*Wordlevel*"):
            file.rename(DATA_DIR / "nrc_emotion_lexicon.txt")
            break

        # Cleanup
        shutil.rmtree(extract_dir)
        zip_path.unlink()

        print("✓ NRC Emotion Lexicon ready")

    except Exception as e:
        print(f"⚠ Manual download required for NRC lexicon: {e}")
        print("  Visit: https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm")
        print(f"  Save to: {DATA_DIR}/nrc_emotion_lexicon.txt")


def download_academic_word_list():
    """
    Download Academic Word List.
    Uses publicly available source.
    """
    # Public AWL source
    url = "https://www.wordfrequency.info/files/academic_word_list.xls"

    try:
        dest = DATA_DIR / "academic_word_list.xls"
        download_file(url, dest, "Academic Word List")
        print("✓ Academic Word List downloaded (needs conversion to .txt)")

    except Exception as e:
        print(f"⚠ Manual download required for AWL: {e}")
        print("  Visit: https://www.wordfrequency.info/free.asp?s=y")
        print(f"  Save to: {DATA_DIR}/academic_word_list.txt")


def create_placeholder_coca_data():
    """
    COCA data requires manual signup.
    Create placeholder with instructions.
    """
    readme_path = DATA_DIR / "coca_frequency.txt"

    if not readme_path.exists():
        with open(readme_path, 'w') as f:
            f.write("""# COCA Frequency Data

# INSTRUCTIONS:
# 1. Visit: https://www.wordfrequency.info/free.asp?s=y
# 2. Complete free signup
# 3. Download "COCA 20000 word frequency list" (text format)
# 4. Replace this file with the downloaded content

# Expected format (tab-separated):
# the	1
# be	2
# of	3
# and	4
# a	5
...
""")
        print("✓ Created COCA data placeholder with instructions")


def create_sample_toefl_corpus():
    """
    Create sample TOEFL frequency data.
    In production, this would be extracted from TPO/Official tests.
    """
    corpus_path = DATA_DIR / "toefl_corpus.txt"

    if not corpus_path.exists():
        with open(corpus_path, 'w') as f:
            f.write("""# TOEFL Word Frequency Corpus
# Format: word\tfrequency_in_exams
# This is sample data - expand with real TOEFL test corpus

analyze	127
hypothesis	98
theory	85
interpret	72
establish	69
...
""")
        print("✓ Created sample TOEFL corpus (expand with real test data)")


def main():
    """Download all databases."""
    print("=" * 60)
    print("TOEFL Classifier - Database Download")
    print("=" * 60)
    print(f"Target directory: {DATA_DIR.absolute()}")
    print()

    download_nrc_emotion_lexicon()
    print()
    download_academic_word_list()
    print()
    create_placeholder_coca_data()
    print()
    create_sample_toefl_corpus()
    print()

    print("=" * 60)
    print("Download complete!")
    print()
    print("Next steps:")
    print("1. Follow manual instructions for COCA data (if needed)")
    print("2. Convert academic_word_list.xls to academic_word_list.txt")
    print("3. Run: python toefl_classifier/classify.py")
    print("=" * 60)


if __name__ == '__main__':
    main()
