import sys
from tkinter import Y

import atm_common as common
import atm_logger as audit
import atm_menu as menu
import atm_taskdb as taskdb

# import atm_taskmgr as taskmgr

# from datetime import datetime

taskBatchSize = 3

# ? How to do X
# * Highlight
# DONE: Get a batch
# TODO: Process the selected batch
# TODO: Update progress of a queue record
# TODO: Schedule a queue record
# TODO: Allow auto retries
# DONE: Sometimes need to remove batch_id value to allow re-selection to "RESET"
# DONE: Abiltiy to email notifications or reports
# DONE: Cancel a batch
# TODO: Cancel a single task
# TODO: Reset a single task
# DONE: Get email function to work with exchange
# TODO: Storage and use of passwords
# TODO: Status report list active tasks, allow for drill down if needed
# TODO: Management Menu


def main():
    audit.setup_logging("./logs/")
    audit.print_heading('Automation Task Manager')

    # taskdb.getTableColumns("task_status")
    # taskdb.addStatus("DoingEvenMoreStuff","test")
    # taskmgr.getPickList("Status")

    # taskdb.getTableColumns("task_type")
    # taskdb.addType("DoSomething","test")
    # taskmgr.getPickList("Type")

    # taskdb.getTableColumns("task_queue")
    # saveDummyEmptyTask()
    # saveDummyDetailedTask()
    # saveDummyDetailedTask()
    # saveDummyDetailedTask()

    # taskdb.getTableColumns("vw_tasks_active")
    # taskdb.getTableColumns("task_queue")

    # for r in recs:
    #     print(r[1],r[2],r[5])

    # batchToDo = taskmgr.getTaskBatch(taskBatchSize)
    # audit.logging.info(batchToDo)
    # print("")
    # audit.logging.info("Batch Records")
    # print('=' * 50)
    # for rec in batchToDo:
    #     audit.logging.info("ID: "+str(rec[0]))
    #     audit.logging.info("BatchID: "+str(rec[1]))
    #     audit.logging.info("Note: "+str(rec[4]))
    #     audit.logging.info("Source Ref: "+str(rec[8]))
    #     print('-' * 50)
    # print("")

    # taskmgr.listActiveBatches()
    # print("")
    # taskmgr.manageActiveBatches()

    # common.send_Mail("karl.jones@capgemini.com", "Something happened")

    menu.loadMainMenu()


def saveDummyEmptyTask():

    audit.print_line()
    addtaskresult = taskdb.addTask("DoThing")
    audit.logging.info("Added Task ID - " + str(addtaskresult))

    audit.print_subheading("Task Queue Record Detail")
    QueueRecords = taskdb.getRecords(
        "TaskQueue", "task_id = " + str(addtaskresult))

    for queuerec in QueueRecords:
        print(queuerec)

    return QueueRecords


def saveDummyDetailedTask():
    audit.print_line()
    audit.print_subheading("Adding New Task")

    # ParamList
    param1 = ("source_ref", "test record")
    param2 = ("source_id", "abcde-12345-abcde-98765-ZYXWV")
    param3 = ("note", "change that value on users account")
    param4 = ("activity_param01", "John.Smith")
    param5 = ("activity_param02", "thing to be changed")
    paramslist = []
    paramslist.append(param1)
    paramslist.append(param2)
    paramslist.append(param3)
    paramslist.append(param4)
    paramslist.append(param5)

    addtaskresult = taskdb.addTask("DoThing", paramslist)
    audit.logging.info("Added Task ID - " + str(addtaskresult))

    audit.print_subheading("Saved Task Queue Record Detail")
    QueueRecords = taskdb.getRecords(
        "TaskQueue", "task_id = " + str(addtaskresult))

    for queuerec in QueueRecords:
        print(queuerec)

    return QueueRecords


print("script name is " + __name__)
if __name__ == "__main__":
    main()
