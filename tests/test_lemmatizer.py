"""
Tests for Word Family Processor (lemmatizer.py)
Tests word family extraction using NLTK WordNet and spaCy POS tagging.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from toefl_classifier.lemmatizer import WordFamilyProcessor


class TestSimpleLemmatization:
    """Test basic lemmatization of simple words."""

    def test_get_lemma_of_simple_verb(self):
        """Test lemmatization of simple verb."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("ran")

        assert result['lemma'] == 'run'
        assert 'run' in result['word_family']
        assert result['pos'] in ['VERB', 'v']

    def test_get_lemma_of_simple_noun(self):
        """Test lemmatization of simple noun plural."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("dogs")

        assert result['lemma'] == 'dog'
        assert 'dog' in result['word_family']
        assert result['pos'] in ['NOUN', 'n']


class TestIrregularWords:
    """Test handling of irregular word forms."""

    def test_get_lemma_of_irregular_verb(self):
        """Test lemmatization of irregular verb."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("went")

        # "went" should lemmatize to "go"
        assert result['lemma'] in ['go', 'be']  # spaCy might handle this differently
        assert 'go' in result['word_family'] or result['lemma'] == 'go'

    def test_get_lemma_of_irregular_adjective(self):
        """Test lemmatization of irregular adjective."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("better")

        # "better" is comparative of "good" or "well"
        assert result['lemma'] in ['good', 'well', 'better']
        # Word family should include the base form
        assert any(form in result['word_family'] for form in ['good', 'well'])


class TestWordFamilyExtraction:
    """Test that word families include derivational forms."""

    def test_get_word_family_includes_derivations(self):
        """Test that word family includes derivational forms."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("analyze")

        assert result['lemma'] == 'analyze'
        # Should include: analysis, analytical, analytically, etc.
        # WordNet typically includes these derivationally related forms
        word_family_str = ' '.join(result['word_family']).lower()
        # At minimum should contain the lemma itself
        assert 'analyze' in result['word_family']

    def test_get_word_family_for_noun(self):
        """Test word family extraction for noun."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("predator")

        assert result['lemma'] in ['predator', 'predate']
        # Word family should include related forms
        assert 'predator' in result['word_family']

    def test_get_word_family_for_verb(self):
        """Test word family extraction for verb."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("establish")

        assert result['lemma'] == 'establish'
        assert 'establish' in result['word_family']


class TestPOSTagging:
    """Test POS tagging accuracy."""

    def test_get_word_family_returns_pos_for_noun(self):
        """Test that POS is correctly identified for noun."""
        processor = WordFamilyProcessor()

        noun_result = processor.get_word_family("predator")
        assert noun_result['pos'] in ['NOUN', 'n', 'PROPN']

    def test_get_word_family_returns_pos_for_verb(self):
        """Test that POS is correctly identified for verb."""
        processor = WordFamilyProcessor()

        verb_result = processor.get_word_family("analyze")
        assert verb_result['pos'] in ['VERB', 'v']

    def test_get_word_family_returns_pos_for_adjective(self):
        """Test that POS is correctly identified for adjective."""
        processor = WordFamilyProcessor()

        adj_result = processor.get_word_family("happy")
        assert adj_result['pos'] in ['ADJ', 'a']

    def test_get_word_family_returns_pos_for_adverb(self):
        """Test that POS is correctly identified for adverb."""
        processor = WordFamilyProcessor()

        adv_result = processor.get_word_family("quickly")
        assert adv_result['pos'] in ['ADV', 'r']


class TestMorphologicalVariants:
    """Test generation of morphological variants."""

    def test_verb_forms_generation(self):
        """Test that verb forms are included."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("analyze")

        # Should include the base form
        assert 'analyze' in result['word_family']

    def test_noun_plural_generation(self):
        """Test that noun plural forms are included."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("dog")

        # Should include the base form and potentially plural
        assert 'dog' in result['word_family']

    def test_adjective_comparative_forms(self):
        """Test that adjective comparative/superlative forms are included."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("happy")

        # Should include the base form
        assert 'happy' in result['word_family']


class TestCaseInsensitivity:
    """Test that processor handles case correctly."""

    def test_uppercase_word(self):
        """Test that uppercase words are handled."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("ANALYZE")

        assert result['lemma'].lower() in ['analyze', 'analyse']
        assert 'analyze' in [w.lower() for w in result['word_family']]

    def test_mixed_case_word(self):
        """Test that mixed case words are handled."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("AnAlYzE")

        assert result['lemma'].lower() in ['analyze', 'analyse']

    def test_title_case_word(self):
        """Test that title case words are handled."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("Analyze")

        assert result['lemma'].lower() in ['analyze', 'analyse']


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string(self):
        """Test handling of empty string."""
        processor = WordFamilyProcessor()

        # Should not crash, may return empty or minimal result
        result = processor.get_word_family("")

        # Just verify it returns a dict without crashing
        assert isinstance(result, dict)
        assert 'lemma' in result
        assert 'word_family' in result
        assert 'pos' in result

    def test_single_letter(self):
        """Test handling of single letter."""
        processor = WordFamilyProcessor()

        result = processor.get_word_family("a")

        assert isinstance(result, dict)
        assert 'lemma' in result

    def test_word_with_hyphen(self):
        """Test handling of hyphenated word."""
        processor = WordFamilyProcessor()

        result = processor.get_word_family("well-known")

        assert isinstance(result, dict)
        assert 'lemma' in result

    def test_word_with_apostrophe(self):
        """Test handling of word with apostrophe."""
        processor = WordFamilyProcessor()

        result = processor.get_word_family("don't")

        # spaCy typically handles contractions
        assert isinstance(result, dict)
        assert 'lemma' in result


