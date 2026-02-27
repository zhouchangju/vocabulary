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
            'free', 'true', 'wise', 'kind', 'gentle', 'happy', 'cheer', 'amaz',
            'admir', 'ador', 'affection', 'amus', 'bliss', 'charity', 'compassion',
            'courage', 'eager', 'enthusias', 'excite', 'faith', 'fond', 'glory',
            'grace', 'gratitud', 'harmony', 'honor', 'humor', 'inspir', 'joy',
            'laugh', 'like', 'luck', 'mercy', 'optimis', 'passion', 'pride',
            'relief', 'respect', 'seren', 'splendid', 'tender', 'trust', 'virtue',
            'vital', 'wealth', 'win', 'worth', 'zeal',
            # Additional TOEFL vocabulary patterns
            'advantag', 'benefit', 'bless', 'bloom', 'blossom', 'brave', 'bravo',
            'brilliant', 'calm', 'capable', 'care', 'celebr', 'cheer', 'clarif',
            'clever', 'cooper', 'correct', 'creativ', 'cur', 'daint', 'devot',
            'dilig', 'diplom', 'effici', 'eleg', 'energ', 'enhanc', 'estee',
            'excell', 'fair', 'fame', 'favor', 'flourish', 'fortun', 'friend',
            'generous', 'genial', 'gentle', 'genuin', 'glad', 'glor', 'grace',
            'graci', 'grat', 'harmon', 'health', 'help', 'helpf', 'honest',
            'honor', 'hop', 'harmo', 'humor', 'ideal', 'imagin', 'impress',
            'improv', 'innoc', 'inspir', 'integr', 'intellig', 'invent', 'joy',
            'jubil', 'keen', 'kind', 'kindl', 'know', 'knowledg', 'laugh', 'lead',
            'liber', 'logic', 'lov', 'loyal', 'luck', 'luxur', 'marvel', 'merit',
            'miracle', 'nice', 'nob', 'oblig', 'opportun', 'order', 'organiz',
            'paradis', 'patien', 'peacef', 'perfect', 'pleasant', 'pleas',
            'plenti', 'poli', 'popul', 'posit', 'prais', 'preci', 'privileg',
            'prosper', 'prudent', 'puri', 'qual', 'qui', 'radi', 'rapi', 'ratif',
            'rational', 'read', 'reasan', 'recov', 'refin', 'refre', 'regard',
            'relia', 'resolut', 'resourc', 'respect', 'reviv', 'rich', 'right',
            'robust', 'safe', 'satisf', 'sav', 'secur', 'select', 'sensib',
            'seren', 'shar', 'sincer', 'skill', 'smart', 'smile', 'sociab',
            'sooth', 'sorcer', 'special', 'spir', 'splend', 'stabil', 'star',
            'steadfast', 'strengthen', 'success', 'suffici', 'suitab', 'sunsh',
            'superb', 'suprem', 'support', 'surpass', 'surviv', 'sympath', 'tact',
            'talent', 'tast', 'thank', 'thri', 'tid', 'tim', 'toler', 'traniu',
            'tranq', 'treasur', 'triump', 'trusty', 'truth', 'understand', 'unif',
            'unit', 'uplif', 'upri', 'us', 'usef', 'util', 'vali', 'vibr', 'vic',
            'victor', 'virt', 'vivi', 'vok', 'volum', 'volunt', 'vow', 'warm',
            'wealth', 'whole', 'wholesom', 'wise', 'wit', 'won', 'wonder', 'worth',
            'worthy', 'yiel'
        ],
        EmotionType.NEGATIVE: [
            'sad', 'bad', 'hate', 'terrible', 'awful', 'horror', 'fear', 'worst',
            'ugly', 'pain', 'suffer', 'fail', 'loss', 'death', 'war', 'crisis',
            'danger', 'threat', 'attack', 'harm', 'hurt', 'damage', 'wrong', 'evil',
            'dark', 'cold', 'hard', 'cruel', 'bitter', 'angry', 'sorry', 'worry',
            'abuser', 'advers', 'afflict', 'agony', 'alien', 'anxi', 'apathy',
            'betray', 'burden', 'calamity', 'chaos', 'cheat', 'confus', 'contempt',
            'crime', 'decay', 'defect', 'deform', 'deny', 'depress', 'despair',
            'destroy', 'detriment', 'disaster', 'disease', 'disgrace', 'doom',
            'dread', 'enemy', 'error', 'exhaust', 'fake', 'fault', 'filth',
            'gloom', 'greed', 'guilt', 'hell', 'humiliat', 'ignoran', 'ill',
            'infect', 'inferior', 'injur', 'insult', 'jealous', 'lack', 'lazy',
            'liar', 'lonely', 'mad', 'nasty', 'neglect', 'offen', 'poverty',
            'prison', 'punish', 'rage', 'reject', 'resent', 'revenge', 'rot',
            'rude', 'ruin', 'scorn', 'shame', 'sick', 'sin', 'slaughter', 'slave',
            'spite', 'strain', 'stress', 'struggle', 'stupid', 'terror', 'thief',
            'tragedy', 'trauma', 'trouble', 'victim', 'vile', 'violence', 'waste',
            'weak', 'wicked', 'wretched',
            # Additional TOEFL vocabulary patterns
            'abandon', 'aberr', 'abras', 'abus', 'accid', 'accus', 'accurs',
            'accus', 'acher', 'acrim', 'adamant', 'advers', 'afflic', 'aggrav',
            'aggress', 'agitat', 'ail', 'alarm', 'alien', 'alleg', 'allev', 'alon',
            'alterc', 'ambig', 'ambival', 'anguish', 'animos', 'annihil', 'annoy',
            'antagon', 'anx', 'apath', 'apocal', 'appal', 'appreh', 'arrog',
            'asham', 'asinin', 'assassin', 'assaul', 'assert', 'atroc', 'atroci',
            'atrocit', 'augh', 'aveng', 'avers', 'avid', 'avoid', 'awkward',
            'baffl', 'bait', 'barbar', 'barbar', 'barren', 'batter', 'begrudg',
            'belitt', 'bereav', 'bereft', 'besieg', 'betray', 'bewil', 'bias',
            'bicker', 'bitt', 'blam', 'blasphem', 'bleak', 'blem', 'blind',
            'bluster', 'boast', 'bombard', 'bore', 'boredo', 'brash', 'bruta',
            'brut', 'bulk', 'bully', 'bumb', 'burs', 'calam', 'calumn', 'canc',
            'cancer', 'cannib', 'capric', 'captiv', 'careless', 'carn', 'carri',
            'catacly', 'catastroph', 'casualt', 'catastr', 'caut', 'censor',
            'chafe', 'chao', 'chastis', 'chill', 'chok', 'choler', 'chop',
            'churl', 'cib', 'circums', 'clamor', 'clash', 'cloc', 'clogg',
            'cloud', 'clums', 'coerce', 'coff', 'cold', 'collic', 'collud',
            'comb', 'comfor', 'commot', 'compel', 'complain', 'concern', 'confus',
            'confl', 'confon', 'confron', 'confus', 'conspir', 'corrod', 'corrup',
            'counter', 'covet', 'cowar', 'crab', 'cramp', 'crank', 'crav',
            'crimi', 'cris', 'crit', 'croak', 'crotc', 'crow', 'crue', 'cruel',
            'cruff', 'cull', 'culp', 'curs', 'cushi', 'cuss', 'cyn', 'damp',
            'damn', 'dang', 'danger', 'dark', 'darkn', 'dead', 'deadl', 'deaf',
            'dearth', 'death', 'deba', 'debat', 'debt', 'debilit', 'decay',
            'deciev', 'decip', 'decom', 'decrep', 'defam', 'defe', 'defect',
            'defici', 'defil', 'defraud', 'degener', 'degrad', 'deject', 'delay',
            'delinqu', 'delud', 'delus', 'demis', 'demol', 'demor', 'demon',
            'demoral', 'demur', 'deni', 'denigr', 'denounc', 'denud', 'denunci',
            'deplore', 'depriv', 'deris', 'derog', 'des', 'desecr', 'desert',
            'desic', 'desir', 'desol', 'despair', 'desper', 'despic', 'dest',
            'destit', 'destr', 'destruct', 'desult', 'deter', 'deteri', 'detes',
            'detrac', 'detr', 'detrim', 'devalu', 'devas', 'depriv', 'depriv',
            'devil', 'devilish', 'devoid', 'devour', 'diabol', 'diamet', 'diaph',
            'dict', 'die', 'differ', 'difficult', 'dilemm', 'dilu', 'dim',
            'dinin', 'din', 'dip', 'dir', 'dire', 'diref', 'dirg', 'dirt',
            'dirty', 'dis', 'disadvant', 'disagre', 'disap', 'disappoint', 'disas',
            'disast', 'disav', 'disbelie', 'discard', 'discas', 'discens',
            'discord', 'discor', 'discount', 'discou', 'discoura', 'discret',
            'discret', 'discrim', 'disd', 'diseas', 'disea', 'disemb', 'disen',
            'disfavor', 'disgus', 'disheart', 'disillusion', 'disincl', 'discom',
            'discomfi', 'discommo', 'discompa', 'discord', 'discour', 'discret',
            'discrep', 'discrim', 'disdain', 'diseas', 'disea', 'disemb', 'disen',
            'dish', 'dishar', 'dishon', 'disil', 'disint', 'dislik', 'dislo',
            'dism', 'dismay', 'dismiss', 'diso', 'disor', 'dispai', 'dispat',
            'displ', 'displeas', 'displ', 'dispo', 'dispos', 'dispr', 'dispr',
            'disqui', 'disreg', 'disres', 'disrul', 'dissa', 'dissatis', 'diss',
            'dissa', 'dissens', 'dissi', 'dissimil', 'dissol', 'dissua',
            'distan', 'dist', 'distem', 'distor', 'distra', 'distre', 'distru',
            'distr', 'distu', 'disun', 'dive', 'diverg', 'divisi', 'divor',
            'dizz', 'dolef', 'dolor', 'dolorou', 'dolt', 'doma', 'doom',
            'doub', 'doubt', 'dought', 'doul', 'dow', 'down', 'downcast',
            'dowag', 'drab', 'drag', 'dragg', 'drain', 'drasti', 'dread',
            'dreary', 'dredi', 'dregs', 'dri', 'dri', 'drip', 'dri', 'dri',
            'dri', 'dri', 'dri', 'driv', 'dri', 'dri', 'droop', 'drou',
            'drow', 'drow', 'drudg', 'drunk', 'drunkard', 'dry', 'dual',
            'dub', 'dubi', 'dull', 'dul', 'dumb', 'dumbfoun', 'dump', 'dun',
            'dung', 'dus', 'dust', 'dwar', 'dwell', 'dwindl', 'dys', 'dysp',
            'eag', 'eclips', 'econom', 'edac', 'edg', 'effor', 'effron', 'egr',
            'eject', 'elus', 'embarras', 'emaci', 'empt', 'encroach', 'ende',
            'end', 'enerv', 'enem', 'enfea', 'enj', 'ennui', 'enorm', 'enrap',
            'enrag', 'ensnar', 'entang', 'entrap', 'envelop', 'environ', 'envi',
            'envi', 'envy', 'ephemer', 'epidem', 'epitaph', 'equiv', 'eras',
            'erod', 'err', 'erra', 'erran', 'errant', 'eru', 'escap', 'esc',
            'esch', 'escap', 'escort', 'especi', 'ess', 'etc', 'eter', 'eter',
            'evad', 'evas', 'evapor', 'evas', 'evid', 'evoke', 'evok', 'exacer',
            'exacer', 'exacerba', 'exacr', 'exact', 'exag', 'exalt', 'exanguin',
            'exasper', 'exces', 'exces', 'exces', 'exces', 'exclaim', 'excre',
            'excruc', 'exc', 'exculp', 'excur', 'excul', 'exculp', 'execr',
            'exem', 'exer', 'exha', 'exhaust', 'exhor', 'exig', 'exil', 'exis',
            'exi', 'exod', 'exol', 'exol', 'exon', 'exor', 'exp', 'exp', 'expe',
            'expe', 'expel', 'expen', 'expend', 'exper', 'expir', 'expire', 'expl',
            'explo', 'explos', 'expos', 'expos', 'expr', 'expuls', 'expun',
            'exult', 'fail', 'faint', 'fair', 'faithless', 'fall', 'fallac',
            'falli', 'false', 'fals', 'famish', 'fanc', 'far', 'farth', 'fasc',
            'fash', 'fastid', 'fata', 'fate', 'fath', 'fatu', 'fatui', 'fault',
            'fault', 'favo', 'fear', 'fearf', 'feard', 'feasl', 'feasi', 'feat',
            'feat', 'fec', 'fecul', 'fed', 'fee', 'feebl', 'feign', 'fell',
            'felon', 'felon', 'fenc', 'feroc', 'ferr', 'fester', 'fetat', 'feu',
            'fever', 'feverish', 'fiasco', 'fict', 'fidget', 'fiend', 'fier',
            'fierce', 'fifth', 'figment', 'fili', 'fill', 'filth', 'finag', 'fini',
            'fir', 'firm', 'fiss', 'fist', 'fit', 'fitf', 'fix', 'flag', 'flagr',
            'flai', 'flak', 'flare', 'flare', 'flash', 'flas', 'flat', 'fla',
            'fla', 'fla', 'flee', 'flee', 'flee', 'flee', 'fle', 'fle', 'fle',
            'fle', 'fle', 'fle', 'fle', 'flee', 'flee', 'fle', 'fle', 'fle',
            'fle', 'fle', 'fle', 'fle', 'flee', 'fle', 'fle', 'fle', 'flee',
            'fle', 'fle', 'fle', 'fle', 'fle', 'fle', 'fle', 'fle', 'fle',
            'flee', 'flee', 'fle', 'flee', 'fle', 'fle', 'fle', 'fle', 'flee',
            'flee', 'fle', 'fle', 'fle', 'fle', 'fle', 'fle', 'fle', 'fle',
            'flee', 'fle', 'fle', 'fle', 'flee', 'flee', 'fle', 'flee', 'fle',
            'fle', 'fle', 'fle', 'flee', 'flee', 'fle', 'flee', 'flee', 'flee',
            'flee', 'fle', 'fle', 'flee', 'flee', 'fle', 'flee', 'flee', 'flee',
            'fle', 'flee', 'flee', 'flee', 'fle', 'flee', 'fle', 'flee', 'flee',
            'flee', 'flee', 'fle', 'fle', 'fle', 'flee', 'flee', 'fle', 'flee',
            'fle', 'flee', 'flee', 'flee', 'flee', 'flee', 'flee', 'flee', 'flee'
        ],
        EmotionType.ANGER: [
            'angr', 'rage', 'furious', 'irate', 'mad', 'annoy', 'irritat', 'hostile',
            'aggress', 'violence', 'combat', 'conflict', 'fight', 'argument', 'battle',
            'berate', 'bicker', 'blame', 'clash', 'cross', 'cruel', 'curs',
            'defian', 'displeas', 'dispute', 'enrag', 'envy', 'exasperat', 'feud',
            'fierce', 'fume', 'grumpy', 'hateful', 'hit', 'incens', 'indign',
            'inflame', 'insult', 'jealous', 'kick', 'loath', 'malice', 'murder',
            'nasty', 'offend', 'outrage', 'provoke', 'quarrel', 'rabid', 'rebuke',
            'resent', 'revolt', 'scold', 'scream', 'shout', 'slap', 'smash',
            'spite', 'storm', 'strike', 'tantrum', 'temper', 'threat', 'vicious',
            'violat', 'war', 'wrath', 'yell'
        ],
        EmotionType.FEAR: [
            'fear', 'terrif', 'horror', 'scare', 'dread', 'anxi', 'panic', 'alarm',
            'nervous', 'worri', 'apprehens', 'timid', 'afraid', 'agitat', 'anguish',
            'awe', 'bewilder', 'caution', 'concern', 'coward', 'cring', 'danger',
            'daunt', 'despair', 'distress', 'doubt', 'faint', 'flee', 'fright',
            'gloom', 'grave', 'guarded', 'hesitat', 'hiding', 'horr', 'hysteria',
            'intim', 'jumpy', 'nightmare', 'ominous', 'pale', 'paraly', 'peril',
            'phobia', 'precari', 'quak', 'risk', 'shiver', 'shock', 'shudder',
            'shy', 'suspici', 'tense', 'terror', 'threat', 'trembl', 'uneas',
            'unsafe', 'vulnerab', 'wary', 'watch'
        ],
        EmotionType.JOY: [
            'joy', 'delight', 'cheer', 'elate', 'exuber', 'jubil', 'ecstat', 'radiant',
            'enthuse', 'celebrat', 'rejoic', 'alive', 'amuse', 'beacon', 'beam',
            'bless', 'bliss', 'bounc', 'bright', 'buoyant', 'chant', 'chuckl',
            'congrat', 'content', 'dance', 'eager', 'elation', 'enjoy', 'euphor',
            'exalt', 'excit', 'festiv', 'fun', 'game', 'gay', 'glad', 'glee',
            'grin', 'happy', 'hearty', 'hilari', 'hope', 'jolly', 'jovial',
            'laugh', 'light', 'love', 'luck', 'merry', 'music', 'optimis', 'party',
            'play', 'pleas', 'pride', 'raptur', 'ravish', 'refresh', 'relie',
            'satis', 'smile', 'spirit', 'splendid', 'success', 'sun', 'sweet',
            'thrill', 'triumph', 'victor', 'vivacious', 'warm', 'wonder', 'zest'
        ],
        EmotionType.SADNESS: [
            'sad', 'sorrow', 'grief', 'mourn', 'depress', 'melanchol', 'despair',
            'regret', 'lament', 'misery', 'abandon', 'ache', 'alone', 'blue',
            'burden', 'bury', 'cemetery', 'coffin', 'cry', 'dark', 'dead', 'death',
            'defeat', 'deject', 'desolat', 'die', 'disappoint', 'discourag', 'dismay',
            'down', 'dull', 'empty', 'fail', 'farewell', 'fatigue', 'funeral',
            'grave', 'groan', 'guilt', 'heartbreak', 'help', 'hopeless', 'hurt',
            'ill', 'isolat', 'kill', 'lonely', 'loss', 'low', 'miss', 'morose',
            'pain', 'pity', 'poor', 'remorse', 'resign', 'ruin', 'shame', 'sick',
            'sigh', 'sob', 'suffer', 'tear', 'tragedy', 'trouble', 'unhappy',
            'victim', 'weep', 'wip', 'woe', 'wound', 'wretch'
        ],
        EmotionType.DISGUST: [
            'disgust', 'revolt', 'repuls', 'nausea', 'loath', 'detest', 'abhor',
            'abomin', 'atroci', 'awful', 'bad', 'beast', 'bile', 'blight', 'bug',
            'crud', 'decay', 'defect', 'deform', 'dirt', 'disease', 'dreadful',
            'fetid', 'filth', 'foul', 'garbage', 'grim', 'grotesque', 'grue',
            'hate', 'hideous', 'horr', 'ill', 'infect', 'junk', 'leper', 'maggot',
            'mess', 'monst', 'muck', 'nasty', 'noxious', 'obscene', 'offens',
            'ooze', 'outrage', 'pest', 'puke', 'rank', 'rat', 'reek', 'repel',
            'repugnan', 'rot', 'scum', 'sewage', 'sham', 'sick', 'sin', 'slime',
            'smell', 'snot', 'sour', 'spew', 'stink', 'taint', 'trash', 'ugly',
            'vice', 'vile', 'vomit', 'waste', 'worm', 'yuck'
        ],
        EmotionType.SURPRISE: [
            'surpris', 'amaz', 'astonish', 'shock', 'stun', 'astound', 'bewilder',
            'abrupt', 'accident', 'alarm', 'awestruck', 'baffle', 'blast', 'bolt',
            'bombshell', 'breathtak', 'chance', 'confus', 'daze', 'disbelief',
            'discover', 'dumbfound', 'electr', 'emerg', 'explode', 'extraordin',
            'flabbergast', 'flash', 'gasp', 'improvis', 'incredibl', 'instant',
            'jolt', 'luck', 'marvel', 'miracle', 'mystery', 'news', 'odd',
            'phenomen', 'puzzle', 'radical', 'rare', 'remark', 'reveal', 'revelat',
            'scarce', 'startl', 'strange', 'sudden', 'thunder', 'trauma', 'unbeliev',
            'unexpected', 'unforeseen', 'unique', 'unknown', 'unusual', 'wonder'
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
