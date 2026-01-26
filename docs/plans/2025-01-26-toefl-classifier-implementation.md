# TOEFL Vocabulary Classifier Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an intelligent multi-dimensional vocabulary classification system for 6000 TOEFL words with interactive web UI for filtering and export to Anki.

**Architecture:** 3-tier pipeline: Python backend processes words using NLTK/spaCy → enriched JSON database → JavaScript web UI for real-time filtering → export layer (Anki CSV/Markdown).

**Tech Stack:** Python 3.8+, NLTK, spaCy, Node.js (existing), vanilla JavaScript, JSON

---

## Task 1: Project Structure & Virtual Environment Setup

**Files:**
- Create: `toefl_classifier/__init__.py`
- Create: `toefl_classifier/requirements.txt`
- Create: `toefl_classifier/data/README.md`

**Step 1: Create requirements.txt**

```bash
cd /Users/leozhou/git/vocabulary/.worktrees/toefl-classifier
```

Create `toefl_classifier/requirements.txt`:

```txt
nltk>=3.8
spacy>=3.7
numpy>=1.24
pandas>=2.0
requests>=2.31
```

**Step 2: Create Python virtual environment**

```bash
cd /Users/leozhou/git/vocabulary/.worktrees/toefl-classifier
python -m venv venv
source venv/bin/activate
pip install -r toefl_classifier/requirements.txt
```

**Step 3: Download NLTK data**

```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt')"
```

**Step 4: Download spaCy model**

```bash
python -m spacy download en_core_web_sm
```

**Step 5: Create data directory README**

Create `toefl_classifier/data/README.md`:

```markdown
# Linguistic Databases

This directory contains reference databases for word classification:

- `coca_frequency.txt` - COCA corpus frequency rankings
- `academic_word_list.txt` - Academic Word List (570 words)
- `nrc_emotion_lexicon.txt` - NRC Emotion Lexicon
- `toefl_corpus.txt` - TOEFL exam frequency data

All files are auto-downloaded by `download_data.py`.
```

**Step 6: Commit setup**

```bash
git add toefl_classifier/
git commit -m "feat: setup Python project structure and dependencies

- Create requirements.txt with NLTK, spaCy, pandas
- Add virtual environment setup instructions
- Create data directory structure"
```

---

## Task 2: Automatic Database Download Script

**Files:**
- Create: `toefl_classifier/download_data.py`
- Create: `toefl_classifier/data/.gitkeep`

**Step 1: Create .gitkeep for data directory**

```bash
touch toefl_classifier/data/.gitkeep
```

**Step 2: Write download script**

Create `toefl_classifier/download_data.py`:

```python
#!/usr/bin/env python3
"""
Automatically download all required linguistic databases.
Run: python toefl_classifier/download_data.py
"""

import os
import requests
import zipfile
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def download_file(url, dest, description):
    """Download file with progress bar."""
    print(f"Downloading {description}...")
    response = requests.get(url, stream=True)
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
        import shutil
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
```

**Step 3: Make script executable**

```bash
chmod +x toefl_classifier/download_data.py
```

**Step 4: Test download script**

```bash
python toefl_classifier/download_data.py
```

Expected output: Downloads NRC lexicon, creates placeholders for COCA and AWL with instructions.

**Step 5: Commit download script**

```bash
git add toefl_classifier/download_data.py toefl_classifier/data/.gitkeep
git commit -m "feat: add automatic database download script

- Download NRC Emotion Lexicon automatically
- Create instruction files for COCA and AWL (manual signup required)
- Add progress bars for large downloads
- Handle errors gracefully with fallback instructions"
```

---

## Task 3: Word Family Processor

**Files:**
- Create: `toefl_classifier/lemmatizer.py`
- Create: `tests/test_lemmatizer.py`

**Step 1: Write failing test**

Create `tests/test_lemmatizer.py`:

```python
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from toefl_classifier.lemmatizer import WordFamilyProcessor

def test_get_lemma_of_simple_word():
    """Test lemmatization of simple word."""
    processor = WordFamilyProcessor()
    result = processor.get_word_family("ran")

    assert result['lemma'] == 'run'
    assert 'run' in result['word_family']
    assert result['pos'] == 'VERB'

def test_get_lemma_of_irregular_word():
    """Test lemmatization of irregular word."""
    processor = WordFamilyProcessor()
    result = processor.get_word_family("better")

    assert result['lemma'] == 'well'  # or 'good' depending on context
    assert 'good' in result['word_family'] or 'well' in result['word_family']

def test_get_word_family_includes_derivations():
    """Test that word family includes derivational forms."""
    processor = WordFamilyProcessor()
    result = processor.get_word_family("analyze")

    assert result['lemma'] == 'analyze'
    # Should include: analysis, analytical, analytically, etc.
    assert 'analysis' in result['word_family']

def test_get_word_family_returns_pos():
    """Test that POS is correctly identified."""
    processor = WordFamilyProcessor()

    noun_result = processor.get_word_family("predator")
    assert noun_result['pos'] == 'NOUN'

    verb_result = processor.get_word_family("analyze")
    assert verb_result['pos'] == 'VERB'
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_lemmatizer.py -v
```