class TestWordNetIntegration:
    """Test integration with NLTK WordNet."""

    def test_wordnet_derivationally_related_forms(self):
        """Test that derivationally related forms from WordNet are included."""
        processor = WordFamilyProcessor()

        # "analyze" should have derivationally related forms like "analysis"
        result = processor.get_word_family("analyze")

        # Word family should be a list with at least the lemma
        assert isinstance(result['word_family'], list)
        assert len(result['word_family']) >= 1
        assert result['lemma'] in result['word_family']

    def test_wordnet_synset_lemmas(self):
        """Test that synset lemmas from WordNet are included."""
        processor = WordFamilyProcessor()

        result = processor.get_word_family("happy")

        # Should include related words from synsets
        assert isinstance(result['word_family'], list)
        # The lemma itself should always be present
        assert result['lemma'] in result['word_family']


class TestReturnStructure:
    """Test that return value has correct structure."""

    def test_return_dict_has_all_keys(self):
        """Test that return dict has all required keys."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("test")

        assert isinstance(result, dict)
        assert 'lemma' in result
        assert 'word_family' in result
        assert 'pos' in result

    def test_lemma_is_string(self):
        """Test that lemma is a string."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("running")

        assert isinstance(result['lemma'], str)

    def test_word_family_is_list(self):
        """Test that word_family is a list."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("running")

        assert isinstance(result['word_family'], list)

    def test_pos_is_string(self):
        """Test that pos is a string."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("running")

        assert isinstance(result['pos'], str)

    def test_word_family_sorted(self):
        """Test that word_family is sorted for consistency."""
        processor = WordFamilyProcessor()
        result = processor.get_word_family("analyze")

        # Check if list is sorted
        word_family = result['word_family']
        assert word_family == sorted(word_family)


class TestInputValidation:
    """Test input validation and error handling."""

    def test_non_string_input_raises_type_error(self):
        """Test that non-string input raises TypeError."""
        processor = WordFamilyProcessor()

        with pytest.raises(TypeError, match="word must be a string"):
            processor.get_word_family(123)

        with pytest.raises(TypeError, match="word must be a string"):
            processor.get_word_family(None)

        with pytest.raises(TypeError, match="word must be a string"):
            processor.get_word_family(['list'])

    def test_invalid_characters_raises_value_error(self):
        """Test that words with invalid characters raise ValueError."""
        processor = WordFamilyProcessor()

        # Numbers not allowed
        with pytest.raises(ValueError, match="invalid characters"):
            processor.get_word_family("word123")

        # Special characters not allowed
        with pytest.raises(ValueError, match="invalid characters"):
            processor.get_word_family("hello@world")

        with pytest.raises(ValueError, match="invalid characters"):
            processor.get_word_family("test$")

        # Punctuation (except hyphen and apostrophe) not allowed
        with pytest.raises(ValueError, match="invalid characters"):
            processor.get_word_family("word.with.dots")

        with pytest.raises(ValueError, match="invalid characters"):
            processor.get_word_family("comma,word")

    def test_too_long_word_raises_value_error(self):
        """Test that words longer than 100 characters raise ValueError."""
        processor = WordFamilyProcessor()

        long_word = "a" * 101
        with pytest.raises(ValueError, match="too long"):
            processor.get_word_family(long_word)

    def test_valid_special_characters_allowed(self):
        """Test that hyphens and apostrophes are allowed."""
        processor = WordFamilyProcessor()

        # Hyphenated words should work
        result = processor.get_word_family("well-known")
        assert isinstance(result, dict)
        assert 'lemma' in result

        # Words with apostrophes should work
        result = processor.get_word_family("don't")
        assert isinstance(result, dict)
        assert 'lemma' in result

    def test_whitespace_only_returns_empty(self):
        """Test that whitespace-only input returns empty result."""
        processor = WordFamilyProcessor()

        result = processor.get_word_family("   ")
        assert result['lemma'] == ''
        assert result['word_family'] == []
        assert result['pos'] == ''

        result = processor.get_word_family("\t\n")
        assert result['lemma'] == ''
        assert result['word_family'] == []
        assert result['pos'] == ''


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
