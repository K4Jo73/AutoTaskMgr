from tkinter import Y
import sys
import atm_logger as audit
import atm_common as common
import atm_taskdb as taskdb
import atm_taskmgr as taskmgr
from datetime import datetime

taskBatchSize = 3 

# ? How to do X
# * Get a batch DONE!
# TODO: Process the selected batch
# TODO: Update progress of a queue record
# TODO: Schedule a queue record
# TODO: Allow auto retries
# TODO: Sometimes need to remove batch_id value to allow re-selection
# TODO: Abiltiy to email notifications or reports




def main():
    audit.setup_logging("./logs/")
    audit.print_heading('Automation Task Manager')

    # taskdb.getTableColumns("task_status")
    # taskdb.addStatus("DoingStuff","test")
    # taskmgr.getPickList("Status")
    
    # taskdb.getTableColumns("task_type")
    # taskdb.addType("DoSomething","test")
    # taskmgr.getPickList("Type")

    # taskdb.getTableColumns("task_queue")
    # saveDummyEmptyTask()
    # saveDummyDetailedTask()


    taskdb.getTableColumns("vw_tasks_active")
    # taskdb.getTableColumns("task_queue")

    # for r in recs:
    #     print(r[1],r[2],r[5])

    # batchToDo = taskmgr.getTaskBatch(taskBatchSize)  
    # audit.logging.info(batchToDo)


    # taskmgr.listActiveBatches()
    print("")
    taskmgr.manageActiveBatches()


   




def saveDummyEmptyTask():

    audit.print_line()
    addtaskresult = taskdb.addTask("DoThing")
    audit.logging.info("Added Task ID - " + str(addtaskresult))

    audit.print_subheading("Task Queue Record Detail")
    QueueRecords = taskdb.getRecords("TaskQueue", "task_id = " + str(addtaskresult))

    for queuerec in QueueRecords:
        print(queuerec)

    return QueueRecords


def saveDummyDetailedTask():
    audit.print_line()
    audit.print_subheading("Adding New Task")

    #ParamList
    param1 = ("source_ref","test record")
    param2 = ("source_id","abcde-12345-abcde-98765-ZYXWV")
    param3 = ("note","change that value on users account")
    param4 = ("activity_param01","John.Smith")
    param5 = ("activity_param02","thing to be changed")
    paramslist = []
    paramslist.append(param1)
    paramslist.append(param2)
    paramslist.append(param3)
    paramslist.append(param4)
    paramslist.append(param5)

    addtaskresult = taskdb.addTask("DoThing",paramslist)
    audit.logging.info("Added Task ID - " + str(addtaskresult))

    audit.print_subheading("Saved Task Queue Record Detail")
    QueueRecords = taskdb.getRecords("TaskQueue", "task_id = " + str(addtaskresult))

    for queuerec in QueueRecords:
        print(queuerec)

    return QueueRecords




print("script name is " + __name__)
if __name__ == "__main__":
    main()
