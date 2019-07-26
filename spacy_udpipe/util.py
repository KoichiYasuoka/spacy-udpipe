# coding: utf8
import os
import urllib.request
from pathlib import Path

from spacy.language import Language
from spacy.util import get_lang_class

BASE_URL = "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2998/"
LANGUAGES = {
    "af": "afrikaans-afribooms-ud-2.4-190531.udpipe",
    "hy": "armenian-armtdp-ud-2.4-190531.udpipe",
    "eu": "basque-bdt-ud-2.4-190531.udpipe",
    "be": "belarusian-hse-ud-2.4-190531.udpipe",
    # "xx": "ancient_greek-perseus-ud-2.4-190531.udpipe",
    # "xx": "ancient_greek-proiel-ud-2.4-190531.udpipe",
    "ca": "catalan-ancora-ud-2.4-190531.udpipe",
    "zh": "chinese-gsd-ud-2.4-190531.udpipe",
    # "xx": "classical_chinese-kyoto-ud-2.4-190531.udpipe",
    "ar": "arabic-padt-ud-2.4-190531.udpipe",
    "bg": "bulgarian-btb-ud-2.4-190531.udpipe",
    # "cs": "czech-cac-ud-2.4-190531.udpipe",
    "cs": "czech-cltt-ud-2.4-190531.udpipe",
    # "cs": "czech-pdt-ud-2.4-190531.udpipe",
    # "cs": "czech-fictree-ud-2.4-190531.udpipe",
    "hr": "croatian-set-ud-2.4-190531.udpipe",
    # "xx": "coptic-scriptorium-ud-2.4-190531.udpipe",
    "nl": "dutch-lassysmall-ud-2.4-190531.udpipe",
    # "nl": "dutch-alpino-ud-2.4-190531.udpipe",
    "da": "danish-ddt-ud-2.4-190531.udpipe",
    "et": "estonian-edt-ud-2.4-190531.udpipe",
    # "et": "estonian-ewt-ud-2.4-190531.udpipe",
    "en": "english-partut-ud-2.4-190531.udpipe",
    # "en": "english-gum-ud-2.4-190531.udpipe",
    # "en": "english-ewt-ud-2.4-190531.udpipe",
    # "en": "english-lines-ud-2.4-190531.udpipe",
    "fr": "french-partut-ud-2.4-190531.udpipe",
    # "fr": "french-gsd-ud-2.4-190531.udpipe",
    # "fr": "french-spoken-ud-2.4-190531.udpipe",
    # "fr": "french-sequoia-ud-2.4-190531.udpipe",
    # "xx": "old_french-srcmf-ud-2.4-190531.udpipe",
    "fi": "finnish-ftb-ud-2.4-190531.udpipe",
    # "fi": "finnish-tdt-ud-2.4-190531.udpipe",
    "de": "german-gsd-ud-2.4-190531.udpipe",
    "gl": "galician-treegal-ud-2.4-190531.udpipe",
    # "gl": "galician-ctg-ud-2.4-190531.udpipe",
    "el": "greek-gdt-ud-2.4-190531.udpipe",
    # "xx": "gothic-proiel-ud-2.4-190531.udpipe",
    "hu": "hungarian-szeged-ud-2.4-190531.udpipe",
    "hi": "hindi-hdtb-ud-2.4-190531.udpipe",
    "he": "hebrew-htb-ud-2.4-190531.udpipe",
    "it": "italian-partut-ud-2.4-190531.udpipe",
    # "it": "italian-postwita-ud-2.4-190531.udpipe",
    # "it": "italian-isdt-ud-2.4-190531.udpipe",
    # "it": "italian-vit-ud-2.4-190531.udpipe",
    "ga": "irish-idt-ud-2.4-190531.udpipe",
    "id": "indonesian-gsd-ud-2.4-190531.udpipe",
    "la": "latin-perseus-ud-2.4-190531.udpipe",
    # "la": "latin-proiel-ud-2.4-190531.udpipe",
    # "la": "latin-ittb-ud-2.4-190531.udpipe",
    "ko": "korean-gsd-ud-2.4-190531.udpipe",
    # "ko": "korean-kaist-ud-2.4-190531.udpipe",
    "ja": "japanese-gsd-ud-2.4-190531.udpipe",
    "lt": "lithuanian-hse-ud-2.4-190531.udpipe",
    # "lt": "lithuanian-alksnis-ud-2.4-190531.udpipe",
    "lv": "latvian-lvtb-ud-2.4-190531.udpipe",
    "nn": "norwegian-nynorsk-ud-2.4-190531.udpipe",
    # "nn": "norwegian-nynorsklia-ud-2.4-190531.udpipe",
    "nb": "norwegian-bokmaal-ud-2.4-190531.udpipe",
    "se": "north_sami-giella-ud-2.4-190531.udpipe",
    "mr": "marathi-ufal-ud-2.4-190531.udpipe",
    "mt": "maltese-mudt-ud-2.4-190531.udpipe",
    # "xx": "persian-seraji-ud-2.4-190531.udpipe",
    "cu": "old_church_slavonic-proiel-ud-2.4-190531.udpipe",
    "ro": "romanian-rrt-ud-2.4-190531.udpipe",
    # "ro": "romanian-nonstandard-ud-2.4-190531.udpipe",
    "pt": "portuguese-gsd-ud-2.4-190531.udpipe",
    # "pt": "portuguese-bosque-ud-2.4-190531.udpipe",
    "pl": "polish-pdb-ud-2.4-190531.udpipe",
    # "pl": "polish-lfg-ud-2.4-190531.udpipe",
    "sr": "serbian-set-ud-2.4-190531.udpipe",
    "ru": "russian-gsd-ud-2.4-190531.udpipe",
    # "ru": "russian-syntagrus-ud-2.4-190531.udpipe",
    # "ru": "russian-taiga-ud-2.4-190531.udpipe",
    # "xx": "old_russian-torot-ud-2.4-190531.udpipe",
    "es": "spanish-gsd-ud-2.4-190531.udpipe",
    # "es": "spanish-ancora-ud-2.4-190531.udpipe",
    "sl": "slovenian-ssj-ud-2.4-190531.udpipe",
    # "sl": "slovenian-sst-ud-2.4-190531.udpipe",
    "sk": "slovak-snk-ud-2.4-190531.udpipe",
    "uk": "ukrainian-iu-ud-2.4-190531.udpipe",
    "tr": "turkish-imst-ud-2.4-190531.udpipe",
    "te": "telugu-mtg-ud-2.4-190531.udpipe",
    "ta": "tamil-ttb-ud-2.4-190531.udpipe",
    "sv": "swedish-talbanken-ud-2.4-190531.udpipe",
    # "sv": "swedish-lines-ud-2.4-190531.udpipe",
    "wo": "wolof-wtb-ud-2.4-190531.udpipe",
    "vi": "vietnamese-vtb-ud-2.4-190531.udpipe",
    "ug": "uyghur-udt-ud-2.4-190531.udpipe",
    "ur": "urdu-udtb-ud-2.4-190531.udpipe"
}
MODELS_DIR = Path(__file__).parent / "models"


