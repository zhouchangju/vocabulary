"""
Register Tagger Module - Classifies words by register (usage context).
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from pathlib import Path


class RegisterType(Enum):
    """Register categories (usage context)."""
    FORMAL = "formal"
    NEUTRAL = "neutral"
    INFORMAL = "informal"
    SLANG = "slang"


class RegisterTagger:
    """
    Tags words with register information based on usage context.
    Uses heuristic analysis and corpus data.
    """

    # Academic/Formal indicators (suffixes, roots, patterns)
    FORMAL_PATTERNS = {
        # Academic suffixes
        'tion', 'sion', 'ment', 'ence', 'ance', 'ity', 'ness', 'ism', 'ist',
        'ology', 'graphy', 'phy', 'mony', 'nomy', 'ture', 'ship', 'hood',
        # Latin/Greek roots
        'struct', 'script', 'spect', 'dict', 'cred', 'miss', 'mit', 'port',
        'pos', 'pon', 'stat', 'stit', 'scrib', 'tract', 'vert', 'vers',
        # Formal vocabulary
        'according', 'consequently', 'furthermore', 'nevertheless', 'therefore',
        'thus', 'hence', 'whereby', 'wherein', 'hereby', 'aforementioned',
        'notwithstanding', 'pertaining', 'regarding', 'concerning', 'respecting'
    }

    # Informal indicators
    INFORMAL_PATTERNS = {
        # Contractions/shortened forms
        'gonna', 'wanna', 'kinda', 'sorta', 'outta', 'gotta', 'hafta',
        # Casual words
        'stuff', 'things', 'okay', 'alright', 'maybe', 'kinda', 'sorta',
        'kids', 'folks', 'guys', 'bunch', 'lot', 'tons', 'loads'
    }

    # Slang indicators
    SLANG_PATTERNS = {
        # Very informal/slang
        'cool', 'awesome', 'dope', 'sick', 'lit', 'fire', ' vibes',
        'bro', 'dude', 'chill', 'hang', 'super', 'mega', 'ultra',
        'boo', 'bae', 'fam', 'squad', 'bestie', 'ghost', 'catfish'
    }

    # Domain-specific academic vocabulary
    ACADEMIC_DOMAINS = {
        'science': ['hypothesis', 'theory', 'experiment', 'analyze', 'data', 'conclusion'],
        'literature': ['metaphor', 'narrative', 'protagonist', 'allegory', 'genre'],
        'philosophy': ['ethics', 'paradigm', 'epistemology', 'ontology', 'dialectic'],
        'economics': ['inflation', 'recession', 'commodity', 'equilibrium', 'utility'],
        'law': ['precedent', 'statute', 'litigation', 'jurisdiction', 'plaintiff'],
        'medicine': ['symptom', 'diagnosis', 'pathology', 'treatment', 'prognosis']
    }

    def __init__(self, corpus_file: Optional[Path] = None):
        """
        Initialize RegisterTagger.

        Args:
            corpus_file: Path to corpus register data file
        """
        self.corpus_file = corpus_file or Path(__file__).parent / "data" / "toefl_corpus.txt"
        self.register_data = self._load_corpus_data()

    def _load_corpus_data(self) -> Dict[str, dict]:
        """Load corpus register data from file."""
        register_data = {}

        if not self.corpus_file.exists():
            return register_data

        try:
            with open(self.corpus_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split('\t')
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        register_info = parts[1]

                        register_data[word] = {
                            'register': register_info,
                            'source': 'Corpus'
                        }

        except Exception as e:
            print(f"Warning: Could not load register data: {e}")

        return register_data

    def tag_register(self, word: str, pos: Optional[str] = None) -> dict:
        """
        Tag a word with register information.

        Args:
            word: Word to tag
            pos: Part of speech (optional)

        Returns:
            Dictionary with register and confidence
        """
        word_lower = word.lower()

        # Check corpus data first
        if word_lower in self.register_data:
            corpus_reg = self.register_data[word_lower]['register']

            # Map corpus register to our types
            register_map = {
                'academic': RegisterType.FORMAL,
                'formal': RegisterType.FORMAL,
                'neutral': RegisterType.NEUTRAL,
                'informal': RegisterType.INFORMAL,
                'slang': RegisterType.SLANG
            }

            if corpus_reg in register_map:
                return {
                    'register': register_map[corpus_reg],
                    'confidence': 'high',
                    'source': 'Corpus'
                }

        # Fallback to heuristic analysis
        register, confidence = self._heuristic_tag(word_lower, pos)

        return {
            'register': register,
            'confidence': confidence,
            'source': 'Heuristic'
        }

    def _heuristic_tag(self, word: str, pos: Optional[str] = None) -> tuple:
        """
        Perform heuristic register tagging.

        Returns:
            Tuple of (RegisterType, confidence_level)
        """
        # Check for slang patterns
        for pattern in self.SLANG_PATTERNS:
            if pattern in word:
                return (RegisterType.SLANG, 'medium')

        # Check for informal patterns
        for pattern in self.INFORMAL_PATTERNS:
            if pattern in word:
                return (RegisterType.INFORMAL, 'medium')

        # Check for formal patterns
        for pattern in self.FORMAL_PATTERNS:
            if pattern in word:
                return (RegisterType.FORMAL, 'medium')

        # Check if word appears in academic domains
        for domain, domain_words in self.ACADEMIC_DOMAINS.items():
            if word in domain_words:
                return (RegisterType.FORMAL, 'high')

        # Check word length and structure (longer words tend to be more formal)
        if len(word) >= 8:
            return (RegisterType.FORMAL, 'low')

        # Default to neutral
        return (RegisterType.NEUTRAL, 'low')
