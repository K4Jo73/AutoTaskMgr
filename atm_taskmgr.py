import os
import sys
from datetime import datetime
from select import select
from tkinter import Y

import atm_common as common
import atm_logger as audit
import atm_menu as menu
import atm_taskdb as taskdb

print("script name is " + __name__)


def listActiveBatches():
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    ActiveBatches = getTaskActiveBatchIDs()
    # audit.logging.info(ActiveBatches)
    audit.logging.info("Current active batches....")
    print("")
    for r in ActiveBatches:
        # audit.logging.info(r[0])
        audit.logging.info(r[0])


def manageActiveBatches():
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    ActiveBatches = getTaskActiveBatchIDs()
    audit.logging.info("Current active batches to manage....")
    print("")
    for r in ActiveBatches:
        audit.logging.info(r[0])
        recordsForBatch = getTaskActiveByBatchID(r[0])
        for batchrecs in recordsForBatch:
            audit.logging.info(
                "\tID: "+str(batchrecs[0])+"\tStatus: "+batchrecs[1]+"\tTask Type: "+batchrecs[2])
        takeAction = "\tTake action on this batch?"
        actionAnswer = common.yes_or_no(takeAction)
        audit.logging.debug(takeAction + " :" + str(actionAnswer))
        if actionAnswer == True:
            wasActioned = batchAction("Cancel", r[0])
            if wasActioned == False:
                wasActioned = batchAction("Reset", r[0])
        print("")


def batchAction(actionName, batchName):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    actionPrompt = "\t\t"+actionName+" this batch?"
    actionAnswer = common.yes_or_no(actionPrompt)
    audit.logging.debug(actionPrompt + " :" + str(actionAnswer))
    if actionAnswer == True:
        audit.logging.info("\t\t\tApplying "+actionName +
                           " action ["+batchName+"]...")
        queueRecordsToUpdate = taskdb.getRecords(
            "TaskQueue", "batch_id = '"+batchName+"'", 0)
        audit.logging.debug("Starting to process records....")
        for upd in queueRecordsToUpdate:
            audit.logging.debug(upd)
            match actionName:
                case "Cancel":
                    UpdTaskResult = setTaskClosed(
                        upd[0], "Cancelled", "Admin Cancelled")
                case "Reset":
                    UpdTaskResult = setTaskReset(
                        upd[0], "New_Pending", "Admin Reset")
                case _:
                    audit.logging.info(
                        "Invalid action type provided ["+actionName+"] - Ignored")
                    UpdTaskResult = False

            if UpdTaskResult == True:
                audit.logging.info("Batch action "+actionName +
                                   " to ["+batchName+"] successful")
            else:
                audit.logging.debug(
                    "Record update for ["+batchName+"]-["+upd[0]+"] failed")
        return True
    else:
        audit.logging.debug("Option to take "+actionName+" action was refused")
        return False


def setTaskClosed(taskID, closureStatus="Completed_Success", closureRef="N/A", closureID="N/A"):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info(
        "Closing Task ["+str(taskID)+"], setting to ["+closureStatus+"]...")
    paramslist = []
    param = ("closed_on", str(datetime.now()))
    paramslist.append(param)
    param = ("closure_id", closureID)
    paramslist.append(param)
    param = ("closure_ref", closureRef)
    paramslist.append(param)
    statusID = taskdb.getID(
        tablename="TaskStatus", criteria="status_name = '"+closureStatus+"'", maxrecords=1)
    param = ("task_status", str(statusID))
    paramslist.append(param)
    recsToUpdate = taskdb.updateTasks(
        "task_id='"+str(taskID)+"'", paramslist, 0)
    if recsToUpdate == "Records Updated":
        audit.logging.debug("Records "+str(taskID)+" updated successfully")
        return True
    else:
        audit.logging.error("Records "+str(taskID) +
                            " update status to "+closureStatus+" FAILED!")
        return False


def setTaskReset(taskID, taskStatus="New_Pending", note="N/A"):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info(
        "Closing Task ["+str(taskID)+"], setting to ["+taskStatus+"]...")
    paramslist = []
    param = ("closed_on", "NULL")
    paramslist.append(param)
    param = ("note", note)
    paramslist.append(param)
    param = ("batch_ID", "NULL")
    paramslist.append(param)
    statusID = taskdb.getID(
        tablename="TaskStatus", criteria="status_name = '"+taskStatus+"'", maxrecords=1)
    param = ("task_status", str(statusID))
    paramslist.append(param)
    recsToUpdate = taskdb.updateTasks(
        "task_id='"+str(taskID)+"'", paramslist, 0)
    if recsToUpdate == "Records Updated":
        audit.logging.debug("Records "+str(taskID)+" updated successfully")
        return True
    else:
        audit.logging.error("Records "+str(taskID) +
                            " update status to "+taskStatus+" FAILED!")
        return False


def getTaskActiveByBatchID(BatchID):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    sql = "Select * FROM atm.vw_tasks_active WHERE batch_id='"+BatchID+"'"
    queueRecords = taskdb.getCustomRecordList(sql)
    for r in queueRecords:
        audit.logging.debug("Retrieved batch record with ID: "+str(r[0]))
    return queueRecords


def getTaskActiveBatchIDs():
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    sql = "Select batch_id FROM atm.vw_tasks_active WHERE batch_id IS NOT NULL Group By batch_id"
    queueRecords = taskdb.getCustomRecordList(sql)
    for r in queueRecords:
        audit.logging.debug("Retrieved batch ID: "+str(r[0]))
    return queueRecords


def getTaskBatch(batchSize):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    date_string = f'{datetime.now():%Y-%m-%d_%H-%M-%S%z}'
    thisBatchId = "Batch_"+date_string
    audit.logging.debug("Batch ID: "+thisBatchId)

    validStatusIDs = taskdb.getRecords(
        "TaskStatus", "is_open=1 and is_hold=0 and is_error=0 and is_progress=0")

    statusIdList = ""
    separator = ""
    for ids in validStatusIDs:
        statusIdList += separator + str(ids[0])
        separator = ", "
        audit.logging.debug("Valid Status ID: "+str(ids[0])+" - "+str(ids[1]))
    audit.logging.debug("Batch Status ID List: "+statusIdList)

    param1 = ("batch_id", thisBatchId)
    paramslist = []
    paramslist.append(param1)
    recsToBatch = taskdb.updateTasks(
        "batch_id is NULL and task_status in ("+statusIdList+")", paramslist, batchSize)

    if recsToBatch == "Records Updated":
        queueRecords = taskdb.getRecords(
            "TaskQueue", "batch_id = '"+thisBatchId+"'", batchSize)

    audit.logging.debug("Queue Recs In This Batch")
    for r in queueRecords:
        audit.logging.debug(r)

    return queueRecords


def getPickList(listtype):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.print_subheading("Task " + listtype + " List")
    Records = taskdb.getRecords("Task" + listtype)

    for rec in Records:
        # print(rec[0], rec[1])
        print(rec)

    audit.print_line()

    return Records


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
