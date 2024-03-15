from Tablero import Tablero

RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

def main():

    print("Inicianado el programa...")

    tablero = Tablero()

    option = None

    while option != 0:
        print("====================================")
        print("[0] Salir")
        print("[1] Generar objetivo aleatorio")
        print("[2] Ingresar objetivo manualmente")
        print("[3] Recorrer")

        option = input("Ingrese una opción: ")
        print("====================================")

        try:
            option = int(option)

        except ValueError:
            print(f"{RED}Opción no válida{RESET}")
            continue

        if option == 1:
            tablero.objetivoAleatorio()

        elif option == 2:
            objA = int(input("Ingrese el alias del primer objetivo: "))
            objB = int(input("Ingrese el alias del segundo objetivo: "))

            tablero.objetivoManual(objA, objB)

        elif option == 3:
            tablero.recorrer()

        else:
            print("Opción no válida")

    print("Saliendo del programa...")
    return


if __name__ == "__main__":

    main()