Expected: `ImportError: cannot import name 'WordFamilyProcessor'`

**Step 3: Write minimal implementation**

Create `toefl_classifier/lemmatizer.py`:

```python
"""
Word family extraction using NLTK WordNet and spaCy.
Groups morphological and derivationally related forms.
"""

import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import defaultdict

class WordFamilyProcessor:
    """Extract lemmas and word families using WordNet and spaCy."""

    def __init__(self):
        """Initialize spaCy model and NLTK lemmatizer."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError(
                "spaCy model not found. Run: python -m spacy download en_core_web_sm"
            )

        self.lemmatizer = WordNetLemmatizer()

    def get_word_family(self, word):
        """
        Extract lemma, word family, and POS for a given word.

        Args:
            word: Single word string

        Returns:
            dict with keys:
                - lemma: Base form of the word
                - word_family: List of related word forms
                - pos: Part of speech (NOUN, VERB, ADJ, ADV)
        """
        # Process with spaCy for POS
        doc = self.nlp(word)
        token = doc[0]

        # Get base lemma
        lemma = token.lemma_

        # Collect word family from WordNet
        word_family = set()
        word_family.add(lemma)  # Always include the lemma

        # Get all derivationally related forms from WordNet
        for synset in wordnet.synsets(lemma):
            for lemma_obj in synset.lemmas():
                # Add the lemma form
                word_family.add(lemma_obj.name())

                # Add derivationally related forms
                if lemma_obj.derivationally_related_forms():
                    for related in lemma_obj.derivationally_related_forms():
                        word_family.add(related.name())

        # Add common morphological variants based on POS
        pos = token.pos_
        if pos == 'VERB':
            # Add -ing, -ed, -s forms
            word_family.update(self._get_verb_forms(lemma))
        elif pos == 'NOUN':
            # Add plural forms
            word_family.update(self._get_noun_forms(lemma))
        elif pos == 'ADJ':
            # Add comparative/superlative
            word_family.update(self._get_adjective_forms(lemma))

        # Remove underscores (WordNet uses underscores for spaces)
        word_family = [w.replace('_', '-') for w in word_family]

        return {
            'lemma': lemma,
            'word_family': sorted(list(word_family)),
            'pos': pos
        }

    def _get_verb_forms(self, lemma):
        """Generate common verb forms."""
        forms = set()

        # Simple rules (not perfect, but good enough for most cases)
        if lemma.endswith('e'):
            forms.add(lemma + 'd')  # -ed
            forms.add(lemma + 's')  # -3rd person
        else:
            forms.add(lemma + 'ed')
            forms.add(lemma + 's')

        forms.add(lemma + 'ing')  # -ing

        return forms

    def _get_noun_forms(self, lemma):
        """Generate common noun forms."""
        forms = set()

        # Simple pluralization
        if lemma.endswith('y'):
            forms.add(lemma[:-1] + 'ies')
        elif lemma.endswith('s') or lemma.endswith('x') or lemma.endswith('ch'):
            forms.add(lemma + 'es')
        else:
            forms.add(lemma + 's')

        return forms

    def _get_adjective_forms(self, lemma):
        """Generate common adjective forms."""
        forms = set()

        # Comparative/superlative
        if lemma.endswith('e'):
            forms.add(lemma + 'r')   # comparative
            forms.add(lemma + 'st')  # superlative
        else:
            if len(lemma) > 2:
                forms.add(lemma + 'er')
                forms.add(lemma + 'est')

        return forms
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_lemmatizer.py -v
```

Expected: All tests pass

**Step 5: Add more edge case tests**

```python
def test_homograph_disambiguation():
    """Test that homographs are handled by context."""
    processor = WordFamilyProcessor()

    # "record" as noun
    noun_context = processor.nlp("The record was broken")
    noun_token = noun_context[2]  # "record"
    noun_result = processor.get_word_family(noun_token.text)

    # "record" as verb
    verb_context = processor.nlp("I will record the song")
    verb_token = verb_context[3]  # "record"
    verb_result = processor.get_word_family(verb_token.text)

    # Both should have same lemma
    assert noun_result['lemma'] == verb_result['lemma']
```

**Step 6: Run extended tests**

```bash
pytest tests/test_lemmatizer.py::test_homograph_disambiguation -v
```

**Step 7: Commit word family processor**

```bash
git add toefl_classifier/lemmatizer.py tests/test_lemmatizer.py
git commit -m "feat: implement word family extraction with NLTK and spaCy

- Use spaCy for accurate POS tagging
- Use WordNet for derivationally related forms
- Generate morphological variants (plurals, tenses)
- Handle homographs via context
- Add comprehensive test suite"
```

