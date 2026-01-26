# TOEFL Vocabulary Intelligent Classifier Design

**Date:** 2025-01-26
**Author:** Claude + Leo
**Status:** Design Approved

## Overview

Build an intelligent classification system for 6000 TOEFL vocabulary words to enable efficient memorization through strategic categorization and association. The system groups words by multiple dimensions (word families, frequency, emotion, register) and provides an interactive web UI for filtering and export.

**Primary Goals:**
- Efficient memorization through word families and spaced repetition optimization
- Deep understanding via semantic connections (emotion, collocations, context)
- Exam optimization with TOEFL-specific frequency and academic vocabulary prioritization

## System Architecture

### 3-Tier Pipeline

```
TOEFL_6000.txt → Python Processor → vocabulary_classified.json → Web UI → Export (Anki/Markdown)
```

**Tier 1: Data Processing (Python)**
- NLTK WordNet for lemmatization and word families
- spaCy for POS tagging and dependency parsing
- COCA frequency dataset for Collins grading
- Academic Word List (AWL) integration
- NRC Emotion Lexicon for sentiment classification
- Output: Enriched JSON database

**Tier 2: Web UI (JavaScript)**
- Extend existing `classify/index.html`
- Multi-dimensional filter sidebar
- Color-coded word badges
- Real-time client-side filtering

**Tier 3: Export Layer**
- Anki-compatible CSV generation
- Markdown reports by category
- Filter preset management

## Data Schema

### JSON Structure

```json
{
  "word": "analyze",
  "lemma": "analyze",
  "word_family": ["analyze", "analyzes", "analyzed", "analyzing", "analysis", "analytical", "analytically"],
  "pos": "verb",
  "frequency": {
    "coca_rank": 456,
    "collins_stars": 5,
    "toefl_frequency": "high"
  },
  "academic": {
    "is_academic": true,
    "awl_level": 1,
    "register": "academic"
  },
  "emotion": {
    "sentiment": "neutral",
    "emotions": ["trust", "anticipation"]
  },
  "usage": {
    "register": ["academic", "writing"],
    "domains": ["science", "research"]
  },
  "metadata": {
    "processed_at": "2025-01-26",
    "source_file": "TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt"
  }
}
```

### Classification Dimensions

**Dimension A: Word Family/Lemma**
- Groups morphological variants (run/ran/running)
- Links derivationally related forms (analyze/analysis/analytical)
- Enables batch learning of word families

**Dimension B: Frequency/Importance**
- Collins COCA grading (1-5 stars based on frequency rank)
- TOEFL exam frequency (high/medium/low from test corpus)
- Academic Word List membership (570 core academic words)

**Dimension C: Semantic/Emotional**
- Sentiment polarity (positive/negative/neutral)
- Specific emotions (8 categories: joy, trust, fear, surprise, sadness, disgust, anger, anticipation)
- Enables affective learning strategies

**Dimension D: Register/Usage Context**
- Academic vs. Spoken vs. Writing vs. Technical
- Domain classification (science, arts, business)
- Informs appropriate usage contexts

**Dimension E: Part of Speech**
- Explicit POS filter (noun/verb/adjective/adverb)
- Critical for accurate word family grouping

## File Structure

```
vocabulary/
├── data/
│   ├── vocabulary/
│   │   └── TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt  (existing)
│   ├── databases/                              (auto-downloaded)
│   │   ├── coca_frequency.txt
│   │   ├── academic_word_list.txt
│   │   └── nrc_emotion_lexicon.txt
│   └── output/
│       └── vocabulary_classified.json           (generated)
├── toefl_classifier/                            (new module)
│   ├── classify.py                              (main orchestrator)
│   ├── lemmatizer.py                            (word family logic)
│   ├── frequency_grader.py                      (Collins/TOEFL grading)
│   ├── emotion_analyzer.py                      (sentiment/emotion)
│   ├── register_tagger.py                       (academic/spoken/technical)
│   └── download_data.py                         (automatic database downloads)
└── web-ui/
    ├── index.html                               (extend existing)
    ├── css/styles.css
    └── js/
        ├── filters.js                           (new)
        ├── display.js                           (new)
        └── export.js                            (new)
```

