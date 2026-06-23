import os
import sys
import appLogic


## Funciones útiles
def clean_screen():
    os.system("cls" if os.name == "nt" else "clear")  ##CLS si es Windows, else CLEAR


def print_start():
    print("-" * 50)
    print("\tASISTENTE DE APRENDIZAJE DE JAPONÉS")
    print("-" * 50)
    print("\tA) Manejar vocabulario")
    print("\tB) Modo examen")
    print("\tC) Traducir frase")
    print("\tX) Salir")


def stop_backToMenu():
    print("-" * 50)
    input("Presione ENTER para volver al menú...")


clean_screen()


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
    print("-" * 50)
    print("\tLISTA DE VOCABULARIO")
    print("-" * 50)
    print("\tÚltima actualización: ")  ## TODO: Añadir fecha
    print("-" * 50)
    for word in appLogic.currentVocab:
        print(f"\t{word}")
        for element, value in appLogic.currentVocab.get(word).items():
            print(f"\t\t{element}: {value}")
    stop_backToMenu()
    return


def searchWordMenu():
    clean_screen()
    print("-" * 50)
    print("\tBUSCADOR DE PALABRAS")
    print("-" * 50)
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

    print("-" * 50)
    print("\tMODO EXAMEN")
    print("-" * 50)
    print("\tA) Palabra individual")
    print("\tB) Examen de diez palabras")

    quiz_valid_opts = ["a", "b"]
    option = input(">> ")

    while option.lower() not in quiz_valid_opts:
        print("ERROR: Por favor, escoja una opción válida")
        option = input(">> ")

    if option.lower() == quiz_valid_opts[0]:
        clean_screen()
        wordChoice = appLogic.getRandomWord()
        hiragana = appLogic.currentVocab.get(wordChoice).get("hiragana")
        print("-" * 50)
        print(f"\t{hiragana} ({wordChoice})")
        print("-" * 50)
        answer = input("\tIntroduzca el significado en castellano:\n>> ")
        printText = appLogic.checkAnswer(answer, wordChoice)
        print("-" * 50)
        print(printText)
        appLogic.saveVocab(appLogic.currentVocab)
        stop_backToMenu()
        return

    elif option.lower() == quiz_valid_opts[1]:
        clean_screen()
        wordList = appLogic.getTenRandomWords()
        for word in wordList:
            hiragana = appLogic.currentVocab.get(word).get("hiragana")
            print("-" * 50)
            print(f"\t{hiragana} ({word})")
            print("-" * 50)
            answer = input("\tIntroduzca el significado en castellano:\n>> ")
            printText = appLogic.checkAnswer(answer, word)
            print("-" * 50)
            print(printText)
            appLogic.saveVocab(appLogic.currentVocab)
        stop_backToMenu()
        return


def translateMenu():
    clean_screen()
    print("-" * 50)
    print("\tTRADUCIR FRASE")
    print("-" * 50)
    spanishSentence = input("\tIntroduzca la frase a traducir:\n>> ")
    allElements = appLogic.extractCandidates(spanishSentence)
    if len(allElements) == 0:
        print("ERROR: No se ha podido encontrar ningún elemento analizable.")
        stop_backToMenu()
        return

    for element in allElements:
        print("-" * 50)
        print(f"\t{element[1]}")
        print(f"\t\tHiragana: {element[2]}")
        print(f"\t\tRomaji: {element[0]}")
        print(f"\t\tSignificado: {element[3]}")
        saveChoice = input(
            "\t¿Deseas guardar esta palabra en el vocabulario? (Y/N):\n>> "
        )
        while saveChoice not in ("Y", "N"):
            saveChoice = input(
                "ERROR: Por favor, introduzca una respuesta válida (Y/N):\n>> "
            )
        if saveChoice == "Y":
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
    print("-" * 50)
    print("\tEDITAR PALABRA")
    print("-" * 50)
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


def manageVocabMenu():
    while True:
        clean_screen()
        print("-" * 50)
        print("\tMANEJAR VOCABULARIO")
        print("-" * 50)
        print("\tA) Listar vocabulario")
        print("\tB) Buscar palabra")
        print("\tC) Editar palabra")
        print("\tX) Volver")
        option = input(">> ")

        valid_options = ["a", "b", "c", "x"]
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
            return


def exitApp():
    clean_screen()
    print("-" * 50)
    print("\tAdiós! またね!")
    print("-" * 50)
    appLogic.saveVocab(appLogic.currentVocab)
    sys.exit()
