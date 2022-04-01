from tkinter import Y
import sys
import atm_logger as audit
import atm_taskdb as taskdb
import atm_common as common
from datetime import datetime


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
            audit.logging.info("\tID: "+str(batchrecs[0])+"\tStatus: "+batchrecs[1]+"\tTask Type: "+batchrecs[2])
        takeAction = "\tTake action on this batch?"
        actionAnswer = common.yes_or_no(takeAction)
        audit.logging.debug(takeAction + " :" + str(actionAnswer))
        if actionAnswer == True:
            cancelBatch = "\t\tCancel this batch?"
            cancelAnswer = common.yes_or_no(cancelBatch)
            audit.logging.debug(cancelBatch + " :" + str(cancelAnswer))
            if cancelAnswer == True:
                audit.logging.info("\t\t\tCancelling ["+r[0]+"]...")
                queueRecordsToUpdate = taskdb.getRecords("TaskQueue","batch_id = '"+r[0]+"'",0)
                audit.logging.debug("Cancelled records....")
                for upd in queueRecordsToUpdate:
                    audit.logging.debug(upd)
                    UpdTaskResult = setTaskClosed(upd[0],"Cancelled","Admin Cancelled")
                    if UpdTaskResult == True:
                        # Do more stuff here
                        audit.logging.info("Batch ["+r[0]+"] Cancelled")

            else:
                resetBatch = "\t\tReset this batch?"
                resetAnswer = common.yes_or_no(resetBatch)
                audit.logging.debug(resetBatch + " :" + str(resetAnswer))
                if resetAnswer == True:
                    audit.logging.info("\t\t\tResetting ["+r[0]+"]...")
                    queueRecordsToUpdate = taskdb.getRecords("TaskQueue","batch_id = '"+r[0]+"'",0)
                    audit.logging.debug("Cancelled records....")
                    for upd in queueRecordsToUpdate:
                        audit.logging.debug(upd)
                        UpdTaskResult = setTaskReset(upd[0],"New_Pending","Admin Reset")
                        if UpdTaskResult == True:
                            # Do more stuff here
                            audit.logging.info("Batch ["+r[0]+"] Reset")
        print("")


def setTaskClosed(taskID,closureStatus="Completed_Success",closureRef="N/A",closureID="N/A"):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info("Closing Task ["+str(taskID)+"], setting to ["+closureStatus+"]...")
    paramslist = []
    param = ("closed_on",str(datetime.now()))
    paramslist.append(param)
    param = ("closure_id",closureID)
    paramslist.append(param)
    param = ("closure_ref",closureRef)
    paramslist.append(param)
    statusID = taskdb.getID(tablename="TaskStatus", criteria="status_name = '"+closureStatus+"'", maxrecords=1)
    param = ("task_status",str(statusID))
    paramslist.append(param)
    recsToUpdate = taskdb.updateTasks("task_id='"+str(taskID)+"'",paramslist,0)
    if recsToUpdate == "Records Updated":
        audit.logging.debug("Records "+str(taskID)+" updated successfully")
        return True
    else:
        audit.logging.error("Records "+str(taskID)+" update status to "+closureStatus+" FAILED!")
        return False


def setTaskReset(taskID,taskStatus="New_Pending",note="N/A"):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info("Closing Task ["+str(taskID)+"], setting to ["+taskStatus+"]...")
    paramslist = []
    param = ("closed_on","NULL")
    paramslist.append(param)
    param = ("note",note)
    paramslist.append(param)
    param = ("batch_ID","NULL")
    paramslist.append(param)
    statusID = taskdb.getID(tablename="TaskStatus", criteria="status_name = '"+taskStatus+"'", maxrecords=1)
    param = ("task_status",str(statusID))
    paramslist.append(param)
    recsToUpdate = taskdb.updateTasks("task_id='"+str(taskID)+"'",paramslist,0)
    if recsToUpdate == "Records Updated":
        audit.logging.debug("Records "+str(taskID)+" updated successfully")
        return True
    else:
        audit.logging.error("Records "+str(taskID)+" update status to "+taskStatus+" FAILED!")
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


def getPickList(listtype):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.print_subheading("Task "+ listtype + " List")
    Records = taskdb.getRecords("Task" + listtype)

    for rec in Records:
        # print(rec[0], rec[1])
        print(rec)

    audit.print_line()
   
    return Records


