import random
import unicodedata
import json
from translate import Translator
import requests
import fugashi
import jaconv
from datetime import datetime

currentVocab = {}
lastEdit = ""
vocabFileName = "vocabData.json"
tagger = fugashi.Tagger()
esLan = "es"
jaLan = "ja"
enLan = "en"
provider = "mymemory"
espToJpTranslator = Translator(provider=provider, from_lang=esLan, to_lang=jaLan)
enToEspTranslator = Translator(provider=provider, from_lang=enLan, to_lang=esLan)
url = "https://jisho.org/api/v1/search/words"

## FILTRADO
allowedWordTypes = ["名詞", "動詞", "形容詞"]  ##[sustantivo, verbo, adjetivo]
allowedFieldModifications = ["kanji", "hiragana", "significado"]


def eliminar_tildes(texto):
    texto_normalizado = unicodedata.normalize("NFD", texto)
    solo_letras = [c for c in texto_normalizado if unicodedata.category(c) != "Mn"]
    return "".join(solo_letras)


## BUSQUEDA DE PALABRAS
def searchWordRomaji(theWord):
    return currentVocab.get(theWord, -1)


def searchWordSpanish(theWord):
    for word in currentVocab:
        sub_diccionario = currentVocab.get(word)
        if (
            sub_diccionario.get("significado")
            and sub_diccionario.get("significado").lower() == theWord
        ):
            return sub_diccionario
    return -1


def findKeyBySpanish(theWord):
    for word in currentVocab:
        sub_diccionario = currentVocab.get(word)
        if (
            sub_diccionario.get("significado")
            and sub_diccionario.get("significado").lower() == theWord
        ):
            return word
    return -1


def findVocabKey(theWord):
    retVal = findKeyBySpanish(theWord)
    if retVal == -1:
        retVal = searchWordRomaji(theWord)
        if retVal == -1:
            return retVal
        return theWord
    return retVal


## LÓGICA DEL QUIZ
def getRandomWord():
    wordList = []
    levelList = []
    for word in currentVocab:
        wordList.append(word)
        levelList.append(1 - currentVocab.get(word)["nivel"])

    selection = random.choices(wordList, weights=levelList, k=1)

    return selection[0]


def getTenRandomWords():
    wordList = []
    levelList = []
    for word in currentVocab:
        wordList.append(word)
        levelList.append(1 - currentVocab.get(word)["nivel"])

    counter = 0
    retList = []
    while counter != 10:
        selection = random.choices(wordList, weights=levelList, k=1)
        retList.append(selection[0])
        counter += 1
        wordList.remove(selection[0])
        levelList.remove(1 - currentVocab.get(selection[0])["nivel"])
    return retList


def checkAnswer(theAnswer, theWord):
    correctAnswer = currentVocab.get(theWord).get("significado")
    if eliminar_tildes(theAnswer).lower() == eliminar_tildes(correctAnswer).lower():
        return updateLevel(theWord, True)
    else:
        return updateLevel(theWord, False)


def updateLevel(theWord, booleanCorrect):
    data_word = currentVocab[theWord]
    if booleanCorrect == True:
        currentLevel = data_word["nivel"]
        data_word["nivel"] = min(1.0, data_word["nivel"] + 0.10)
        newLevel = data_word["nivel"]
        return f"Correcto!\nNivel: {currentLevel} --> {newLevel}"
    else:
        currentLevel = data_word["nivel"]
        data_word["nivel"] = max(0.00, data_word["nivel"] - 0.10)
        newLevel = data_word["nivel"]
        return f"Fallo!\nNivel: {currentLevel} --> {newLevel}"


## JSON y MANEJO DE VOCABULARIO
def saveVocab(dictionary):
    global lastEdit
    lastEdit = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(vocabFileName, "w") as writeFile:
        retDict = {}
        retDict["lastEdit"] = lastEdit
        retDict["words"] = dictionary

        json.dump(retDict, writeFile)


def loadVocab():
    try:
        with open(vocabFileName, "r") as loadFile:
            retValue = json.load(loadFile)
        vocab = retValue["words"]

        global lastEdit
        lastEdit = retValue["lastEdit"]
        return vocab
    except (FileNotFoundError, json.JSONDecodeError) as e:
        saveVocab({})
        return {}


def initVocab():
    global currentVocab
    currentVocab = loadVocab()


def updateWordField(key, field, newValue):
    if field not in allowedFieldModifications:
        return -1
    if key not in currentVocab:
        return -1
    currentVocab[key][field] = newValue
    saveVocab(currentVocab)


def deleteWord(theKey):
    if theKey not in currentVocab:
        return -1
    del currentVocab[theKey]
    saveVocab(currentVocab)


## TRADUCCIÓN
def translateSentence(toTranslate, theTranslator):
    translatedRes = theTranslator.translate(toTranslate.lower())
    return translatedRes


def getMeaning(theWord):
    answer = requests.get(url, params={"keyword": theWord})
    alldata = answer.json()["data"]
    if len(alldata) == 0:
        return -1

    firstValidResult = alldata[0]
    return firstValidResult["senses"][0].get("english_definitions")[0]


def extractCandidates(spanishSentence):
    retList = []
    japaneseSentence = translateSentence(spanishSentence, espToJpTranslator)
    tokenList = tagger(japaneseSentence)
    for token in tokenList:
        wordType = token.feature.pos1
        if wordType in allowedWordTypes:
            wordMeaning = getMeaning(token.feature.lemma)
            if wordMeaning == -1:
                print(
                    f"-- No se pudo encontrar un significado válido para {token.feature.lemma} -> Palabra omitida"
                )
                continue
            else:
                hiragana = jaconv.kata2hira(token.feature.kana)
                retList.append(  ##[romaji, palabra inf, kana, significado]
                    [
                        jaconv.kana2alphabet(hiragana),
                        token.feature.lemma,
                        hiragana,
                        translateSentence(wordMeaning, enToEspTranslator),
                    ]
                )
    return retList
