"""
Frequency Grader Module - Assigns frequency bands to words based on COCA data.
"""

from enum import Enum
from typing import Dict, Optional
from pathlib import Path


class FrequencyBand(Enum):
    """TOEFL frequency bands."""
    BAND_1 = "1"  # Very Common (top 1000-3000)
    BAND_2 = "2"  # Common (3000-5000)
    BAND_3 = "3"  # Moderate (5000-10000)
    BAND_4 = "4"  # Low (10000-20000)
    BAND_5 = "5"  # Rare (20000+)
    BEYOND = "beyond"  # Not in corpus


class FrequencyGrader:
    """
    Grades words by frequency using COCA corpus data.
    """

    def __init__(self, coca_file: Optional[Path] = None):
        """
        Initialize FrequencyGrader.

        Args:
            coca_file: Path to COCA frequency data file
        """
        self.coca_file = coca_file or Path(__file__).parent / "data" / "coca_frequency.txt"
        self.frequency_data = self._load_frequency_data()

    def _load_frequency_data(self) -> Dict[str, int]:
        """Load COCA frequency data from file."""
        freq_data = {}

        if not self.coca_file.exists():
            return freq_data

        try:
            with open(self.coca_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split()
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        rank = int(parts[1])
                        freq_data[word] = rank

        except Exception as e:
            print(f"Warning: Could not load frequency data: {e}")

        return freq_data

    def grade_word(self, word: str) -> dict:
        """
        Grade a single word by frequency.

        Args:
            word: Word to grade

        Returns:
            Dictionary with band and rank information
        """
        word_lower = word.lower()

        if word_lower in self.frequency_data:
            rank = self.frequency_data[word_lower]
            band = self._rank_to_band(rank)

            return {
                'band': band,
                'rank': rank,
                'source': 'COCA'
            }
        else:
            # Word not in corpus - assign BEYOND band
            return {
                'band': FrequencyBand.BEYOND,
                'rank': None,
                'source': 'Unknown'
            }

    def _rank_to_band(self, rank: int) -> FrequencyBand:
        """Convert COCA rank to frequency band."""
        if rank <= 3000:
            return FrequencyBand.BAND_1
        elif rank <= 5000:
            return FrequencyBand.BAND_2
        elif rank <= 10000:
            return FrequencyBand.BAND_3
        elif rank <= 20000:
            return FrequencyBand.BAND_4
        else:
            return FrequencyBand.BAND_5
