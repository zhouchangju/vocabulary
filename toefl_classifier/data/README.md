# Linguistic Databases Directory

This directory stores linguistic databases and reference data for the TOEFL vocabulary classifier.

## Expected Contents

### Linguistic Databases
- **COCA (Corpus of Contemporary American English)**: Word frequency data
  - `coca_word_freq.txt` - Word frequency rankings from COCA corpus
  - Source: https://www.english-corpora.org/coca/

- **WordNet**: Lexical database
  - Automatically accessed via NLTK
  - Provides synsets, word relationships, and semantic categories

- **spaCy Linguistic Data**: English language model
  - Model: `en_core_web_sm`
  - Provides POS tagging, dependency parsing, and named entity recognition

### Frequency Reference Files
- **Frequency Bands**: Word frequency categorization data
  - High frequency (top 1000-3000 words)
  - Medium frequency (3000-8000 words)
  - Low frequency (8000+ words)

- **Register Data**: Usage context classifications
  - Academic, spoken, fiction, newspaper categories

### Output Files
- **Processed Vocabulary**: Classified word lists with metadata
  - TOEFL words with frequency scores
  - Emotional characteristics
  - Register classifications
  - Word family groupings

## Data Sources

### COCA (Corpus of Contemporary American English)
- **Description**: 1+ billion word corpus of American English
- **Coverage**: 1990-2019 (present-day), evenly divided between spoken, fiction, popular magazines, newspapers, and academic texts
- **Usage**: Provides frequency rankings and register distribution
- **License**: Free for academic use (registration required)
- **URL**: https://www.english-corpora.org/coca/

### WordNet (via NLTK)
- **Description**: Lexical database of English semantic relations
- **Coverage**: Nouns, verbs, adjectives, adverbs
- **Usage**: Synonyms, hypernyms, hyponyms, word meanings
- **License**: Open source (Princeton University)
- **URL**: https://wordnet.princeton.edu/

### spaCy English Models
- **Description**: Industrial-strength NLP models
- **Coverage**: POS tagging, dependency parsing, named entity recognition
- **Usage**: Grammatical analysis and part-of-speech tagging
- **License**: MIT
- **URL**: https://spacy.io/models/en

## File Naming Conventions

- `coca_word_freq.txt` - Raw COCA frequency data
- `coca_processed.csv` - Processed COCA data with frequency bands
- `wordnet_synsets.json` - Cached WordNet data
- `register_data.json` - Register classification data
- `toefl_classified.csv` - Final classified TOEFL vocabulary

## Notes

- Only the README.md file is tracked by git
- All data files are git-ignored (see .gitignore)
- Use the automatic download script (Task 2) to fetch databases
- Ensure data files are properly formatted and UTF-8 encoded
- Backup original data files before processing
