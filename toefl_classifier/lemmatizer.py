"""
Word family extraction using NLTK WordNet and spaCy.
Groups morphological and derivationally related forms.
"""

from collections.abc import Set
from typing import Dict, List

import spacy
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


class WordFamilyProcessor:
    """Extract lemmas and word families using WordNet and spaCy."""

    def __init__(self):
        """Initialize spaCy model and NLTK lemmatizer."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError as e:
            raise OSError(
                "spaCy model not found. Run: python -m spacy download en_core_web_sm"
            ) from e

        self.lemmatizer = WordNetLemmatizer()

    def get_word_family(self, word: str) -> Dict[str, object]:
        """
        Extract lemma, word family, and POS for a given word.

        Args:
            word: Single word string

        Returns:
            dict with keys:
                - lemma: Base form of the word
                - word_family: List of related word forms
                - pos: Part of speech (NOUN, VERB, ADJ, ADV, or spaCy tags)

        Raises:
            TypeError: If word is not a string
            ValueError: If word contains invalid characters or is too long
        """
        # Input validation
        if not isinstance(word, str):
            raise TypeError(f"word must be a string, got {type(word).__name__}")

        # Handle empty string
        if not word or not word.strip():
            return {
                'lemma': '',
                'word_family': [],
                'pos': ''
            }

        # Validate word content - only allow letters, hyphens, and apostrophes
        word = word.strip()
        if not all(char.isalpha() or char in {"-", "'"} for char in word):
            raise ValueError(
                f"word contains invalid characters: {word!r}. "
                "Only letters, hyphens, and apostrophes are allowed."
            )

        # Validate word length (prevent unreasonably long inputs)
        if len(word) > 100:
            raise ValueError(
                f"word is too long ({len(word)} characters). Maximum length is 100 characters."
            )

        # Process with spaCy for POS
        try:
            doc = self.nlp(word)
            if len(doc) == 0:
                return {
                    'lemma': word.lower(),
                    'word_family': [word.lower()],
                    'pos': 'UNKNOWN'
                }
            token = doc[0]
        except Exception as e:
            raise RuntimeError(f"spaCy processing failed for word {word!r}") from e

        # Get base lemma from spaCy
        lemma = token.lemma_

        # Collect word family from WordNet
        word_family: Set = set()
        word_family.add(lemma.lower())  # Always include the lemma (lowercased)

        # Get all derivationally related forms from WordNet
        # Use the spaCy lemma as the base for WordNet lookup
        try:
            for synset in wordnet.synsets(lemma.lower()):
                for lemma_obj in synset.lemmas():
                    # Add the lemma form
                    word_family.add(lemma_obj.name())

                    # Add derivationally related forms
                    if lemma_obj.derivationally_related_forms():
                        for related in lemma_obj.derivationally_related_forms():
                            word_family.add(related.name())
        except (AttributeError, LookupError, RuntimeError) as e:
            # If WordNet lookup fails, log and continue with spaCy lemma
            # Specific exceptions: AttributeError (corrupted data), LookupError (missing data),
            # RuntimeError (WordNet internal errors)
            pass

        # Add common morphological variants based on POS
        pos = token.pos_

        # Normalize POS to consistent format
        pos_normalized = self._normalize_pos(pos)

        if pos_normalized == 'VERB':
            # Add -ing, -ed, -s forms
            word_family.update(self._get_verb_forms(lemma.lower()))
        elif pos_normalized == 'NOUN':
            # Add plural forms
            word_family.update(self._get_noun_forms(lemma.lower()))
        elif pos_normalized == 'ADJ':
            # Add comparative/superlative
            word_family.update(self._get_adjective_forms(lemma.lower()))

        # Remove underscores (WordNet uses underscores for spaces)
        # and convert to hyphens for multi-word expressions
        word_family_clean = [w.replace('_', '-') for w in word_family]

        # Sort for consistent output
        word_family_sorted = sorted(list(word_family_clean))

        return {
            'lemma': lemma.lower(),
            'word_family': word_family_sorted,
            'pos': pos
        }

    def _normalize_pos(self, pos: str) -> str:
        """
        Normalize POS tags to consistent format.

        Args:
            pos: spaCy POS tag

        Returns:
            Normalized POS string (NOUN, VERB, ADJ, ADV)
        """
        pos_mapping = {
            'NOUN': 'NOUN',
            'PROPN': 'NOUN',  # Proper nouns -> NOUN
            'VERB': 'VERB',
            'AUX': 'VERB',    # Auxiliary verbs -> VERB
            'ADJ': 'ADJ',
            'ADV': 'ADV'
        }

        return pos_mapping.get(pos, pos)

    def _get_verb_forms(self, lemma: str) -> Set[str]:
        """Generate common verb forms."""
        forms: Set[str] = set()

        # Simple rules (not perfect, but good enough for most cases)
        if lemma.endswith('e'):
            forms.add(lemma + 'd')  # -ed
            forms.add(lemma + 's')  # -3rd person
        else:
            forms.add(lemma + 'ed')
            forms.add(lemma + 's')

        forms.add(lemma + 'ing')  # -ing

        # Handle consonant + 'y' ending (study -> studies)
        if lemma.endswith('y') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
            forms.add(lemma[:-1] + 'ies')
            forms.add(lemma[:-1] + 'ied')

        return forms

    def _get_noun_forms(self, lemma: str) -> Set[str]:
        """Generate common noun forms."""
        forms: Set[str] = set()

        # Simple pluralization rules
        if lemma.endswith('y'):
            if len(lemma) > 1 and lemma[-2] not in 'aeiou':
                forms.add(lemma[:-1] + 'ies')
            else:
                forms.add(lemma + 's')
        elif lemma.endswith('s') or lemma.endswith('x') or lemma.endswith('ch') or lemma.endswith('sh'):
            forms.add(lemma + 'es')
        elif lemma.endswith('f'):
            forms.add(lemma[:-1] + 'ves')
        elif lemma.endswith('fe'):
            forms.add(lemma[:-2] + 'ves')
        else:
            forms.add(lemma + 's')

        return forms

    def _get_adjective_forms(self, lemma: str) -> Set[str]:
        """Generate common adjective forms."""
        forms: Set[str] = set()

        # Comparative/superlative
        if lemma.endswith('e'):
            forms.add(lemma + 'r')   # comparative
            forms.add(lemma + 'st')  # superlative
        else:
            if len(lemma) > 2:
                forms.add(lemma + 'er')
                forms.add(lemma + 'est')

        # Handle 'y' ending (happy -> happier)
        if lemma.endswith('y') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
            forms.add(lemma[:-1] + 'ier')
            forms.add(lemma[:-1] + 'iest')

        return forms
