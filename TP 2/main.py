from CLI import CLI


def main():

    cli = CLI()
    cli.prompt = '--> '
    cli.cmdloop('Iniciando entrada de comandos. Usar help para ver comandos.')


if __name__ == "__main__":

    main()
