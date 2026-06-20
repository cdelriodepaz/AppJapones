import dataDict


def searchWordRomaji(theWord):
    for word in dataDict.VOCAB_WORDS:
        if word == theWord:
            return dataDict.VOCAB_WORDS.get(word)
    return -1


def searchWordSpanish(theWord):
    for word in dataDict.VOCAB_WORDS:
        sub_diccionario = dataDict.VOCAB_WORDS.get(word)
        if (
            sub_diccionario.get("significado")
            and sub_diccionario.get("significado").lower() == theWord
        ):
            return sub_diccionario
    return -1
