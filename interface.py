import os
import sys
import appLogic

textLongLine = "-" * 50


## Funciones útiles
def clean_screen():
    os.system("cls" if os.name == "nt" else "clear")  ##CLS si es Windows, else CLEAR


def print_start():
    print(f"{textLongLine}")
    print("\tASISTENTE DE APRENDIZAJE DE JAPONÉS")
    print(f"{textLongLine}")
    print("\tA) Manejar vocabulario")
    print("\tB) Modo examen")
    print("\tC) Traducir frase")
    print("\tX) Salir")


def stop_backToMenu():
    print(f"{textLongLine}")
    input("Presione ENTER para volver al menú...")


def mainMenu():
    while True:
        clean_screen()
        print_start()
        option = input(">> ")
        valid_opt = ["a", "b", "c", "x"]  ##opciones del menú
        while option.lower() not in valid_opt:
            print("ERROR: Por favor, escoja una opción válida")
            option = input(">> ")
        if option.lower() == valid_opt[0]:
            manageVocabMenu()
        elif option.lower() == valid_opt[1]:
            quizMenu()
        elif option.lower() == valid_opt[2]:
            translateMenu()
        elif option.lower() == valid_opt[3]:
            exitApp()


def vocabListMenu():
    clean_screen()
    print(f"{textLongLine}")
    print("\tLISTA DE VOCABULARIO")
    print(f"{textLongLine}")
    print(f"\tÚltima actualización: {appLogic.lastEdit}")  ## TODO: Añadir fecha
    print(f"{textLongLine}")
    for word in appLogic.currentVocab:
        print(f"\t{word}")
        for element, value in appLogic.currentVocab.get(word).items():
            print(f"\t\t{element}: {value}")
    stop_backToMenu()
    return


def searchWordMenu():
    clean_screen()
    print(f"{textLongLine}")
    print("\tBUSCADOR DE PALABRAS")
    print(f"{textLongLine}")
    print("\tA) Buscar palabra en castellano")
    print("\tB) Buscar palabra en su romanización")
    print("\tX) Volver")
    option = input(">> ")

    search_valid_opt = ["a", "b", "x"]
    while option.lower() not in search_valid_opt:
        print("ERROR: Por favor, escoja una opción válida")
        option = input(">> ")

    if option.lower() == search_valid_opt[2]:
        return

    word = input("\tBuscar la palabra...\n>> ")

    if option.lower() == search_valid_opt[0]:
        data = appLogic.searchWordSpanish(word.lower())
        if data == -1:
            print(f"ERROR: La palabra '{word}' no existe en el vocabulario")
        else:
            for element, value in data.items():
                print(f"\t\t{element}: {value}")
    elif option.lower() == search_valid_opt[1]:
        data = appLogic.searchWordRomaji(word.lower())
        if data == -1:
            print(f"ERROR: La palabra '{word}' no existe en el vocabulario")
        else:
            for element, value in data.items():
                print(f"\t\t{element}: {value}")

    stop_backToMenu()
    return


def quizMenu():
    if len(appLogic.currentVocab) < 10:
        print(
            "ERROR: No puedes entrar al modo examen si tu vocabulario tiene menos de 10 palabras."
        )
        stop_backToMenu()
        return

    print(f"{textLongLine}")
    print("\tMODO EXAMEN")
    print(f"{textLongLine}")
    print("\tA) Palabra individual")
    print("\tB) Examen de diez palabras")
    print("\tX) Volver")

    quiz_valid_opts = ["a", "b", "x"]
    option = input(">> ")

    while option.lower() not in quiz_valid_opts:
        print("ERROR: Por favor, escoja una opción válida")
        option = input(">> ")

    if option.lower() == quiz_valid_opts[2]:
        stop_backToMenu()
        return

    elif option.lower() == quiz_valid_opts[0]:
        clean_screen()
        wordChoice = appLogic.getRandomWord()
        hiragana = appLogic.currentVocab.get(wordChoice).get("hiragana")
        print(f"{textLongLine}")
        print(f"\t{hiragana} ({wordChoice})")
        print(f"{textLongLine}")
        answer = input("\tIntroduzca el significado en castellano:\n>> ")
        printText = appLogic.checkAnswer(answer, wordChoice)
        print(f"{textLongLine}")
        print(printText)
        appLogic.saveVocab(appLogic.currentVocab)
        stop_backToMenu()
        return

    elif option.lower() == quiz_valid_opts[1]:
        clean_screen()
        wordList = appLogic.getTenRandomWords()
        for word in wordList:
            hiragana = appLogic.currentVocab.get(word).get("hiragana")
            print(f"{textLongLine}")
            print(f"\t{hiragana} ({word})")
            print(f"{textLongLine}")
            answer = input("\tIntroduzca el significado en castellano:\n>> ")
            printText = appLogic.checkAnswer(answer, word)
            print(f"{textLongLine}")
            print(printText)
            appLogic.saveVocab(appLogic.currentVocab)
        stop_backToMenu()
        return


