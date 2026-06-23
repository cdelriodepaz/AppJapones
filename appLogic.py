import random
import unicodedata
import json
from translate import Translator
import requests
import fugashi
import jaconv

currentVocab = {}
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
    wordList = list(currentVocab.keys())
    choice = random.randint(0, len(wordList) - 1)
    return wordList[choice]


def getTenRandomWords():
    return random.sample(list(currentVocab.keys()), 10)


def checkAnswer(theAnswer, theWord):
    correctAnswer = currentVocab.get(theWord).get("significado")
    if eliminar_tildes(theAnswer).lower() == eliminar_tildes(correctAnswer):
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
    with open(vocabFileName, "w") as writeFile:
        json.dump(dictionary, writeFile)


def loadVocab():
    try:
        with open(vocabFileName, "r") as loadFile:
            retValue = json.load(loadFile)
        return retValue
    except FileNotFoundError as e:
        saveVocab({})
        return {}


def updateWordField(key, field, newValue):
    if field not in allowedFieldModifications:
        return -1
    if key not in currentVocab:
        return -1
    currentVocab[key][field] = newValue
    saveVocab(currentVocab)


def initVocab():
    global currentVocab
    currentVocab = loadVocab()


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