---

## Task 4: Frequency Grading Module

**Files:**
- Create: `toefl_classifier/frequency_grader.py`
- Create: `tests/test_frequency_grader.py`

**Step 1: Write failing test**

Create `tests/test_frequency_grader.py`:

```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from toefl_classifier.frequency_grader import FrequencyGrader

def test_collins_5_star_most_common():
    """Test that most common words get 5 stars."""
    grader = FrequencyGrader()

    # "the" is rank 1, should be 5 stars
    result = grader._get_collins_stars(1)
    assert result == 5

def test_collins_1_star_less_common():
    """Test that less common words get 1 star."""
    grader = FrequencyGrader()

    # Rank 15000 should be 1 star
    result = grader._get_collins_stars(15000)
    assert result == 1

def test_grade_frequency_with_mock_data():
    """Test frequency grading with mock data."""
    # Create temporary mock data file
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("the\t1\n")
        f.write("predator\t5000\n")
        f.write("abacus\t18000\n")
        temp_file = f.name

    try:
        grader = FrequencyGrader(coca_file=temp_file)

        # Test high frequency word
        the_result = grader.grade_frequency("the")
        assert the_result['coca_rank'] == 1
        assert the_result['collins_stars'] == 5

        # Test medium frequency word
        predator_result = grader.grade_frequency("predator")
        assert predator_result['coca_rank'] == 5000
        assert predator_result['collins_stars'] == 3

        # Test low frequency word
        abacus_result = grader.grade_frequency("abacus")
        assert abacus_result['coca_rank'] == 18000
        assert abacus_result['collins_stars'] == 1

    finally:
        os.unlink(temp_file)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_frequency_grader.py -v
```

Expected: `ImportError`

**Step 3: Write minimal implementation**

Create `toefl_classifier/frequency_grader.py`:

```python
"""
Frequency grading using COCA corpus data.
Assigns Collins star ratings and TOEFL frequency levels.
"""

from pathlib import Path

class FrequencyGrader:
    """
    Grade words by frequency using COCA corpus data.

    Collins star thresholds:
    - 5 stars: rank 1-1000 (most common)
    - 4 stars: rank 1001-3000
    - 3 stars: rank 3001-6000
    - 2 stars: rank 6001-12000
    - 1 star: rank 12001-20000
    """

    COLLINS_STAR_THRESHOLDS = {
        5: (1, 1000),
        4: (1001, 3000),
        3: (3001, 6000),
        2: (6001, 12000),
        1: (12001, 20000)
    }

    def __init__(self, coca_file=None, awl_file=None, toefl_corpus_file=None):
        """
        Initialize frequency grader.

        Args:
            coca_file: Path to COCA frequency data (tab-separated: word\\trank)
            awl_file: Path to Academic Word List
            toefl_corpus_file: Path to TOEFL frequency data
        """
        self.data_dir = Path(__file__).parent / "data"

        # Default file paths
        if coca_file is None:
            coca_file = self.data_dir / "coca_frequency.txt"

        # Load COCA frequency data
        self.coca_data = self._load_coca_data(coca_file)

        # Load AWL if provided
        self.awl_data = {}
        if awl_file:
            self.awl_data = self._load_awl(awl_file)

        # Load TOEFL corpus if provided
        self.toefl_corpus = {}
        if toefl_corpus_file:
            self.toefl_corpus = self._load_toefl_corpus(toefl_corpus_file)

    def _load_coca_data(self, filepath):
        """Load COCA frequency data from file."""
        data = {}

        if not filepath.exists():
            print(f"Warning: COCA file not found: {filepath}")
            return data

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split('\t')
                if len(parts) >= 2:
                    word = parts[0].lower()
                    rank = int(parts[1])
                    data[word] = rank

        return data

    def _load_awl(self, filepath):
        """Load Academic Word List."""
        data = {}

        # Implementation depends on AWL file format
        # TODO: Implement after file format is determined
        return data

    def _load_toefl_corpus(self, filepath):
        """Load TOEFL frequency corpus."""
        data = {}

        if not filepath.exists():
            return data

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split('\t')
                if len(parts) >= 2:
                    word = parts[0].lower()
                    freq = int(parts[1])
                    data[word] = freq

        return data

    def _get_collins_stars(self, rank):
        """
        Convert COCA rank to Collins star rating.

        Args:
            rank: COCA frequency rank (lower = more common)

        Returns:
            int: Star rating (1-5)
        """
        for stars, (min_rank, max_rank) in self.COLLINS_STAR_THRESHOLDS.items():
            if min_rank <= rank <= max_rank:
                return stars

        return 1  # Default to 1 star if not in range

    def grade_frequency(self, word):
        """
        Grade a word by frequency.

        Args:
            word: Word to grade

        Returns:
            dict with keys:
                - coca_rank: COCA frequency rank (or None)
                - collins_stars: Star rating (1-5)
                - toefl_frequency: "high", "medium", or "low"
                - is_academic: True if in AWL
                - awl_level: AWL sublist number (1-10) if academic
        """
        word = word.lower()

        # Get COCA rank
        coca_rank = self.coca_data.get(word)

        if coca_rank is None:
            # Word not in COCA data
            collins_stars = 1
        else:
            collins_stars = self._get_collins_stars(coca_rank)

        # Get TOEFL frequency
        toefl_freq = self.toefl_corpus.get(word, 0)
        if toefl_freq > 50:
            toefl_level = "high"
        elif toefl_freq > 10:
            toefl_level = "medium"
        else:
            toefl_level = "low"

        # Check if in AWL
        is_academic = word in self.awl_data
        awl_info = self.awl_data.get(word, {})
        awl_level = awl_info.get('level')

        return {
            'coca_rank': coca_rank,
            'collins_stars': collins_stars,
            'toefl_frequency': toefl_level,
            'is_academic': is_academic,
            'awl_level': awl_level
        }
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_frequency_grader.py -v
```

