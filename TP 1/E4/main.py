from Tablero import Tablero

RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

def main():

    #NOTA DE USO: No sobrecargar las impresiones de pantalla (plots) porque se saturará el canal HTTP.

    print("Inicianado el programa...")

    tablero = Tablero()

    option = None

    while option != 0:
        print("====================================")
        print("[0] Salir")
        print("[1] Generar objetivo aleatorio")
        print("[2] Ingresar objetivo manualmente")
        print("[3] Recorrer")
        print("[4] Tomar pedido")
        print("[5] Optimizar distribucion")

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
            obj = int(input("Ingrese el alias del punto objetivo: "))

            tablero.objetivoManual(obj)

        elif option == 3:
            tablero.recorrer()

        elif option == 4:
            pedido = input("Ingrese el numero del pedido: ")
            tablero.tomarPedido(pedido)

        elif option == 5:
            print("Optimizando distribución...")
            tablero.reordenarTablero()

        else:
            print("Opción no válida")

    print("Saliendo del programa...")
    return


if __name__ == "__main__":

    main()

