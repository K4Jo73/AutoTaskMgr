import sys
from tkinter import Y

import atm_common as common
import atm_logger as audit
import atm_menu as menu
import atm_taskdb as taskdb
import atm_taskmgr as taskmgr

# from datetime import datetime

taskBatchSize = 3

# The Comment patterns below change color due to the "Better-Comments" extension being installed
# // Strike Through
# ? How to do X
# * Highlight
# ! Alert
# DONE: Get a batch
# TODO: Process the selected batch
# TODO: Update progress of a queue record
# TODO: Schedule a queue record
# TODO: Allow auto retries
# TODO: Cancel a single task
# TODO: Reset a single task
# TODO: Storage and use of passwords
# TODO: Settings for execution like mail server etc. use db maybe and add mgt in menus
# Active: Menu to call more menus - Use db to store
# TODO: Status report list active tasks, allow for drill down if needed
# Done: Management Menu
# TODO: Want to be able to trigger prompt params when menu triggers a function (may just add to the functions)
# TODO: Bypass menu straight to action


def main():
    audit.setup_logging("./logs/")
    audit.print_heading('Automation Task Manager')
    menu.loadMainMenu()


def oldTestCode():
    # * THIS IS OLD LINES OF CODE USED TO TEST FUNCTIONALITY
    taskdb.getTableColumns("task_status")
    taskdb.addStatus("DoingEvenMoreStuff", "test")
    taskmgr.getPickList("Status")

    taskdb.getTableColumns("task_type")
    taskdb.addType("DoSomething", "test")
    taskmgr.getPickList("Type")

    taskdb.getTableColumns("task_queue")

    taskdb.getTableColumns("vw_tasks_active")
    taskdb.getTableColumns("task_queue")

    batchToDo = taskmgr.getTaskBatch(taskBatchSize)
    audit.logging.info(batchToDo)
    print("")
    audit.logging.info("Batch Records")
    print('=' * 50)
    for rec in batchToDo:
        audit.logging.info("ID: "+str(rec[0]))
        audit.logging.info("BatchID: "+str(rec[1]))
        audit.logging.info("Note: "+str(rec[4]))
        audit.logging.info("Source Ref: "+str(rec[8]))
        print('-' * 50)
    print("")

    taskmgr.listActiveBatches()
    print("")
    taskmgr.manageActiveBatches()

    common.send_Mail("karl.jones@capgemini.com", "Something happened")


print("script name is " + __name__)
if __name__ == "__main__":
    main()