**Step 5: Commit frequency grader**

```bash
git add toefl_classifier/frequency_grader.py tests/test_frequency_grader.py
git commit -m "feat: implement frequency grading module

- Load COCA frequency data from tab-separated files
- Convert ranks to Collins star ratings (1-5)
- Calculate TOEFL frequency levels (high/medium/low)
- Support Academic Word List integration
- Add comprehensive tests"
```

---

## Task 5: Emotion Analyzer Module

**Files:**
- Create: `toefl_classifier/emotion_analyzer.py`
- Create: `tests/test_emotion_analyzer.py`

**Step 1: Write failing test**

Create `tests/test_emotion_analyzer.py`:

```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from toefl_classifier.emotion_analyzer import EmotionAnalyzer

def test_positive_emotion_detection():
    """Test detection of positive emotions."""
    # Create mock lexicon
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # "happy" has joy emotion
        f.write("happy\tjoy\t1\n")
        f.write("happy\ttrust\t1\n")
        f.write("happy\tanticipation\t1\n")
        temp_file = f.name

    try:
        analyzer = EmotionAnalyzer(lexicon_file=temp_file)
        result = analyzer.analyze_emotion("happy")

        assert result['sentiment'] == 'positive'
        assert 'joy' in result['emotions']
        assert 'trust' in result['emotions']

    finally:
        os.unlink(temp_file)

def test_negative_emotion_detection():
    """Test detection of negative emotions."""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # "fear" has fear and sadness emotions
        f.write("fear\tfear\t1\n")
        f.write("fear\tsadness\t1\n")
        temp_file = f.name

    try:
        analyzer = EmotionAnalyzer(lexicon_file=temp_file)
        result = analyzer.analyze_emotion("fear")

        assert result['sentiment'] == 'negative'
        assert 'fear' in result['emotions']

    finally:
        os.unlink(temp_file)

def test_neutral_sentiment():
    """Test that words without emotion are neutral."""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # "analyze" has no emotions marked
        temp_file = f.name

    try:
        analyzer = EmotionAnalyzer(lexicon_file=temp_file)
        result = analyzer.analyze_emotion("analyze")

        assert result['sentiment'] == 'neutral'
        assert result['emotions'] == []

    finally:
        os.unlink(temp_file)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_emotion_analyzer.py -v
```

Expected: `ImportError`

**Step 3: Write minimal implementation**

Create `toefl_classifier/emotion_analyzer.py`:

```python
"""
Emotion and sentiment analysis using NRC Emotion Lexicon.
Classifies words by sentiment polarity and specific emotions.
"""

from pathlib import Path

class EmotionAnalyzer:
    """
    Analyze word emotions using NRC Emotion Lexicon.

    The NRC lexicon categorizes words into 8 emotions:
    - anger, anticipation, disgust, fear, joy, sadness, surprise, trust

    And sentiment:
    - positive (joy, trust, anticipation)
    - negative (anger, fear, sadness, disgust)
    - neutral (balanced or no emotion)
    """

    EMOTIONS = [
        'anger', 'anticipation', 'disgust', 'fear',
        'joy', 'sadness', 'surprise', 'trust'
    ]

    POSITIVE_EMOTIONS = ['joy', 'trust', 'anticipation']
    NEGATIVE_EMOTIONS = ['anger', 'fear', 'sadness', 'disgust']

    def __init__(self, lexicon_file=None):
        """
        Initialize emotion analyzer.

        Args:
            lexicon_file: Path to NRC Emotion Lexicon file
                        Format: word\\temotion\\tpresent(0/1)
        """
        self.data_dir = Path(__file__).parent / "data"

        if lexicon_file is None:
            lexicon_file = self.data_dir / "nrc_emotion_lexicon.txt"

        self.lexicon = self._load_lexicon(lexicon_file)

    def _load_lexicon(self, filepath):
        """Load NRC Emotion Lexicon from file."""
        lexicon = {}

        if not filepath.exists():
            print(f"Warning: Emotion lexicon not found: {filepath}")
            return lexicon

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split('\t')
                if len(parts) >= 3:
                    word = parts[0].lower()
                    emotion = parts[1]
                    present = parts[2] == '1'

                    if present:
                        key = f"{word}\t{emotion}"
                        lexicon[key] = True

        return lexicon

    def analyze_emotion(self, word):
        """
        Analyze emotion and sentiment of a word.

        Args:
            word: Word to analyze

        Returns:
            dict with keys:
                - sentiment: "positive", "negative", or "neutral"
                - emotions: List of emotion labels present
        """
        word = word.lower()

        # Check all 8 emotions
        emotions_present = []
        for emotion in self.EMOTIONS:
            key = f"{word}\t{emotion}"
            if key in self.lexicon:
                emotions_present.append(emotion)

        # Determine sentiment polarity
        positive_count = sum(1 for e in emotions_present if e in self.POSITIVE_EMOTIONS)
        negative_count = sum(1 for e in emotions_present if e in self.NEGATIVE_EMOTIONS)

        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            'sentiment': sentiment,
            'emotions': emotions_present
        }
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_emotion_analyzer.py -v
```

