import random
import string
import sys
from dataclasses import dataclass, field
from operator import and_

import atm_common as common
import atm_logger as audit

print("script name is " + __name__)


menuOptions = []


@dataclass(kw_only=True)
class MenuOption:
    id: str = "00"
    optionNo: int
    optionName: str
    optionType: str
    optionValue: str
    optionParams: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.id = "".join(random.choices(string.ascii_uppercase, k=12))

    def showFullRecord(self):
        audit.logging.info("\n\nOutputting Full Catalog Record")
        for k, v in zip(self.__dict__.keys(), self.__dict__.values()):
            if not k.startswith('_'):
                if k.__eq__('id'):
                    audit.logging.info(k+'\t\t\t: '+str(v))
                else:
                    audit.logging.info(k+'\t\t: '+str(v))

    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._search_string = f"{self.name} {self.set_name} {self.rarity} {self.type_line} {self.keywords}"
        return  # self


def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))


def addMenuOption(No, Name, Type, Value, Params=[]):
    opt = MenuOption(
        # id=generate_id(),
        optionNo=No,
        optionName=Name,
        optionType=Type,
        optionValue=Value,
        optionParams=Params
    )
    return opt


def loadMainMenu():
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    # This should eventually be filled by a SQL fetch
    menuOptions.append(addMenuOption(
        1,
        "List Active Batches",
        "runFunction",
        "atm_taskmgr.listActiveBatches"))
    menuOptions.append(addMenuOption(
        2,
        "Manage Active Batches",
        "runFunction",
        "atm_taskmgr.manageActiveBatches"))
    menuOptions.append(addMenuOption(
        3,
        "Add Dummy Task",
        "runFunction",
        "atm_taskmgr.saveDummyDetailedTask"))
    params = ["karl.jones@capgemini.com", "Something happened"]
    menuOptions.append(addMenuOption(
        4,
        "Send Test Email",
        "runFunction",
        "atm_common.send_Mail",
        params))
    menuOptions.append(addMenuOption(
        9,
        "Exit",
        "Quit",
        ""))

    # for x in menuOptions:
    #     audit.logging.info(x.optionName)
    audit.logging.info(f'\nMenu Options: {len(menuOptions)}')

    loadMenu(menuOptions)


def loadMenu(options):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    result = "Start"
    while result != "Quit":
        common.clear()
        optionNos = []
        for x in options:
            opt = "[" + str(x.optionNo) + "] " + x.optionName
            optionNos.append(x.optionNo)
            audit.logging.info(opt)

        # print(optionNos)
        selection = input("Please Select From " + str(optionNos) + ":")
        if selection == "":
            selection = "0"
        if selection in str(optionNos):
            for opt in options:
                audit.logging.debug(
                    "\nChecking Option [" + selection + "] against [" + str(opt) + "]")
                if int(selection) == opt.optionNo:
                    audit.logging.info(
                        "\n\nRunning Option [" + selection + "]")
                    result = runMenuAction(
                        opt.optionName, opt.optionType, opt.optionValue, opt.optionParams)
                    if result == "Quit":
                        break
                    # else:
                    #     return
                else:
                    audit.logging.debug(
                        "Option [" + selection + "] is not a match")
        else:
            print("Unknown Option Selected!")

        if result != "Quit":
            input("\n\tPress Return To Reload Menu\n")


def runMenuAction(actionName, actionType, actionValue, actionParams=[]):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info("Running menu action: "+actionName +
                       " - "+actionType+" - "+actionValue)
    print("")
    match actionType:
        case "loadMenu":
            audit.logging.info(
                "Loading Menu ["+actionName+"]")  # Parameter is menu name
        case "Quit":
            audit.logging.info("Exiting Auto Task Manager")
            return "Quit"
        case "runFunction":
            audit.logging.info(
                "\tRunning ["+actionName+"]")  # Must have no more than 1 parameter
            if actionValue.find(".") == -1:
                audit.logging.debug(
                    "\tAction value does NOT call module function")
                # locals()[actionValue]()
                # globals()[actionValue]()
            else:
                audit.logging.debug("\tAction value does call module function")
                actionParts = actionValue.split(".")
                module = __import__(actionParts[0])
                func = getattr(module, actionParts[1])
                print(actionParams)
                if not actionParams:
                    func()
                else:
                    func(*actionParams)

        case _:
            audit.logging.info(
                "Invalid action type provided ["+actionName+"] - Ignored")

    return "Done"
