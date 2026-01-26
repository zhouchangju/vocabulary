"""
Main Orchestrator Module - Integrates all classifier modules.
Coordinates lemmatizer, frequency grader, emotion analyzer, and register tagger.
"""

import json
import csv
from io import StringIO
from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum

from toefl_classifier.lemmatizer import WordFamilyProcessor
from toefl_classifier.frequency_grader import FrequencyGrader, FrequencyBand
from toefl_classifier.emotion_analyzer import EmotionAnalyzer, EmotionType
from toefl_classifier.register_tagger import RegisterTagger, RegisterType


class TOEFLWordClassifier:
    """
    Main orchestrator for TOEFL word classification.
    Integrates all analysis modules for comprehensive word analysis.
    """

    def __init__(
        self,
        lemmatizer: Optional[WordFamilyProcessor] = None,
        frequency_grader: Optional[FrequencyGrader] = None,
        emotion_analyzer: Optional[EmotionAnalyzer] = None,
        register_tagger: Optional[RegisterTagger] = None,
        parallel: bool = False,
        use_cache: bool = False
    ):
        """
        Initialize TOEFLWordClassifier with analysis modules.

        Args:
            lemmatizer: WordFamilyProcessor instance (created if None)
            frequency_grader: FrequencyGrader instance (created if None)
            emotion_analyzer: EmotionAnalyzer instance (created if None)
            register_tagger: RegisterTagger instance (created if None)
            parallel: Enable parallel processing for batches
            use_cache: Enable caching of results
        """
        self.lemmatizer = lemmatizer or WordFamilyProcessor()
        self.frequency_grader = frequency_grader or FrequencyGrader()
        self.emotion_analyzer = emotion_analyzer or EmotionAnalyzer()
        self.register_tagger = register_tagger or RegisterTagger()

        self.parallel = parallel
        self.use_cache = use_cache
        self._cache: Dict[str, Dict[str, Any]] = {}

    def classify_word(
        self,
        word: str,
        skip_lemmatization: bool = False,
        skip_frequency: bool = False,
        skip_emotion: bool = False,
        skip_register: bool = False
    ) -> Dict[str, Any]:
        """
        Classify a single word using all analysis modules.

        Args:
            word: Word to classify
            skip_lemmatization: Skip lemmatization step
            skip_frequency: Skip frequency grading
            skip_emotion: Skip emotion analysis
            skip_register: Skip register tagging

        Returns:
            Dictionary with comprehensive word analysis:
                - word: Original word
                - lemma: Base form (if lemmatization enabled)
                - word_family: List of related forms (if lemmatization enabled)
                - pos: Part of speech (if lemmatization enabled)
                - frequency: Frequency analysis dict (if enabled)
                - emotion: Emotion analysis dict (if enabled)
                - register: Register analysis dict (if enabled)
                - error: Error message (if any module failed)

        Raises:
            TypeError: If word is not a string
        """
        if not isinstance(word, str):
            raise TypeError(f"word must be a string, got {type(word).__name__}")

        # Check cache
        if self.use_cache and word in self._cache:
            return self._cache[word]

        result = {
            'word': word.lower().strip()
        }

        # Lemmatization
        if not skip_lemmatization:
            try:
                lemma_result = self.lemmatizer.get_word_family(word)
                result.update({
                    'lemma': lemma_result['lemma'],
                    'word_family': lemma_result['word_family'],
                    'pos': lemma_result['pos']
                })
            except Exception as e:
                result['lemmatization_error'] = str(e)
                result['lemma'] = word.lower().strip()
                result['word_family'] = [word.lower().strip()]
                result['pos'] = 'UNKNOWN'

        # Frequency grading
        if not skip_frequency:
            try:
                frequency_result = self.frequency_grader.grade_word(word)
                result['frequency'] = {
                    'band': frequency_result['band'],
                    'rank': frequency_result['rank'],
                    'normalized_score': frequency_result['normalized_score']
                }
            except Exception as e:
                result['frequency_error'] = str(e)
                result['frequency'] = {
                    'band': FrequencyBand.BEYOND,
                    'rank': float('inf'),
                    'normalized_score': 0.0
                }

        # Emotion analysis
        if not skip_emotion:
            try:
                emotion_result = self.emotion_analyzer.analyze_emotion(word)
                result['emotion'] = {
                    'emotions': emotion_result['emotions'],
                    'primary_emotion': emotion_result['primary_emotion'],
                    'confidence': emotion_result['confidence'],
                    'emotion_scores': emotion_result['emotion_scores']
                }
            except Exception as e:
                result['emotion_error'] = str(e)
                result['emotion'] = {
                    'emotions': [],
                    'primary_emotion': None,
                    'confidence': 0.0,
                    'emotion_scores': {}
                }

        # Register tagging
        if not skip_register:
            try:
                register_result = self.register_tagger.classify_register(word)
                result['register'] = {
                    'register_type': register_result['register'],
                    'confidence': register_result['confidence'],
                    'context': register_result['context']
                }
            except Exception as e:
                result['register_error'] = str(e)
                result['register'] = {
                    'register_type': RegisterType.NEUTRAL,
                    'confidence': 0.0,
                    'context': 'unknown'
                }

        # Cache result
        if self.use_cache:
            self._cache[word] = result

        return result

    def classify_words(
        self,
        words: List[str],
        skip_lemmatization: bool = False,
        skip_frequency: bool = False,
        skip_emotion: bool = False,
        skip_register: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Classify multiple words using all analysis modules.

        Args:
            words: List of words to classify
            skip_lemmatization: Skip lemmatization step
            skip_frequency: Skip frequency grading
            skip_emotion: Skip emotion analysis
            skip_register: Skip register tagging

        Returns:
            List of dictionaries with comprehensive word analysis

        Raises:
            TypeError: If words is not a list or contains non-string elements
        """
        if not isinstance(words, list):
            raise TypeError(f"words must be a list, got {type(words).__name__}")

        # Validate all elements are strings
        for i, word in enumerate(words):
            if not isinstance(word, str):
                raise TypeError(
                    f"All words must be strings. "
                    f"Element {i} is {type(word).__name__}"
                )

        results = []
        for word in words:
            try:
                result = self.classify_word(
                    word,
                    skip_lemmatization=skip_lemmatization,
                    skip_frequency=skip_frequency,
                    skip_emotion=skip_emotion,
                    skip_register=skip_register
                )
                results.append(result)
            except Exception as e:
                # Add error result but continue processing
                results.append({
                    'word': word if isinstance(word, str) else str(word),
                    'error': str(e)
                })

        return results

    def generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics from classification results.

        Args:
            results: List of classification results

        Returns:
            Dictionary with summary statistics
        """
        total_words = len(results)

        # Count frequency bands
        frequency_dist = {band: 0 for band in FrequencyBand}
        for result in results:
            if 'frequency' in result:
                band = result['frequency'].get('band')
                if band:
                    frequency_dist[band] += 1

        # Count emotions
        emotion_counts = {emotion: 0 for emotion in EmotionType}
        for result in results:
            if 'emotion' in result:
                primary = result['emotion'].get('primary_emotion')
                if primary:
                    emotion_counts[primary] += 1

        # Count registers
        register_counts = {reg: 0 for reg in RegisterType}
        for result in results:
            if 'register' in result:
                reg = result['register'].get('register_type')
                if reg:
                    register_counts[reg] += 1

        return {
            'total_words': total_words,
            'frequency_distribution': dict(frequency_dist),
            'emotion_distribution': dict(emotion_counts),
            'register_distribution': dict(register_counts)
        }

    def get_frequency_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get frequency-related statistics."""
        ranks = []
        band_dist = {band: 0 for band in FrequencyBand}

        for result in results:
            if 'frequency' in result:
                rank = result['frequency'].get('rank')
                if rank and rank != float('inf'):
                    ranks.append(rank)
                band = result['frequency'].get('band')
                if band:
                    band_dist[band] += 1

        avg_rank = sum(ranks) / len(ranks) if ranks else 0

        return {
            'band_distribution': dict(band_dist),
            'average_rank': avg_rank,
            'total_ranks': len(ranks)
        }

    def get_emotion_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get emotion-related statistics."""
        emotion_counts = {emotion: 0 for emotion in EmotionType}
        confidences = []

        for result in results:
            if 'emotion' in result:
                primary = result['emotion'].get('primary_emotion')
                if primary:
                    emotion_counts[primary] += 1
                confidence = result['emotion'].get('confidence')
                if confidence:
                    confidences.append(confidence)

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            'emotion_distribution': dict(emotion_counts),
            'primary_emotion_counts': dict(emotion_counts),
            'average_confidence': avg_confidence
        }

    def get_register_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get register-related statistics."""
        register_counts = {reg: 0 for reg in RegisterType}
        confidences = []

        for result in results:
            if 'register' in result:
                reg = result['register'].get('register_type')
                if reg:
                    register_counts[reg] += 1
                confidence = result['register'].get('confidence')
                if confidence:
                    confidences.append(confidence)

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            'register_distribution': dict(register_counts),
            'confidence_distribution': {
                'average': avg_confidence,
                'min': min(confidences) if confidences else 0,
                'max': max(confidences) if confidences else 0
            }
        }

    def to_json(self, results: List[Dict[str, Any]], indent: int = 2) -> str:
        """
        Convert results to JSON format.

        Args:
            results: List of classification results
            indent: JSON indentation level

        Returns:
            JSON string
        """
        # Convert enums to values for JSON serialization
        serializable_results = []
        for result in results:
            serializable = {}
            for key, value in result.items():
                if isinstance(value, Enum):
                    serializable[key] = value.value
                elif isinstance(value, dict):
                    serializable[key] = {
                        k: v.value if isinstance(v, Enum) else v
                        for k, v in value.items()
                    }
                elif isinstance(value, list):
                    serializable[key] = [
                        v.value if isinstance(v, Enum) else v
                        for v in value
                    ]
                else:
                    serializable[key] = value
            serializable_results.append(serializable)

        return json.dumps(serializable_results, indent=indent)

    def to_csv(self, results: List[Dict[str, Any]]) -> str:
        """
        Convert results to CSV format.

        Args:
            results: List of classification results

        Returns:
            CSV string
        """
        output = StringIO()
        fieldnames = [
            'word', 'lemma', 'pos',
            'frequency_band', 'frequency_rank',
            'primary_emotion', 'emotion_confidence',
            'register_type', 'register_confidence', 'register_context'
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = {
                'word': result.get('word', ''),
                'lemma': result.get('lemma', ''),
                'pos': result.get('pos', ''),
                'frequency_band': (
                    result['frequency']['band'].value if 'frequency' in result else ''
                ),
                'frequency_rank': (
                    result['frequency'].get('rank', '') if 'frequency' in result else ''
                ),
                'primary_emotion': (
                    result['emotion']['primary_emotion'].value if 'emotion' in result and result['emotion']['primary_emotion'] else ''
                ),
                'emotion_confidence': (
                    result['emotion'].get('confidence', '') if 'emotion' in result else ''
                ),
                'register_type': (
                    result['register']['register_type'].value if 'register' in result else ''
                ),
                'register_confidence': (
                    result['register'].get('confidence', '') if 'register' in result else ''
                ),
                'register_context': (
                    result['register'].get('context', '') if 'register' in result else ''
                )
            }
            writer.writerow(row)

        return output.getvalue()

    def to_markdown(self, results: List[Dict[str, Any]]) -> str:
        """
        Convert results to Markdown report format.

        Args:
            results: List of classification results

        Returns:
            Markdown string
        """
        lines = [
            "# Word Classification Report",
            "",
            f"Total words: {len(results)}",
            "",
            "## Summary",
            ""
        ]

        # Add summary statistics
        summary = self.generate_summary_report(results)

        lines.append("### Frequency Distribution")
        for band, count in summary['frequency_distribution'].items():
            if count > 0:
                lines.append(f"- {band.label}: {count}")
        lines.append("")

        lines.append("### Emotion Distribution")
        for emotion, count in summary['emotion_distribution'].items():
            if count > 0:
                lines.append(f"- {emotion.label}: {count}")
        lines.append("")

        lines.append("### Register Distribution")
        for reg, count in summary['register_distribution'].items():
            if count > 0:
                lines.append(f"- {reg.label}: {count}")
        lines.append("")

        # Add detailed word table
        lines.append("## Word Details")
        lines.append("")
        lines.append("| Word | Lemma | POS | Frequency | Emotion | Register |")
        lines.append("|------|-------|-----|-----------|---------|----------|")

        for result in results[:50]:  # Limit to first 50 words
            word = result.get('word', '')
            lemma = result.get('lemma', '')
            pos = result.get('pos', '')

            freq_band = result['frequency']['band'].value if 'frequency' in result else 'N/A'
            emotion = (
                result['emotion']['primary_emotion'].value if 'emotion' in result and result['emotion']['primary_emotion'] else 'N/A'
            )
            register = (
                result['register']['register_type'].value if 'register' in result else 'N/A'
            )

            lines.append(f"| {word} | {lemma} | {pos} | {freq_band} | {emotion} | {register} |")

        return '\n'.join(lines)