def translateMenu():
    clean_screen()
    print(f"{textLongLine}")
    print("\tTRADUCIR FRASE")
    print(f"{textLongLine}")
    spanishSentence = input("\tIntroduzca la frase a traducir:\n>> ")
    allElements = appLogic.extractCandidates(spanishSentence)
    if len(allElements) == 0:
        print("ERROR: No se ha podido encontrar ningún elemento analizable.")
        stop_backToMenu()
        return

    for element in allElements:
        print(f"{textLongLine}")
        print(f"\t{element[1]}")
        print(f"\t\tHiragana: {element[2]}")
        print(f"\t\tRomaji: {element[0]}")
        print(f"\t\tSignificado: {element[3]}")
        saveChoice = input(
            "\t¿Deseas guardar esta palabra en el vocabulario? (Y/N):\n>> "
        )

        saveChoiceOptions = ["y", "n"]
        while saveChoice.lower() not in saveChoiceOptions:
            saveChoice = input(
                "ERROR: Por favor, introduzca una respuesta válida (Y/N):\n>> "
            )
        if saveChoice.lower() == saveChoiceOptions[0]:
            if element[0] in appLogic.currentVocab:
                print("ERROR: Esta palabra ya existe en el vocabulario.")
                stop_backToMenu()
                continue
            dictionaryEntry = {
                "kanji": element[1],
                "hiragana": element[2],
                "significado": element[3],
                "nivel": 0.50,
            }
            appLogic.currentVocab[element[0]] = dictionaryEntry
    appLogic.saveVocab(appLogic.currentVocab)
    stop_backToMenu()
    return


def editWordMenu():
    clean_screen()
    print(f"{textLongLine}")
    print("\tEDITAR PALABRA")
    print(f"{textLongLine}")
    word = input("\tIntroduzca la palabra a editar (romaji o castellano):\n>> ")
    key = appLogic.findVocabKey(word.lower())
    if key == -1:
        print(f"ERROR: La palabra '{word}' no existe en el vocabulario")
        stop_backToMenu()
        return

    print("\tA) Hiragana")
    print("\tB) Kanji")
    print("\tC) Significado")
    partToEdit = input(">> ")

    partValidOpt = ["a", "b", "c"]
    while partToEdit.lower() not in partValidOpt:
        print("ERROR: Opción inválida")
        partToEdit = input(">> ")

    newValue = input("\tPor favor, introduzca el nuevo valor:\n>> ")
    appLogic.updateWordField(
        key,
        appLogic.allowedFieldModifications[partValidOpt.index(partToEdit.lower())],
        newValue,
    )
    stop_backToMenu()
    return


def deleteWordMenu():
    clean_screen()
    print(f"{textLongLine}")
    print("\tELIMINAR PALABRA")
    print(f"{textLongLine}")
    wordToDelete = input("\tIntroduzca la palabra a eliminar\n>>")

    key = appLogic.findVocabKey(wordToDelete.lower())

    if key == -1:
        print("\tERROR: No se pudo encontrar la palabra buscada")
        stop_backToMenu()
        return

    data = appLogic.currentVocab[key]

    for element, value in data.items():
        print(f"\t\t{element}: {value}")
    deleteConfir = input(
        "\t¿Está seguro de eliminar esta entrada en el vocabulario?\n>>(Y/N)"
    )

    validDeleteConfir = ["y", "n"]

    while deleteConfir.lower() not in validDeleteConfir:
        deleteConfir = input("\tPor favor, escoja una opción válida.\n>>(Y/N)")

    if deleteConfir.lower() == validDeleteConfir[0]:
        appLogic.deleteWord(key)
        print("\tPalabra eliminada satisfactoriamente")
        stop_backToMenu()
        return

    stop_backToMenu()
    return


def manageVocabMenu():
    while True:
        clean_screen()
        print(f"{textLongLine}")
        print("\tMANEJAR VOCABULARIO")
        print(f"{textLongLine}")
        print("\tA) Listar vocabulario")
        print("\tB) Buscar palabra")
        print("\tC) Editar palabra")
        print("\tD) Eliminar palabra")
        print("\tX) Volver")
        option = input(">> ")

        valid_options = ["a", "b", "c", "d", "x"]
        while option.lower() not in valid_options:
            print("ERROR: Por favor, introduzca una opción válida")
            option = input(">> ")

        if option.lower() == valid_options[0]:
            vocabListMenu()
        elif option.lower() == valid_options[1]:
            searchWordMenu()
        elif option.lower() == valid_options[2]:
            editWordMenu()
        elif option.lower() == valid_options[3]:
            deleteWordMenu()
        elif option.lower() == valid_options[4]:
            return


def exitApp():
    clean_screen()
    print(f"{textLongLine}")
    print("\tAdiós! またね!")
    print(f"{textLongLine}")
    appLogic.saveVocab(appLogic.currentVocab)
    sys.exit()