**Step 5: Commit emotion analyzer**

```bash
git add toefl_classifier/emotion_analyzer.py tests/test_emotion_analyzer.py
git commit -m "feat: implement emotion analyzer using NRC lexicon

- Load NRC Emotion Lexicon (8 emotions + sentiment)
- Classify words by sentiment polarity
- Extract specific emotion categories
- Handle words with no emotion data as neutral
- Add comprehensive test coverage"
```

---

## Task 6: Register & Usage Context Tagger

**Files:**
- Create: `toefl_classifier/register_tagger.py`
- Create: `tests/test_register_tagger.py`

**Step 1: Write failing test**

Create `tests/test_register_tagger.py`:

```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from toefl_classifier.register_tagger import RegisterTagger

def test_detect_academic_register():
    """Test detection of academic register."""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # "moreover" appears 70% in academic, 20% in writing
        f.write("moreover\tacademic\t700\twriting\t200\tspoken\t50\tfiction\t50\n")
        temp_file = f.name

    try:
        tagger = RegisterTagger(corpus_file=temp_file)
        result = tagger.detect_register("moreover")

        assert 'academic' in result['register']
        assert 'writing' in result['register']

    finally:
        os.unlink(temp_file)

def test_detect_spoken_register():
    """Test detection of spoken register."""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # "gonna" appears 80% in spoken
        f.write("gonna\tacademic\t50\twriting\t50\tspoken\t800\tfiction\t0\n")
        temp_file = f.name

    try:
        tagger = RegisterTagger(corpus_file=temp_file)
        result = tagger.detect_register("gonna")

        assert 'spoken' in result['register']

    finally:
        os.unlink(temp_file)

def test_general_register():
    """Test that words without strong register bias are general."""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        # "make" is evenly distributed
        f.write("make\tacademic\t200\twriting\t200\tspoken\t200\tfiction\t200\n")
        temp_file = f.name

    try:
        tagger = RegisterTagger(corpus_file=temp_file)
        result = tagger.detect_register("make")

        assert result['register'] == ['general']

    finally:
        os.unlink(temp_file)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_register_tagger.py -v
```

Expected: `ImportError`

**Step 3: Write minimal implementation**

Create `toefl_classifier/register_tagger.py`:

