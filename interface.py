import os
import appLogic
import unicodedata


## Funciones útiles
def clean_screen():
    os.system("cls" if os.name == "nt" else "clear")  ##CLS si es Windows, else CLEAR


def print_start():
    print("====PROGRAMA DE ASISTENCIA AL APRENDIZAJE DE JAPONÉS====")
    print(
        f"Elija una opción:\n\tA) Revisar lista de vocabulario.\n\tB) Buscar una palabra específica en el vocabulario.\n\tC) Modo examen\n\tD) Traducir frase\n\tE) Editar palabra del vocabulario\n\tX) Exit"
    )  ##TODO: añadir opciones


def stop_backToMenu():
    print("~" * 10)
    input("Presione ENTER para volver al menú...")


clean_screen()


def start_app():
    while True:
        clean_screen()
        print_start()
        option = input(">>>")

        valid_opt = ["a", "b", "c", "d", "e", "x"]  ##opciones del menú
        while option.lower() not in valid_opt:
            print("Por favor, escoja una opción válida")
            option = input(">>>")

        if option.lower() == valid_opt[0]:  ## LISTA DE VOCABULARIO
            clean_screen()
            print(
                "-- Lista de vocabulario --\nÚltima actualización: "
            )  ## TODO: Añadir fecha
            for word in appLogic.currentVocab:
                print(word)
                for element, value in appLogic.currentVocab.get(word).items():
                    print(f"|-> {element}: {value}")
            stop_backToMenu()

        elif option.lower() == valid_opt[1]:  ## BUSCAR PALABRA
            clean_screen()
            print(
                "---:-- Buscador de palabras --:---\nPor favor, escoja una opción:\n\tA) Buscar palabra en castellano\n\tB) Buscar palabra en su romanización"
            )
            option = input(">>>")

            search_valid_opt = ["a", "b"]
            while option.lower() not in search_valid_opt:
                option = input("ERROR: Por favor, escoja una opción válida:\n>>>")

            word = input("> Buscar la palabra ...\n>>>")

            if option.lower() == search_valid_opt[0]:
                data = appLogic.searchWordSpanish(word.lower())
                if data == -1:
                    print(f"ERROR: The word {word} isn't part of the vocabulary list")
                else:
                    for element, value in data.items():
                        print(f"|-> {element}: {value}")
            elif option.lower() == search_valid_opt[1]:
                data = appLogic.searchWordRomaji(word.lower())
                if data == -1:
                    print(f"ERROR: The word {word} isn't part of the vocabulary list")
                else:
                    for element, value in data.items():
                        print(f"|->{element}: {value}")
            stop_backToMenu()

        elif option.lower() == valid_opt[2]:  ##QUIZ
            if len(appLogic.currentVocab) < 10:
                print(
                    "Lo sentimos, no puedes entrar al modo examen si tu lista de vocabulario es inferior a 10 palabras."
                )
                stop_backToMenu()
                continue
            clean_screen()
            print("---- Modo examen ----")
            print("\tA) Palabra individual\n\tB) Examen de diez palabras")

            quiz_valid_opts = ["a", "b"]

            option = input(">>>")

            while option.lower() not in quiz_valid_opts:
                print("Please, enter a valid option")
                option = input(">>>")

            if option.lower() == quiz_valid_opts[0]:
                clean_screen()
                wordChoice = appLogic.getRandomWord()
                hiragana = appLogic.currentVocab.get(wordChoice).get("hiragana")
                print(f"->WORD: {hiragana} ({wordChoice})")

                answer = input("Introduzca el signficiado en castellano:\n>>>")
                printText = appLogic.checkAnswer(answer, wordChoice)

                print("-" * 10)
                print(printText)
                appLogic.saveVocab(appLogic.currentVocab)

                stop_backToMenu()

            elif option.lower() == quiz_valid_opts[1]:
                clean_screen()
                wordList = appLogic.getTenRandomWords()
                for word in wordList:
                    hiragana = appLogic.currentVocab.get(word).get("hiragana")
                    print(f"->WORD: {hiragana} ({word})")

                    answer = input("Introduzca el signficiado en castellano:\n>>>")
                    printText = appLogic.checkAnswer(answer, word)

                    print("-" * 10)
                    print(printText)
                    appLogic.saveVocab(appLogic.currentVocab)
                stop_backToMenu()

        elif option.lower() == valid_opt[3]:
            clean_screen()
            print("---Interfaz de traducción---")
            spanishSentence = input("\tIntroduzca la frase a traducir:\n>>>")
            allElements = appLogic.extractCandidates(spanishSentence)
            if len(allElements) == 0:
                print("> No se ha podido encontrar ningún elemento analizable.")
                stop_backToMenu()
            for element in allElements:
                print(
                    f"{element[1]}\n\tHiragana: {element[2]}\n\tRomaji: {element[0]}\n\tSignificado: {element[3]}"
                )
                saveChoice = input(
                    "¿Deseas guardar esta palabra en el vocabulario?\n>>>(Y/N):"
                )
                while saveChoice not in ("Y", "N"):
                    saveChoice = input(
                        "> Por favor, introduzca una respuesta válida.\n¿Deseas guardar esta palabra en el vocabulario?\n>>>(Y/N):"
                    )
                if saveChoice == "Y":
                    if element[0] in appLogic.currentVocab:
                        print("> Esta palabra ya existe en el vocabulario!")
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

        elif option.lower() == valid_opt[4]:  ## EDITAR PALABRA
            clean_screen()
            print("---- Editar palabra ----")
            word = input("> Introduzca la palabra a editar (romaji o castellano):\n>>>")
            key = appLogic.findVocabKey(word.lower())
            if key == -1:
                print(f"ERROR: La palabra '{word}' no existe en el vocabulario")
                stop_backToMenu()
                continue
            partValidOpt = ["a", "b", "c"]
            partToEdit = input(
                "------------\nA) Hiragana\nB) Kanji\nC) Significado\n>>>"
            )
            while partToEdit.lower() not in partValidOpt:
                partToEdit = input(
                    "Opción inválida, por favor introduzca una opción válida:\n>>>"
                )
            newValue = input("Por favor, introduzca el nuevo valor:\n>>>")
            appLogic.updateWordField(
                key,
                appLogic.allowedFieldModifications[
                    partValidOpt.index(partToEdit.lower())
                ],
                newValue,
            )
            stop_backToMenu()

            # pedir la opción, pedir el nuevo valor, llamar a appLogic.updateWordField(key, campo, nuevoValor)

        elif option.lower() == valid_opt[5]:  ##SALIR DEL PROGRAMA
            clean_screen()
            print("Adiós! またね!")
            appLogic.saveVocab(appLogic.currentVocab)
            break
