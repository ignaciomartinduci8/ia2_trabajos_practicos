from cmd import Cmd
from Controller import Controller
from DataGen import DataGen

GREEN = "\033[92m"
RESET = "\033[0m"
ROJO = "\033[91m"
LIGHT_BLUE = "\033[94m"
IDENTATION = f"{LIGHT_BLUE}> {RESET}"


class CLI(Cmd):

    doc_header = "Ayuda de comandos documentados"
    undoc_header = "Ayuda de comandos no documentados"
    ruler = "="

    def __init__(self):
        super().__init__()
        self.completekey = 'tab'
        self.DataGen = None
        self.controller = None

    ###################################################

    def do_evaluateCase(self, args):
        """
        Descripción: Iniciar control de caso especial
        Sintaxis: evaluateCase
        """

        if not self.controller:
            self.controller = Controller()

        dia = input(f"{IDENTATION}{GREEN}Ingrese el dia frio/templado/caliente/calienteFrio/frioCaliente:{RESET} ")

        print(f"{IDENTATION}{GREEN}Iniciando control del caso...{RESET}")
        self.controller.evaluateCase(dia)

        self.controller = None

    def do_genYear(self, args):
        """
        Descripción: Generar un año de datos
        Sintaxis: genAño
        """

        print(f"{IDENTATION}{GREEN}Ingrese el año a generar desde la base de datos: {RESET}")

        self.DataGen = DataGen(int(input()))
        self.DataGen = None

    ##################################################

    def default(self, args):
        print(f"{ROJO}Error, el comando /{args} no existe.{RESET}")

    def do_help(self, args):
        """
        Descripción: Obtener ayuda
        Sintaxis: help
        """

        if not args:
            # Si no se proporcionan argumentos, mostrar una lista de comandos disponibles
            self.stdout.write(f"{GREEN}Comandos disponibles:{RESET}\n")
            for command in self.get_names():
                if command.startswith("do_"):
                    self.stdout.write(f"- {command[3:]}\n")
        else:
            # Si se proporciona un argumento, intentar mostrar ayuda específica para ese comando
            try:
                super().do_help(args)
            except AttributeError:
                self.stdout.write(f"No se encontró ayuda para el comando '{args}'\n")

    def precmd(self, args):

        return args

    def preloop(self):
        print('\n========== CLI de servidor ==========')