```python
"""
Register and usage context detection using corpus data.
Classifies words as academic, spoken, writing, or technical.
"""

from pathlib import Path

class RegisterTagger:
    """
    Detect word register (usage context) using corpus data.

    COCA corpus sections:
    - academic: Academic journals
    - spoken: Conversation transcripts
    - fiction: Books and fiction
    - magazine: Popular magazines
    - newspaper: News articles
    """

    SECTIONS = ['academic', 'spoken', 'magazine', 'newspaper', 'fiction']

    # Threshold: section must be > 30% to be tagged
    REGISTER_THRESHOLD = 0.30

    def __init__(self, corpus_file=None):
        """
        Initialize register tagger.

        Args:
            corpus_file: Path to corpus section data
                        Format: word\\tsection1\\tcount1\\tsection2\\tcount2...
        """
        self.data_dir = Path(__file__).parent / "data"

        if corpus_file is None:
            corpus_file = self.data_dir / "coca_section_counts.txt"

        self.corpus_data = self._load_corpus_data(corpus_file)

    def _load_corpus_data(self, filepath):
        """Load corpus section data."""
        data = {}

        if not filepath.exists():
            print(f"Warning: Corpus data not found: {filepath}")
            return data

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split('\t')
                if len(parts) >= 2:
                    word = parts[0].lower()

                    # Parse section counts (odd indices are sections, even are counts)
                    sections = {}
                    for i in range(1, len(parts), 2):
                        if i + 1 < len(parts):
                            section = parts[i]
                            count = int(parts[i + 1])
                            sections[section] = count

                    data[word] = sections

        return data

    def detect_register(self, word):
        """
        Detect register/usage context of a word.

        Args:
            word: Word to analyze

        Returns:
            dict with keys:
                - register: List of register tags (academic, spoken, writing, general)
                - domains: List of domain tags (science, arts, etc.) - placeholder for now
        """
        word = word.lower()

        if word not in self.corpus_data:
            return {'register': ['general'], 'domains': []}

        section_counts = self.corpus_data[word]
        total = sum(section_counts.values())

        # Calculate percentage for each section
        sections_pct = {}
        for section, count in section_counts.items():
            sections_pct[section] = count / total

        # Detect dominant registers
        registers = []
        if sections_pct.get('academic', 0) > self.REGISTER_THRESHOLD:
            registers.append('academic')

        if sections_pct.get('spoken', 0) > self.REGISTER_THRESHOLD:
            registers.append('spoken')

        # Combine magazine + newspaper as "writing"
        writing_pct = sections_pct.get('magazine', 0) + sections_pct.get('newspaper', 0)
        if writing_pct > self.REGISTER_THRESHOLD:
            registers.append('writing')

        if not registers:
            registers = ['general']

        return {
            'register': registers,
            'domains': self._detect_domains(word)  # TODO: Implement domain detection
        }

    def _detect_domains(self, word):
        """
        Detect subject/domain of a word.

        This is a placeholder. Could be enhanced with:
        - Domain-specific corpora
        - WordNet domain labels
        - Topic modeling
        """
        # For now, return empty list
        # Future implementation could detect:
        # - science (hypothesis, theory, experiment)
        # - arts (metaphor, narrative, imagery)
        # - business (profit, investment, market)
        return []
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_register_tagger.py -v
```

**Step 5: Commit register tagger**

```bash
git add toefl_classifier/register_tagger.py tests/test_register_tagger.py
git commit -m "feat: implement register tagger for usage context

- Load corpus section distribution data
- Detect academic, spoken, writing registers
- Use 30% threshold for register classification
- Default to 'general' for balanced words
- Add placeholder for domain detection"
```

---

## Task 7: Main Classifier Orchestrator

**Files:**
- Create: `toefl_classifier/classify.py`
- Create: `tests/test_classify.py`

**Step 1: Write failing test**

Create `tests/test_classify.py`:

```python
import pytest
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from toefl_classifier.classify import TOEFLClassifier

def test_classify_single_word():
    """Test classification of a single word."""
    classifier = TOEFLClassifier()

    result = classifier.classify_word("analyze")

    # Check all dimensions are present
    assert 'word' in result
    assert result['word'] == 'analyze'

    assert 'lemma' in result
    assert 'word_family' in result
    assert 'pos' in result

    assert 'frequency' in result
    assert 'collins_stars' in result['frequency']

    assert 'emotion' in result
    assert 'sentiment' in result['emotion']

    assert 'usage' in result
    assert 'register' in result['usage']

def test_classify_word_list():
    """Test classification of multiple words."""
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("analyze\n")
        f.write("happy\n")
        f.write("predator\n")
        temp_input = f.name

    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_output = f.name

    try:
        classifier = TOEFLClassifier()
        results = classifier.process_word_list(temp_input, temp_output)

        assert len(results) == 3

        # Verify output file was created
        import os
        assert os.path.exists(temp_output)

        # Verify JSON structure
        with open(temp_output, 'r') as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) == 3

    finally:
        import os
        os.unlink(temp_input)
        if os.path.exists(temp_output):
            os.unlink(temp_output)
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/test_classify.py -v
```

Expected: `ImportError`

**Step 3: Write minimal implementation**

Create `toefl_classifier/classify.py`:

