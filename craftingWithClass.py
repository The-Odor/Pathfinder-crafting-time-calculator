import sys

class Crafting():
    """
    A class to calculate crafting progress for the roleplaying game Pathfinder 1e
    """
    def __init__(self):
        self.spellcraftMOD = None
        self.casterLevel   = None
        self.NreqNotMet    = None
        self.Nhelpers      = None
        self.amazingTools  = None
        self.iounStoneBool = None


    def inputDefault(self, arg, default):
        """
        Returns arg if it is valid, returns default otherwise
        """
        arg = arg.lower()
        if isinstance(default, int):
            if len(arg)==0:
                return default
            else:
                return int(arg)
        default = default.lower()
        if default == "y":
            return not arg == "n"
        elif default == "n":
            return not arg == "y"

        
    def getValues(self, default=False):
        """
        Asks for relevant values from user
        Defaults to command-line arguments if the correct number (6) is given
        Defaults to getValuesDefault() if default argument is set to True
        """
        Narguments = 6

        try:
            if len(sys.argv) == Narguments+1:
                self.getValuesDefault(CMDarg = True)
                return
            elif sys.argv[1] == "default" or default:
                self.getValuesDefault(CMDarg = False)
                return
        except IndexError:
            if default:
                self.getValuesDefault(CMDarg = False)
                return
        print("Welcome to the crafting calculator!!\n")

        self.spellcraftMOD = int(input("Spellcrafting Modifier : "))
        self.casterLevel   = int(input("Crafting CL            : "))
        self.NreqNotMet    = self.inputDefault(input("#Requirements not met: [DFLT0] "), 0)
        self.Nhelpers      = self.inputDefault(input("#Helpers?:             [DFLT1] "), 1)
        self.amazingTools  = self.inputDefault(input("Amazing Tools apply?:  [ Y/n ] "), "Y")
        self.iounStoneBool = self.inputDefault(input("time for Ioun stone?:  [ Y/n ] "), "Y")

        if not self.NreqNotMet: self.NreqNotMet=0
        else: self.NreqNotMet = int(self.NreqNotMet)


    def getValuesDefault(self, CMDarg):
        """
        Defaults relevant values, for easy use when bugfixing
        """

        print("Crafting calculator; defaulting values")

        if CMDarg:
            print("using command line arguments")
            # print(sys.argv)
            # exit()
            self.spellcraftMOD = int(sys.argv[1])
            self.casterLevel = int(sys.argv[2])
            self.NreqNotMet = self.inputDefault(sys.argv[3], 0)
            self.Nhelpers = self.inputDefault(sys.argv[4], 1)
            self.amazingTools = self.inputDefault(sys.argv[5], "Y")
            self.iounStoneBool = self.inputDefault(sys.argv[6], "Y")
        else: 
            print("\n"+" "*17 + """Spellcraft modifier  = 16
                    Caster Level of item = 7
                    requirements not met = 1
                    Helping       : Mon Kie
                    Amazing tools : Apply
                    ioun Stone    : Used\n""")

            self.spellcraftMOD = 15
            self.casterLevel   = 8
            self.NreqNotMet    = 0
            self.Nhelpers      = 1
            self.amazingTools  = True
            self.iounStoneBool = True


    def craftingProgress(self):
        """
        Calculates crafting progress for a single day, under multiple conditions
        """
        take10Spellcraft = self.spellcraftMOD + 10
        take10Spellcraft+= self.amazingTools*4 + self.Nhelpers*2 + self.iounStoneBool # Boolean arithmetic is just neat

        spellcraftDC = self.casterLevel + 5 + self.NreqNotMet*5

        if spellcraftDC > take10Spellcraft:
            print("\nTaking 10 ({}) does not pass DC ({})".format(take10Spellcraft, spellcraftDC))
            return

        craftMod = 2**(((take10Spellcraft - spellcraftDC) // 5) + self.Nhelpers)

        tools1hrEffect = 2000
        toolsOfManufactureNorm = (tools1hrEffect - (1/8)*1000*craftMod)*self.amazingTools
        toolsOfManufactureAdv  = (tools1hrEffect - (1/8)*(1/2)*1000*craftMod)*self.amazingTools
        ringOfSustenance = (6/8)*1000*craftMod

        craftAdv  = toolsOfManufactureAdv + (4/8)*(1/2)*1000*craftMod
        craftSust = craftAdv + ringOfSustenance/2

        craftNorm = toolsOfManufactureNorm + 1000*craftMod
        craftBIG  = craftNorm + ringOfSustenance

        print("""
        Progress for adventuring: {}gp
                w/ ring of Sust.: {}gp
        Progress whilst chilling: {}gp
                w/ ring of Sust.: {}gp
        with a crafting modifier of {} and {} skill points in excess""".format(int(craftAdv), 
                                                 int(craftSust), 
                                                 int(craftNorm), 
                                                 int(craftBIG), 
                                                 int(craftMod), int((take10Spellcraft-spellcraftDC)%5)))


    def run(self):
        """
        Contains main loop for class
        """
        defaultBool = False
        while True:

            self.getValues(defaultBool)

            self.craftingProgress()

            if input("\n\npress Enter to exit ('c' to go again) ") != "c":
                break

            print("\n\n\nAnd once again: ", end="")


if __name__ == "__main__":

    Crafting().run()