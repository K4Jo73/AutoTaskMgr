import random
import string
import sys
from dataclasses import dataclass, field
from operator import and_

import atm_common as common
import atm_logger as audit

# from sre_constants import CATEGORY


print("script name is " + __name__)

# # ?: Think I need to define a class here and make an easy way to pump in a list of menu structures
# optionNos = [1, 2, 3, 4, 9]
# optionNames = ["List Active Batches",
#                "Manage Active Batches", "Add Dummy Task", "Send Test Email", "Exit"]
# optionTypes = ["runFunction", "runFunction", "runFunction", "", "X"]
# optionValues = ["atm_taskmgr.listActiveBatches",
#                 "atm_taskmgr.manageActiveBatches", "atm_taskmgr.saveDummyDetailedTask", "atm_common.send_Mail", "X"]


menuOptions = []


@dataclass(kw_only=True)
class MenuOption:
    id: str = "00"
    optionNo: int
    optionName: str
    optionType: str
    optionValue: str

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


def addMenuOption(No, Name, Type, Value):
    opt = MenuOption(
        # id=generate_id(),
        optionNo=No,
        optionName=Name,
        optionType=Type,
        optionValue=Value
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
    menuOptions.append(addMenuOption(
        4,
        "Send Test Email",
        "",
        "atm_common.send_Mail"))
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

    while True:
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
                        opt.optionName, opt.optionType, opt.optionValue)
                    if result == "Quit":
                        break
                    # else:
                    #     return
                else:
                    audit.logging.debug(
                        "Option [" + selection + "] is not a match")
        else:
            print("Unknown Option Selected!")

        input("\n\tPress Return To Reload Menu\n")


def runMenuAction(actionName, actionType, actionValue):
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
                globals()[actionValue]()
            else:
                audit.logging.debug("\tAction value does call module function")
                actionParts = actionValue.split(".")
                module = __import__(actionParts[0])
                func = getattr(module, actionParts[1])
                func()

        case _:
            audit.logging.info(
                "Invalid action type provided ["+actionName+"] - Ignored")

    return "Done"