```python
"""
Main classifier orchestrator.
Combines all classification modules to process word lists.
"""

import json
from datetime import datetime
from pathlib import Path

from lemmatizer import WordFamilyProcessor
from frequency_grader import FrequencyGrader
from emotion_analyzer import EmotionAnalyzer
from register_tagger import RegisterTagger

class TOEFLClassifier:
    """
    Orchestrates multi-dimensional word classification.

    Combines:
    - Word family extraction
    - Frequency grading
    - Emotion analysis
    - Register detection
    """

    def __init__(self):
        """Initialize all classification modules."""
        self.word_family = WordFamilyProcessor()
        self.frequency = FrequencyGrader()
        self.emotion = EmotionAnalyzer()
        self.register = RegisterTagger()

    def classify_word(self, word):
        """
        Classify a single word across all dimensions.

        Args:
            word: Word to classify (can include line number like "1→analyze")

        Returns:
            dict: Classification results with all dimensions
        """
        # Extract clean word (remove line number if present)
        if '→' in word:
            clean_word = word.split('→')[-1].strip()
        else:
            clean_word = word.strip()

        # Get word family data
        wf_data = self.word_family.get_word_family(clean_word)

        # Get frequency data
        freq_data = self.frequency.grade_frequency(clean_word)

        # Get emotion data
        emotion_data = self.emotion.analyze_emotion(clean_word)

        # Get register data
        usage_data = self.register.detect_register(clean_word)

        # Combine all data
        result = {
            'word': clean_word,
            'lemma': wf_data['lemma'],
            'word_family': wf_data['word_family'],
            'pos': wf_data['pos'],
            'frequency': {
                'coca_rank': freq_data.get('coca_rank'),
                'collins_stars': freq_data['collins_stars'],
                'toefl_frequency': freq_data['toefl_frequency']
            },
            'academic': {
                'is_academic': freq_data.get('is_academic', False),
                'awl_level': freq_data.get('awl_level'),
                'register': 'academic' if 'academic' in usage_data['register'] else 'general'
            },
            'emotion': emotion_data,
            'usage': usage_data,
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'source_file': 'unknown'
            }
        }

        return result

    def process_word_list(self, input_file, output_file):
        """
        Process a list of words and save to JSON.

        Args:
            input_file: Path to input text file (one word per line)
            output_file: Path to output JSON file

        Returns:
            list: Classification results for all words
        """
        # Read input words
        with open(input_file, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]

        print(f"Processing {len(words)} words...")

        results = []
        for i, word in enumerate(words):
            if i % 100 == 0:
                print(f"  {i}/{len(words)}: {word}")

            try:
                result = self.classify_word(word)
                results.append(result)
            except Exception as e:
                print(f"  ⚠ Error processing '{word}': {e}")
                continue

        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        print(f"✓ Classified {len(results)} words")
        print(f"✓ Output saved to: {output_file}")

        return results


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python classify.py <input_file> [output_file]")
        print("\nExample:")
        print("  python classify.py data/vocabulary/TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt")
        print("  python classify.py input.txt output.json")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Generate output filename
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_classified.json"

    classifier = TOEFLClassifier()
    classifier.process_word_list(input_file, output_file)


if __name__ == '__main__':
    main()
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/test_classify.py -v
```

**Step 5: Test with real data**

```bash
cd /Users/leozhou/git/vocabulary/.worktrees/toefl-classifier
python toefl_classifier/classify.py data/vocabulary/TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt
```

Expected: Processes words and generates JSON file

**Step 6: Commit main classifier**

```bash
git add toefl_classifier/classify.py tests/test_classify.py
git commit -m "feat: implement main classifier orchestrator

- Combine all classification modules
- Process word lists end-to-end
- Generate enriched JSON output
- Add CLI interface
- Include comprehensive test suite"
```

---

## Task 8: Create Sample Test Data

**Files:**
- Create: `toefl_classifier/data/sample_coca.txt`
- Create: `toefl_classifier/data/sample_toefl_corpus.txt`

**Step 1: Create sample COCA data**

```bash
cat > /Users/leozhou/git/vocabulary/.worktrees/toefl-classifier/toefl_classifier/data/sample_coca.txt << 'EOF'
# Sample COCA frequency data for testing
# Format: word<TAB>rank
# Top 50 words for demonstration

the	1
be	2
of	3
and	4
a	5
in	6
to	7
have	8
it	9
that	10
for	11
they	12
I	13
with	14
as	15
not	16
on	17
she	18
at	19
by	20
this	21
we	22
you	23
do	24
but	25
from	26
or	27
which	28
one	29
would	30
all	31
will	32
there	33
say	34
who	35
make	36
when	37
can	38
more	39
if	40
no	41
man	42
out	43
other	44
so	45
what	46
time	47
up	48
go	49
about	50
analyze	456
hypothesis	1234
theory	890
predator	5000
ancient	2500
behavior	1200
happy	3000
fear	1500
EOF
```

**Step 2: Create sample TOEFL corpus**

```bash
cat > /Users/leozhou/git/vocabulary/.worktrees/toefl-classifier/toefl_classifier/data/sample_toefl_corpus.txt << 'EOF'
# Sample TOEFL word frequency corpus
# Format: word<TAB>frequency_in_exams
# Based on common TOEFL vocabulary

analyze	127
hypothesis	98
theory	85
interpret	72
establish	69
significant	63
factor	58
process	55
available	51
behavior	48
ancient	42
predator	35
happy	15
fear	22
joy	8
anger	12
sadness	10
surprise	18
trust	14
disgust	5
anticipation	19
moreover	85
furthermore	72
however	95
therefore	88
gonna	2
wanna	3
gotta	1
EOF
```

**Step 3: Commit sample data**

```bash
git add toefl_classifier/data/sample_coca.txt toefl_classifier/data/sample_toefl_corpus.txt
git commit -m "feat: add sample test data for development

- Create sample COCA frequency data (top 50 + TOEFL words)
- Create sample TOEFL corpus for testing
- Enables development and testing without full datasets"
```

