#!/usr/bin/env python3
"""
Automatically download all required linguistic databases.
Run: python toefl_classifier/download_data.py
"""

import os
import tempfile
import requests
import zipfile
import shutil
from pathlib import Path


def get_data_dir():
    """Get and ensure data directory exists."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def download_file(url, dest, description):
    """Download file with progress bar."""
    print(f"Downloading {description}...")
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    downloaded = 0

    # Download to temporary file first
    temp_dest = dest.with_suffix(dest.suffix + '.tmp')
    try:
        with open(temp_dest, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)

        # Atomic rename to final destination
        temp_dest.rename(dest)
        print(f"\r✓ Downloaded {description}")
        return dest
    except Exception:
        # Clean up temporary file on error
        if temp_dest.exists():
            temp_dest.unlink()
        raise


def safe_extract_zip(zip_path, extract_dir):
    """
    Safely extract zip file with path sanitization to prevent zip slip attacks.

    Args:
        zip_path: Path to zip file
        extract_dir: Directory to extract to

    Raises:
        ValueError: If a file attempts path traversal outside extract_dir
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            # Resolve the full path of the extracted file
            member_path = (extract_dir / member.filename).resolve()

            # Ensure the resolved path is within the extract directory
            if not str(member_path).startswith(str(extract_dir.resolve())):
                raise ValueError(
                    f"Zip slip vulnerability detected: {member.filename} "
                    f"attempts to escape extraction directory"
                )

            # Extract the file safely
            zip_ref.extract(member, extract_dir)


def download_nrc_emotion_lexicon():
    """
    Download NRC Emotion Lexicon.
    Source: https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm
    """
    data_dir = get_data_dir()
    url = "https://saifmohammad.com/WebPages/Downloadlexicon.zip"
    zip_path = data_dir / "NRC-Emotion-Lexicon.zip"
    extract_dir = None

    try:
        download_file(url, zip_path, "NRC Emotion Lexicon")

        print("Extracting...")
        # Use temporary directory for extraction
        extract_dir = tempfile.mkdtemp(prefix="nrc_extract_")
        safe_extract_zip(zip_path, Path(extract_dir))

        # Find and rename the text file
        found = False
        for file in Path(extract_dir).rglob("*Wordlevel*"):
            file.rename(data_dir / "nrc_emotion_lexicon.txt")
            found = True
            break

        if not found:
            raise FileNotFoundError("Could not find Wordlevel lexicon file in downloaded archive")

        print("✓ NRC Emotion Lexicon ready")

    except Exception as e:
        print(f"⚠ Manual download required for NRC lexicon: {e}")
        print("  Visit: https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm")
        print(f"  Save to: {data_dir}/nrc_emotion_lexicon.txt")

    finally:
        # Always cleanup temporary files and directories
        if extract_dir and os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        if zip_path.exists():
            zip_path.unlink()


def download_academic_word_list():
    """
    Download Academic Word List.
    Uses publicly available source.
    """
    data_dir = get_data_dir()
    # Public AWL source
    url = "https://www.wordfrequency.info/files/academic_word_list.xls"

    try:
        dest = data_dir / "academic_word_list.xls"
        download_file(url, dest, "Academic Word List")
        print("✓ Academic Word List downloaded (needs conversion to .txt)")

    except Exception as e:
        print(f"⚠ Manual download required for AWL: {e}")
        print("  Visit: https://www.wordfrequency.info/free.asp?s=y")
        print(f"  Save to: {data_dir}/academic_word_list.txt")


def create_placeholder_coca_data():
    """
    COCA data requires manual signup.
    Create placeholder with instructions.
    """
    data_dir = get_data_dir()
    readme_path = data_dir / "coca_frequency.txt"

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
    data_dir = get_data_dir()
    corpus_path = data_dir / "toefl_corpus.txt"

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
    data_dir = get_data_dir()
    print("=" * 60)
    print("TOEFL Classifier - Database Download")
    print("=" * 60)
    print(f"Target directory: {data_dir.absolute()}")
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