def _check_language(lang):
    if not lang in LANGUAGES:
        raise Exception("'%s' language not available" % lang)


def _check_models_dir(lang):
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)


def download(lang):
    """Download the UDPipe pretrained model.

    lang (unicode): The language code.
    """
    _check_language(lang)
    _check_models_dir(lang)
    url = BASE_URL + LANGUAGES[lang]
    fname = os.path.join(MODELS_DIR, LANGUAGES[lang])
    urllib.request.urlretrieve(url=url, filename=fname)


def get_path(lang):
    """Get the path to the UDPipe pretrained model if it was downloaded.

    lang (unicode): The language code.
    RETURNS (unicode): The path to the UDPipe pretrained model.
    """
    _check_language(lang)
    _check_models_dir(lang)
    if not LANGUAGES[lang] in os.listdir(MODELS_DIR):
        raise Exception(("Use spacy_udpipe.download to download "
                         "the pretrained UDPipe model for the '%s' language"
                         % lang))
    path = os.path.join(MODELS_DIR, LANGUAGES[lang])
    return path


def get_defaults(lang):
    """Get the language-specific defaults, if available in spaCy. This allows
    using lexical attribute getters that depend on static language data, e.g.
    Token.like_num, Token.is_stop, Doc.noun_chunks etc.

    lang (unicode): The language code.
    RETURNS (Language.Defaults): The language defaults.
    """
    try:
        lang_cls = get_lang_class(lang)
        return lang_cls.Defaults
    except ImportError:
        return Language.Defaults