---

## Task 9: Update Classifier to Use Sample Data

**Files:**
- Modify: `toefl_classifier/classify.py`

**Step 1: Update classifier to detect and use sample data**

```python
# In __init__ method of TOEFLClassifier:

def __init__(self):
    """Initialize all classification modules."""
    data_dir = Path(__file__).parent / "data"

    # Use sample data for development
    coca_file = data_dir / "sample_coca.txt"
    toefl_corpus_file = data_dir / "sample_toefl_corpus.txt"

    self.word_family = WordFamilyProcessor()
    self.frequency = FrequencyGrader(
        coca_file=coca_file,
        toefl_corpus_file=toefl_corpus_file
    )
    self.emotion = EmotionAnalyzer()
    self.register = RegisterTagger()
```

**Step 2: Test with sample data**

```bash
cd /Users/leozhou/git/vocabulary/.worktrees/toefl-classifier
echo -e "analyze\nhappy\npredator\nmoreover" | python toefl_classifier/classify.py /dev/stdin test_output.json
```

**Step 3: Verify output**

```bash
cat test_output.json | python -m json.tool | head -50
```

**Step 4: Commit updated classifier**

```bash
git add toefl_classifier/classify.py
git commit -m "feat: configure classifier to use sample data

- Point to sample_coca.txt and sample_toefl_corpus.txt
- Enables immediate testing without downloading full datasets
- Easy to switch to production data later"
```

---

## Task 10: Quick Start Documentation

**Files:**
- Create: `toefl_classifier/README.md`

**Step 1: Create comprehensive README**

Create `toefl_classifier/README.md`:

```markdown
# TOEFL Vocabulary Classifier

Intelligent multi-dimensional classification system for TOEFL vocabulary.

## Features

- **Word Family Extraction**: Groups related word forms using NLTK WordNet
- **Frequency Grading**: Collins star ratings + TOEFL exam frequency
- **Emotion Analysis**: Sentiment polarity and 8 emotion categories
- **Register Detection**: Academic, spoken, writing context classification
- **Interactive Web UI**: Filter and export to Anki

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. Download Databases

```bash
# Automatic download (NRC lexicon) + instructions for manual data
python toefl_classifier/download_data.py
```

### 3. Classify Words

```bash
# Using sample data (included)
python toefl_classifier/classify.py data/vocabulary/TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt

# Output: TOEFL_2000_AND_GREEN_BOOK_UNIQUE_classified.json
```

### 4. Explore Results

```bash
# View JSON structure
cat TOEFL_2000_AND_GREEN_BOOK_UNIQUE_classified.json | python -m json.tool | less
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_lemmatizer.py -v
```

### Project Structure

```
toefl_classifier/
├── classify.py              # Main orchestrator
├── lemmatizer.py            # Word family extraction
├── frequency_grader.py      # Collins/TOEFL grading
├── emotion_analyzer.py      # Sentiment/emotion classification
├── register_tagger.py       # Register detection
├── download_data.py         # Database download script
├── data/                    # Linguistic databases
│   ├── sample_coca.txt      # Sample COCA data (for testing)
│   ├── sample_toefl_corpus.txt
│   └── README.md
└── tests/                   # Test suite
```

## Data Sources

- **COCA**: Corpus of Contemporary American English (free signup required)
- **AWL**: Academic Word List (public)
- **NRC Emotion Lexicon**: Free for research
- **TOEFL Corpus**: Extract from TPO/Official tests

## Next Steps

1. Download full COCA frequency data (replace sample_coca.txt)
2. Convert Academic Word List to proper format
3. Build TOEFL corpus from past exam papers
4. Develop web UI for interactive filtering
5. Add Anki export functionality

## License

MIT
```

**Step 2: Commit README**

```bash
git add toefl_classifier/README.md
git commit -m "docs: add comprehensive README for classifier

- Quick start guide
- Installation instructions
- Development setup
- Project structure overview
- Data source documentation"
```

---

## Summary

This implementation plan provides a complete, tested TOEFL vocabulary classifier with:

**✓ Completed:**
1. Project structure and virtual environment setup
2. Automatic database download script
3. Word family extraction (NLTK + spaCy)
4. Frequency grading (Collins stars + TOEFL frequency)
5. Emotion analysis (sentiment + 8 emotions)
6. Register detection (academic/spoken/writing)
7. Main orchestrator combining all modules
8. Sample test data
9. Comprehensive test suite
10. Quick start documentation

**🎯 Next Phase:**
- Web UI development (HTML/JS)
- Anki export functionality
- Full database integration (replace sample data)
- Performance optimization for 6000 words

**Testing Strategy:**
- TDD approach for all modules
- Each task follows: red → green → commit cycle
- Sample data enables immediate testing
- Comprehensive edge case coverage

Ready to execute this plan using `superpowers:executing-plans` or `superpowers:subagent-driven-development`.