## Algorithm Specifications

### Word Family Extraction

```python
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy

def get_word_family(word):
    """Returns lemma, all word forms, and POS"""
    doc = nlp(word)
    lemma = token.lemma_

    # Collect from WordNet synsets
    word_family = set()
    for synset in wordnet.synsets(lemma):
        for lemma_obj in synset.lemmas():
            word_family.add(lemma_obj.name())

    return {
        'lemma': lemma,
        'word_family': list(word_family),
        'pos': token.pos_
    }
```

### Frequency Grading

```python
COLLINS_STAR_THRESHOLDS = {
    5: (1, 1000),
    4: (1001, 3000),
    3: (3001, 6000),
    2: (6001, 12000),
    1: (12001, 20000)
}

def grade_frequency(word, coca_data, awl_data, toefl_corpus):
    coca_rank = coca_data.get(word, 99999)

    # Determine Collins stars
    collins_stars = 1
    for stars, (min_rank, max_rank) in COLLINS_STAR_THRESHOLDS.items():
        if min_rank <= coca_rank <= max_rank:
            collins_stars = stars
            break

    # TOEFL frequency
    toefl_freq = toefl_corpus.get(word, 0)
    if toefl_freq > 50:
        toefl_level = "high"
    elif toefl_freq > 10:
        toefl_level = "medium"
    else:
        toefl_level = "low"

    return {
        'coca_rank': coca_rank,
        'collins_stars': collins_stars,
        'toefl_frequency': toefl_level,
        'is_academic': awl_data.get(word) is not None
    }
```

### Emotion Analysis

```python
def analyze_emotion(word, nrc_lexicon):
    """Returns sentiment polarity + specific emotions"""
    emotions_present = []
    for emotion in EMOTIONS:
        if nrc_lexicon.get(f"{word}\t{emotion}") == "1":
            emotions_present.append(emotion)

    # Calculate sentiment
    positive = sum(1 for e in emotions_present if e in ['joy', 'trust', 'anticipation'])
    negative = sum(1 for e in emotions_present if e in ['anger', 'fear', 'sadness', 'disgust'])

    if positive > negative:
        sentiment = "positive"
    elif negative > positive:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {'sentiment': sentiment, 'emotions': emotions_present}
```

### Register Detection

```python
def detect_register(word, coca_section_counts):
    """Determine primary usage context"""
    total = sum(coca_section_counts.values())
    sections = {k: (v/total)*100 for k, v in coca_section_counts.items()}

    registers = []
    if sections.get('academic', 0) > 30:
        registers.append('academic')
    if sections.get('spoken', 0) > 30:
        registers.append('spoken')
    if sections.get('magazine', 0) + sections.get('newspaper', 0) > 30:
        registers.append('writing')

    return {
        'register': registers if registers else ['general'],
        'domains': detect_technical_domain(word)
    }
```

## Web UI Design

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  TOEFL Vocabulary Classifier                      [Export ▾] │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  FILTERS     │  WORD GRID (6000 words)                      │
│              │  ┌──────────┬──────────┬──────────┐          │
│  □ Word      │  │ analyze  │ ancient  │ behavior │          │
│    Filter    │  │ [5⭐][Ac] │ [3⭐][Ne] │ [4⭐][Ac] │          │
│              │  │ [😐][Wr]  │ [😐][Ac]  │ [😐][Ac]  │          │
│  □ Frequency │  └──────────┴──────────┴──────────┘          │
│    ⭐⭐⭐⭐⭐  │                                               │
│    ○ High    │  Load more...                                 │
│    ○ Medium  │                                               │
│    ○ Low     │  Showing: 1-50 of 6,000                       │
│              │                                               │
│  □ Emotion   │  [Clear Filters] [Apply] [Export Anki]       │
│    😊 Pos    │                                               │
│    😐 Neu    │                                               │
│    ☹️ Neg    │                                               │
│              │                                               │
│  □ Register  │                                               │
│    ☑ Academic│                                               │
│    ☑ Spoken  │                                               │
│    ☐ Writing │                                               │
│              │                                               │
│  □ POS       │                                               │
│    ☑ Noun    │                                               │
│    ☑ Verb    │                                               │
│    ☑ Adj     │                                               │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

