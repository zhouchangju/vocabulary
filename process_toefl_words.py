#!/usr/bin/env python3
"""
TOEFL Vocabulary Processing Script
Processes the 6000-word TOEFL vocabulary list and generates classified output.
"""

import sys
import json
from pathlib import Path

def main():
    """Main processing function."""
    print("=" * 70)
    print("TOEFL VOCABULARY CLASSIFIER")
    print("=" * 70)
    print()
    print("⚠️  SETUP REQUIRED:")
    print("   1. Install dependencies: pip install -r toefl_classifier/requirements.txt")
    print("   2. Download NLTK data: python -c \"import nltk; nltk.download('wordnet')\"")
    print("   3. Download spaCy: python -m spacy download en_core_web_sm")
    print()
    print("Then run this script again to process your vocabulary.")
    print()
    print("=" * 70)

    # Check if dependencies are available
    try:
        import toefl_classifier
        from toefl_classifier.orchestrator import TOEFLWordClassifier
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print()
        print("Please run:")
        print("  cd /Users/leozhou/git/vocabulary")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate")
        print("  pip install -r toefl_classifier/requirements.txt")
        print("  python -m spacy download en_core_web_sm")
        return 1

    print("✓ Dependencies loaded")
    print()

    # Check input file
    input_file = Path("data/vocabulary/TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt")
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return 1

    print(f"✓ Input file found: {input_file}")
    print()

    # Load words
    print("Loading vocabulary...")
    words = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Extract word (handle format "123→word")
            if '→' in line:
                word = line.split('→')[-1].strip()
            else:
                word = line.strip()

            if word:
                words.append(word)

    print(f"✓ Loaded {len(words)} words")
    print()

    # Initialize classifier
    print("Initializing classifier...")
    classifier = TOEFLWordClassifier()
    print()

    # Process words
    import time
    print(f"Processing {len(words)} words...")
    print()

    results = []
    errors = []
    start_time = time.time()

    batch_size = 100
    for i in range(0, len(words), batch_size):
        batch = words[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(words) + batch_size - 1) // batch_size

        print(f"  Batch {batch_num}/{total_batches} (words {i+1}-{min(i+batch_size, len(words))})")

        for word in batch:
            try:
                result = classifier.classify_word(word)
                results.append(result)
            except Exception as e:
                errors.append((word, str(e)))

    elapsed = time.time() - start_time
    print()
    if len(results) > 0:
        print(f"✓ Classified {len(results)} words in {elapsed:.1f}s ({elapsed/len(results)*1000:.1f}ms per word)")
    else:
        print(f"⚠ No words successfully classified in {elapsed:.1f}s")
    print(f"  Errors: {len(errors)}")

    if errors:
        print()
        print("First 10 errors:")
        for word, error in errors[:10]:
            print(f"  - {word}: {error}")
    print()

    # Save results
    output_file = Path("data/vocabulary/TOEFL_CLASSIFIED.json")
    print(f"Saving results to {output_file}...")

    # Convert to JSON-serializable format
    serializable_results = []
    for r in results:
        serializable = {
            'word': r['word'],
            'lemma': r['lemma'],
            'word_family': r['word_family'],
            'pos': str(r['pos']),
        }

        if 'frequency' in r:
            serializable['frequency'] = {
                'band': str(r['frequency'].get('band', 'Unknown')),
            }

        if 'emotion' in r:
            serializable['emotion'] = {
                'primary': r['emotion'].get('primary', 'Unknown'),
                'emotions': [str(e) for e in r['emotion'].get('emotions', [])],
            }

        if 'register' in r:
            serializable['register'] = {
                'register': str(r['register'].get('register', 'Unknown')),
            }

        serializable_results.append(serializable)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2)

    print(f"✓ Saved {len(serializable_results)} classified words to {output_file}")
    print()

    # Show sample
    if results:
        print("Sample classification:")
        print("-" * 70)
        sample = results[0]
        print(f"Word: {sample['word']}")
        print(f"Lemma: {sample['lemma']}")
        print(f"POS: {sample['pos']}")
        print(f"Word Family Size: {len(sample['word_family'])}")
        print("-" * 70)
    print()

    print("=" * 70)
    print("✓ Processing complete!")
    print("=" * 70)
    print()
    print(f"Output file: {output_file}")
    print(f"Ready for web UI filtering and Anki export!")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
