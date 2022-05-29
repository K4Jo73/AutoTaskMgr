import os
import random
import string
import sys
from dataclasses import dataclass, field
from operator import and_

import atm_common as common
import atm_logger as audit
import atm_taskdb as db

print("script name is " + __name__)


menuOptions = []
moduleFiles = []


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
        audit.logging.info("\n\nOutputting Full Record")
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
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    return "".join(random.choices(string.ascii_uppercase, k=12))


def addMenuOption(No, Name, Type="Quit", Value="", Params=[]):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    # The match statements below are to make the calls to this function simpler

    match Type:
        case "Menu":
            saveType = "LoadMenu"
            saveValue = Value
        case "Func":
            saveType = "runFunction"
            actionParts = Value.split(".")
            saveValue = "atm_"+actionParts[0]+"."+actionParts[1]
        case _:
            saveType = Type
            saveValue = Value

    audit.logging.debug("Type ["+Type+"] changed to ["+saveType+"]")
    audit.logging.debug("Value ["+Value+"] changed to ["+saveValue+"]")

    option = MenuOption(
        # id=generate_id(),
        optionNo=No,
        optionName=Name,
        optionType=saveType,
        optionValue=saveValue,
        optionParams=Params
    )
    option.showFullRecord()
    return option


def loadMainMenu(menuId="1"):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    dbMenuHead = db.getRecords("Menus", "menu_id="+menuId, 1)
    audit.logging.debug("Menu Head: "+str(dbMenuHead[0][1]))
    dbMenuHOptions = db.getRecords("MenuOptions", "menu_id="+menuId)
    for dbOpt in dbMenuHOptions:
        audit.logging.debug("Adding option: "+str(dbOpt))
        menuOptions.append(addMenuOption(
            dbOpt[2], dbOpt[3], dbOpt[4], dbOpt[5]))

    # menuHead = db.getRecords("Menus", "menu_id="+menuId)

    # * This should eventually be filled by a SQL fetch
    # menuOptions.append(addMenuOption(1, "List Active Batches",
    #                    "Func", "taskmgr.listActiveBatches"))
    # menuOptions.append(addMenuOption(
    #     2, "Manage Active Batches", "Func", "taskmgr.manageActiveBatches"))
    # menuOptions.append(addMenuOption(3, "Add Dummy Task",
    #                    "Func", "taskmgr.saveDummyDetailedTask"))
    # params = ["karl.jones@capgemini.com", "Something happened"]
    # menuOptions.append(addMenuOption(4, "Send Test Email",
    #                    "Func", "common.send_Mail", params))
    # params = ["Menus", "menu_id=1"]
    # menuOptions.append(addMenuOption(
    #     5, "menu list", "Func", "taskdb.listRecords", params))
    # params = ["MenuOptions", "menu_id=1"]
    # menuOptions.append(addMenuOption(
    #     6, "menu option list", "Func", "taskdb.listRecords", params))
    # params = ["MenuOptionParams"]
    # menuOptions.append(addMenuOption(
    #     7, "menu option param list", "Func", "taskdb.listRecords", params))
    # menuOptions.append(addMenuOption(9, "Exit", "Quit", ""))
    loadMenu(dbMenuHead[0][1], menuOptions)


def loadMenu(title, options):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    result = "Start"
    while result != "Quit":
        common.clear()
        audit.print_heading('Automation Task Manager')
        optionNos = []
        for x in options:
            opt = "[" + str(x.optionNo) + "] " + x.optionName
            audit.logging.info(opt)
            optionNos.append(x.optionNo)

        menuResult = waitMenuChoice(optionNos, options)
        audit.logging.debug("Menu execution result: "+menuResult)
        if menuResult != "Quit":
            input("\n\tPress Return To Reload Menu\n")
        else:
            break


def waitMenuChoice(optionNos, options):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    selection = input("Please Select From " + str(optionNos) + ":")
    if selection == "":
        selection = "0"
    if selection in str(optionNos):
        for opt in options:
            audit.logging.debug(
                "Checking Option [" + selection + "] against [" + str(opt) + "]")
            if selection == opt.optionNo:
                audit.logging.debug(
                    "Running Valid Option [" + selection + " - " + opt.optionName + "]")
                choiceResult = runMenuAction(
                    opt.optionName, opt.optionType, opt.optionValue, opt.optionParams)
                audit.logging.debug(
                    "Choice execution result: "+choiceResult)
                return choiceResult
            else:
                audit.logging.debug(
                    "Option [" + selection + "] is not a match")
    else:
        audit.logging.info("Invalid Option Number Selected!")
        return "Invalid Option Number Selected"


def runMenuAction(actionName, actionType, actionValue, actionParams=[]):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    audit.logging.debug("Matching menu action: ["+actionName +
                        " - "+actionType+" - "+actionValue + "]")
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
                "Running ["+actionName+"]")  # Must have no more than 1 parameter
            if actionValue.find(".") == -1:
                audit.logging.debug(
                    "Action value does NOT call module function")
                # locals()[actionValue]()
                # globals()[actionValue]()
            else:
                audit.logging.debug("Action value calls module function")
                actionParts = actionValue.split(".")
                module = __import__(actionParts[0])
                func = getattr(module, actionParts[1])
                audit.logging.debug(
                    "Provided parameters: ["+str(actionParams)+"]")
                if not actionParams:
                    func()
                else:
                    func(*actionParams)

        case _:
            audit.logging.info(
                "Invalid action type provided ["+actionName+"] - Ignored")

    return "Done"