### Badge Color Coding

- **Frequency stars**: ⭐⭐⭐⭐⭐ (gold → bronze gradient)
- **Academic**: [Ac] (blue badge)
- **Emotion**: 😊 (green), 😐 (gray), ☹️ (red)
- **Register**: [Wr] (purple), [Sp] (orange), [Te] (green)

### Filter Logic

Real-time client-side filtering with OR/AND logic:
- Multiple selection within category = OR (e.g., "Academic OR Spoken")
- Different categories = AND (e.g., "Academic AND Positive")

## Implementation Roadmap

### Phase 1: Environment Setup
```bash
python -m venv venv
source venv/bin/activate
pip install nltk spacy numpy pandas
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
python -m spacy download en_core_web_sm
```

### Phase 2: Automatic Data Downloads
```python
# toefl_classifier/download_data.py
def download_all_databases():
    """Automatically download all required databases"""
    download_coca_frequency()
    download_academic_word_list()
    download_nrc_emotion_lexicon()
    download_toefl_corpus()
```

### Phase 3: Build Classification Modules
- `lemmatizer.py` - Word family extraction
- `frequency_grader.py` - Collins/TOEFL grading
- `emotion_analyzer.py` - Sentiment classification
- `register_tagger.py` - Register detection
- `classify.py` - Main orchestrator

### Phase 4: Web UI Development
- Extend `classify/index.html` with filter sidebar
- Implement `filters.js` for real-time filtering
- Create `display.js` for word card rendering
- Add `export.js` for Anki/Markdown export

### Phase 5: Testing & Validation
- Spot-check 100 random words
- Validate word family grouping
- Cross-check Collins grading
- Test emotion classification

## Testing Strategy

### Manual Validation Checklist

**Word Lemmatization**
- [ ] "ran" → "run"
- [ ] "better" → "good"
- [ ] "analyses" → "analysis"

**Word Families**
- [ ] "analyze" includes: analysis, analytical, analytically
- [ ] No false positives for homographs

**Frequency Grading**
- [ ] "the" → 5 stars
- [ ] Cross-check 10 words with official Collins

**Emotion Analysis**
- [ ] "happy" → positive + joy
- [ ] "fear" → negative + fear
- [ ] "analyze" → neutral

**Register Detection**
- [ ] "moreover" → academic + writing
- [ ] "gonna" → spoken
- [ ] "hypothesis" → academic

### Performance Benchmarks
- Processing time: < 5 minutes for 6000 words
- Web UI load time: < 2 seconds
- Filter response: < 100ms

## Future Enhancements

1. **Etymology/Word Origins**
   - Latin/Greek root detection
   - Morphological breakdown
   - Related words by root

2. **Collocations & Usage Examples**
   - Common word pairs from TOEFL corpus
   - Real example sentences
   - TOEFL-style usage patterns

3. **Personal Difficulty Scoring**
   - Track wrong answers in Anki
   - Personalized "difficult words" list
   - Spaced repetition integration

4. **Practice Mode**
   - Fill-in-blank exercises
   - Word-matching games
   - Timed quiz mode

5. **Progress Tracking**
   - Learned vs. remaining visualization
   - Statistics by category
   - Study schedule generation

## Technical Requirements

**Python Dependencies**
- nltk (WordNet, lemmatization)
- spacy (POS tagging, dependency parsing)
- numpy (data processing)
- pandas (CSV handling)

**Data Sources**
- COCA frequency dataset (free signup required)
- Academic Word List (public)
- NRC Emotion Lexicon (free for research)
- TOEFL corpus (TPO/Official tests)

**Browser Compatibility**
- Modern browsers with ES6+ support
- Local file:// protocol support

## Success Criteria

1. All 6000 words classified across 5 dimensions
2. Interactive web UI with sub-100ms filter response
3. Export to Anki CSV format
4. Automatic data download and setup
5. Validation accuracy > 90% on spot checks

---

**Next Steps:** Implementation planning with git worktree for isolated development environment.
