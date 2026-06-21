import random
import unicodedata
import json

currentVocab = {}
vocabFileName = "vocabData.json"


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


## JSON


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


## VOCAB MANAGEMENT


def initVocab():
    global currentVocab
    currentVocab = loadVocab()
