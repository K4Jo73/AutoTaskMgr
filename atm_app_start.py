from tkinter import Y
import atm_logger as audit
import atm_taskdb as taskdb
import atm_common as common
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
    # getPickList("Status")
    
    # taskdb.getTableColumns("task_type")
    # taskdb.addType("DoSomething","test")
    # getPickList("Type")

    # taskdb.getTableColumns("task_queue")
    # saveDummyEmptyTask()
    # saveDummyDetailedTask()


    # taskdb.getTableColumns("vw_tasks_active")
    # taskdb.getTableColumns("task_queue")
    # recs = getSomeTasks(10)
    # recs = getSomeTasks(10,"Active")
    # recs = getSomeTasks(10,"Closed")
    # recs = getSomeTasks(10,"Error")
    # recs = getSomeTasks(10,"Hold")

    # for r in recs:
    #     print(r[1],r[2],r[5])

    # batchToDo = getTaskBatch(taskBatchSize)  
    # audit.logging.info(batchToDo)


    listActiveBatches()
    print("")
    manageActiveBatches()


def listActiveBatches():
    ActiveBatches = getTaskActiveBatchIDs()
    # audit.logging.info(ActiveBatches)
    audit.logging.info("Current active batches....")
    print("")
    for r in ActiveBatches:
        # audit.logging.info(r[0])
        audit.logging.info("["+r[0]+"n]")
    

def manageActiveBatches():
    ActiveBatches = getTaskActiveBatchIDs()
    # audit.logging.info(ActiveBatches)
    audit.logging.info("Current active batches to manage....")
    print("")
    for r in ActiveBatches:
        # audit.logging.info(r[0])
        takeAction = "["+r[0]+"n] Take action on this batch?"
        actionAnswer = common.yes_or_no(takeAction)
        audit.logging.debug(takeAction + " :" + str(actionAnswer))
        if actionAnswer == True:
            cancelBatch = "\tCancel this batch?"
            cancelAnswer = common.yes_or_no(cancelBatch)
            audit.logging.debug(cancelBatch + " :" + str(cancelAnswer))
            if cancelAnswer == True:
                audit.logging.info("\t\tCancelling ["+r[0]+"]...")
            else:
                resetBatch = "\tReset this batch?"
                resetAnswer = common.yes_or_no(resetBatch)
                audit.logging.debug(resetBatch + " :" + str(resetAnswer))
                if resetAnswer == True:
                    audit.logging.info("\t\tResetting ["+r[0]+"]...")
        print("")





def getTaskActiveBatchIDs():
    queueRecords = taskdb.getCustomRecordList("Select batch_id FROM atm.vw_tasks_active WHERE batch_id IS NOT NULL Group By batch_id")
    for r in queueRecords:
        audit.logging.debug(r[0])
    return queueRecords




def getTaskBatch(batchSize):
    date_string = f'{datetime.now():%Y-%m-%d_%H-%M-%S%z}'
    thisBatchId = "Batch_"+date_string
    audit.logging.debug("Batch ID: "+thisBatchId)

    validStatusIDs = taskdb.getRecords("TaskStatus","is_open=1 and is_hold=0 and is_error=0 and is_progress=0")

    statusIdList = ""
    separator = ""
    for ids in validStatusIDs:
        statusIdList += separator + str(ids[0])
        separator = ", "
        audit.logging.debug("Valid Status ID: "+str(ids[0])+" - "+str(ids[1]))
    audit.logging.debug("Batch Status ID List: "+statusIdList)

    param1 = ("batch_id",thisBatchId)
    paramslist = []
    paramslist.append(param1)
    recsToBatch = taskdb.updateTasks("batch_id is NULL and task_status in ("+statusIdList+")",paramslist,batchSize)

    if recsToBatch == "Records Updated":
        queueRecords = taskdb.getRecords("TaskQueue","batch_id = '"+thisBatchId+"'",batchSize)

    audit.logging.debug("Queue Recs In This Batch")
    for r in queueRecords:
        audit.logging.debug(r)

    return queueRecords

   




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


def getPickList(listtype):
    audit.print_subheading("Task "+ listtype + " List")
    Records = taskdb.getRecords("Task" + listtype)

    for rec in Records:
        # print(rec[0], rec[1])
        print(rec)

    audit.print_line()
   
    return Records




print("script name is " + __name__)
if __name__ == "__main__":
    main()
