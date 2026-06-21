JAPANESE VOCABULARY TRAINER

A small command-line tool I built to help myself study Japanese vocabulary while learning the language.
Words have an adaptive level so I can tell which ones I actually know and which ones I keep failing.

FEATURES
- Browse the full vocabulary list
- Search a word by its Spanish meaning or by its romaji transcription
- Quiz mode: single random word, or a 10-word random choice session
- Adaptive level per word (+0.10 on a correct answer, -0.10 on a wrong one, clamped between 0.0 and 1.0)
- Vocabulary persists between sessions (saved to vocabData.json)

PROJECT STRUCTURE
main.py        -> entry point: loads the vocabulary and starts the app
interface.py   -> menu and user interaction loop
appLogic.py    -> search, quiz, and persistence logic
vocabData.json -> vocabulary data (created automatically on first run)

REQUIREMENTS
Python 3.x (no external dependencies yet)

RUNNING IT
python main.py

On first run, vocabData.json is created empty. Quiz mode requires at least 10 words in the 
vocabulary, so words need to be added before testing yourself (see Roadmap).