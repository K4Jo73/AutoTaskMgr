import sys

import atm_common as common
import atm_logger as audit

print("script name is " + __name__)

# # ?: Think I need to define a class here and make an easy way to pump in a list of menu structures
optionNos = [1, 2, 3, 4, 9]
optionNames = ["List Active Batches",
               "Manage Active Batches", "Three", "Four", "Exit"]
optionTypes = ["runFunction", "runFunction", "C", "D", "X"]
optionValues = ["atm_taskmgr.listActiveBatches",
                "atm_taskmgr.manageActiveBatches", "C", "D", "X"]


def loadMainMenu():
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    loadMenu(optionNos, optionNames, optionTypes, optionValues)


def loadMenu(optionNos, optionNames, optionTypes, optionValues):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    common.clear()

    while True:
        for no in range(0, len(optionNos)):
            print(optionNos[no], optionNames[no],
                  optionTypes[no], optionValues[no])

        print("")

        print(optionNos)
        selection = input("Please Select:")
        if selection in str(optionNos):
            if selection == str(optionNos[len(optionNos)-1]):
                print("Exiting Auto Task Manager")
                break
            else:
                for num in range(0, len(optionNos) - 1):
                    if str(optionNos[num]) == selection:
                        runMenuAction(
                            optionNames[num], optionTypes[num], optionValues[num])
        else:
            print("Unknown Option Selected!")

        input("\n\tPress A Key To Reload Menu\n")


def runMenuAction(actionName, actionType, actionValue):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info("Running menu action: "+actionName +
                       " - "+actionType+" - "+actionValue)
    print("")
    match actionType:
        case "loadMenu":
            audit.logging.info(
                "Loading Menu ["+actionName+"]")  # Parameter is menu name
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
