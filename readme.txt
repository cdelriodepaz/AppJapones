JAPANESE VOCABULARY TRAINER

A small command-line tool I built to help myself study Japanese vocabulary while learning the language.
It now includes a full pipeline that turns a Spanish sentence into vocabulary candidates, plus an adaptive
quiz mode so I can tell which words I actually know.

FEATURES
- Browse the full vocabulary list
- Search a word by its Spanish meaning or by its romaji
- Quiz mode: single random word, or a 10-word session
- Sentence-to-vocabulary pipeline: write a sentence in Spanish, get it translated to Japanese, tokenized and
    tagged (nouns/verbs only), looked up in a Japanese-English dictionary, and the meaning translated back
    to Spanish, then choose which words to add to your vocabulary
- Vocabulary persists between sessions (saved to vocabData.json)

PROJECT STRUCTURE
main.py        -> entry point: loads the vocabulary and starts the app
interface.py   -> menu and user interaction loop
appLogic.py    -> search, quiz, translation/tokenization pipeline, and persistence logic
vocabData.json -> vocabulary data (created automatically on first run)

REQUIREMENTS
Python 3.x
See requirements.txt (translate, requests, fugashi, unidic-lite, jaconv)

RUNNING IT
pip install -r requirements.txt
python main.py

On first run, vocabData.json is created empty. Quiz mode requires at least 10 words in the vocabulary, use
the sentence pipeline (option D) to build it up first.

HOW THE PIPELINE WORKS
1. Spanish sentence -> translated to Japanese (MyMemory, via the translate package)
2. Japanese sentence -> tokenized and POS-tagged (fugashi)
3. Tokens filtered down to nouns and verbs
4. Each word looked up in Jisho for its English meaning
5. Meaning translated back to Spanish
6. Reading converted from katakana to hiragana and to romaji (jaconv)
7. Candidates shown to the user, who chooses which ones to save

No part of this pipeline requires an API key or any account setup, by design.