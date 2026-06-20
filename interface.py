import dataDict
import os
import appLogic


## Funciones útiles
def clean_screen():
    os.system("cls" if os.name == "nt" else "clear")  ##CLS si es Windows, else CLEAR


def print_start():
    print("====PROGRAMA DE ASISTENCIA AL APRENDIZAJE DE JAPONÉS====")
    print(
        f"Elija una opción:\n\tA) Revisar lista de vocabulario.\n\tB) Buscar una palabra específica en el vocabulario.\n\tX) Exit"
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

        valid_opt = ["a", "b", "x"]
        while option.lower() not in valid_opt:
            print("Por favor, escoja una opción válida")
            option = input(">>>")

        if option.lower() == valid_opt[0]:  ## LISTA DE VOCABULARIO
            clean_screen()
            print(
                "-- Lista de vocabulario --\nÚltima actualización: "
            )  ## TODO: Añadir fecha
            for word in dataDict.VOCAB_WORDS:
                print(word)
                for element, value in dataDict.VOCAB_WORDS.get(word).items():
                    print(f"|-> {element}: {value}")
            stop_backToMenu()

        if option.lower() == valid_opt[1]:  ## BUSCAR PALABRA
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
            if option.lower() == search_valid_opt[1]:
                data = appLogic.searchWordRomaji(word.lower())
                if data == -1:
                    print(f"ERROR: The word {word} isn't part of the vocabulary list")
                else:
                    for element, value in data.items():
                        print(f"|->{element}: {value}")
            stop_backToMenu()

        if option.lower() == valid_opt[2]:  ##SALIR DEL PROGRAMA
            clean_screen()
            print("Adiós! またね!")
            break
