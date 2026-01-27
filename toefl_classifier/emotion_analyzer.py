"""
Emotion Analyzer Module - Analyzes emotional content of words using NRC lexicon.
"""

from enum import Enum
from typing import Dict, List, Optional
from pathlib import Path
import random


class EmotionType(Enum):
    """Emotion categories from NRC Emotion Lexicon."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class EmotionAnalyzer:
    """
    Analyzes emotional content of words using NRC Emotion Lexicon.
    Falls back to heuristic analysis if lexicon not available.
    """

    # Heuristic emotion patterns (suffixes, prefixes, roots)
    EMOTION_PATTERNS = {
        EmotionType.POSITIVE: [
            'happy', 'joy', 'good', 'great', 'love', 'wonder', 'excel', 'perfect',
            'beautiful', 'pleas', 'delight', 'satisfy', 'success', 'hope', 'peace',
            'friend', 'help', 'comfort', 'safe', 'calm', 'warm', 'light', 'bright',
            'free', 'true', 'wise', 'kind', 'gentle', 'happy', 'cheer'
        ],
        EmotionType.NEGATIVE: [
            'sad', 'bad', 'hate', 'terrible', 'awful', 'horror', 'fear', 'worst',
            'ugly', 'pain', 'suffer', 'fail', 'loss', 'death', 'war', 'crisis',
            'danger', 'threat', 'attack', 'harm', 'hurt', 'damage', 'wrong', 'evil',
            'dark', 'cold', 'hard', 'cruel', 'bitter', 'angry', 'sorry', 'worry'
        ],
        EmotionType.ANGER: [
            'angr', 'rage', 'furious', 'irate', 'mad', 'annoy', 'irritat', 'hostile',
            'aggress', 'violence', 'combat', 'conflict', 'fight'
        ],
        EmotionType.FEAR: [
            'fear', 'terrif', 'horror', 'scare', 'dread', 'anxi', 'panic', 'alarm',
            'nervous', 'worri', 'apprehens', 'timid'
        ],
        EmotionType.JOY: [
            'joy', 'delight', 'cheer', 'elate', 'exuber', 'jubil', 'ecstat', 'radiant',
            'enthuse', 'celebrat', 'rejoic'
        ],
        EmotionType.SADNESS: [
            'sad', 'sorrow', 'grief', 'mourn', 'depress', 'melanchol', 'despair',
            'regret', 'lament', 'misery'
        ],
        EmotionType.DISGUST: [
            'disgust', 'revolt', 'repuls', 'nausea', 'loath', 'detest', 'abhor'
        ],
        EmotionType.SURPRISE: [
            'surpris', 'amaz', 'astonish', 'shock', 'stun', 'astound', 'bewilder'
        ]
    }

    def __init__(self, nrc_file: Optional[Path] = None):
        """
        Initialize EmotionAnalyzer.

        Args:
            nrc_file: Path to NRC Emotion Lexicon file
        """
        self.nrc_file = nrc_file or Path(__file__).parent / "data" / "nrc_emotion_lexicon.txt"
        self.emotion_data = self._load_nrc_data()

    def _load_nrc_data(self) -> Dict[str, List[EmotionType]]:
        """Load NRC Emotion Lexicon from file."""
        emotion_data = {}

        if not self.nrc_file.exists():
            return emotion_data

        try:
            with open(self.nrc_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip() or line.startswith('#'):
                        continue

                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        word = parts[0].lower()
                        emotion = parts[1]
                        value = int(parts[2])

                        if value == 1:
                            if word not in emotion_data:
                                emotion_data[word] = []

                            # Map NRC emotions to our types
                            emotion_map = {
                                'joy': EmotionType.JOY,
                                'sadness': EmotionType.SADNESS,
                                'anger': EmotionType.ANGER,
                                'fear': EmotionType.FEAR,
                                'disgust': EmotionType.DISGUST,
                                'surprise': EmotionType.SURPRISE,
                                'positive': EmotionType.POSITIVE,
                                'negative': EmotionType.NEGATIVE
                            }

                            if emotion in emotion_map:
                                emotion_data[word].append(emotion_map[emotion])

        except Exception as e:
            print(f"Warning: Could not load emotion data: {e}")

        return emotion_data

    def analyze_emotion(self, word: str) -> dict:
        """
        Analyze emotional content of a word.

        Args:
            word: Word to analyze

        Returns:
            Dictionary with primary emotion and emotion list
        """
        word_lower = word.lower()

        if word_lower in self.emotion_data:
            emotions = self.emotion_data[word_lower]
            primary = self._determine_primary(emotions)

            return {
                'primary': primary,
                'emotions': emotions,
                'source': 'NRC'
            }
        else:
            # Fallback to heuristic analysis
            emotions = self._heuristic_analysis(word_lower)
            primary = self._determine_primary(emotions)

            return {
                'primary': primary,
                'emotions': emotions,
                'source': 'Heuristic'
            }

    def _heuristic_analysis(self, word: str) -> List[EmotionType]:
        """Perform heuristic emotion analysis based on word patterns."""
        detected = []

        for emotion, patterns in self.EMOTION_PATTERNS.items():
            for pattern in patterns:
                if pattern in word:
                    if emotion not in detected:
                        detected.append(emotion)
                    break

        # If no emotions detected, default to neutral (no specific emotion)
        if not detected:
            pass  # Return empty list for neutral

        return detected

    def _determine_primary(self, emotions: List[EmotionType]) -> str:
        """Determine primary emotion from list of emotions."""
        if not emotions:
            return 'neutral'

        # Priority: positive/negative first, then specific emotions
        priority_order = [
            EmotionType.POSITIVE,
            EmotionType.NEGATIVE,
            EmotionType.JOY,
            EmotionType.ANGER,
            EmotionType.FEAR,
            EmotionType.SADNESS,
            EmotionType.SURPRISE,
            EmotionType.DISGUST
        ]

        for emotion in priority_order:
            if emotion in emotions:
                return emotion.value

        # Fallback to first detected emotion
        return emotions[0].value if emotions else 'neutral'
