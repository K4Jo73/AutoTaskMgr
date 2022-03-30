from tkinter import Y
import atm_logger as audit
import atm_taskdb as taskdb
import atm_common as common
from datetime import datetime


print("script name is " + __name__)


def listActiveBatches():
    ActiveBatches = getTaskActiveBatchIDs()
    # audit.logging.info(ActiveBatches)
    audit.logging.info("Current active batches....")
    print("")
    for r in ActiveBatches:
        # audit.logging.info(r[0])
        audit.logging.info(r[0])
    

def manageActiveBatches():
    ActiveBatches = getTaskActiveBatchIDs()
    # audit.logging.info(ActiveBatches)
    audit.logging.info("Current active batches to manage....")
    print("")
    for r in ActiveBatches:
        audit.logging.info(r[0])
        recordsForBatch = getTaskActiveByBatchID(r[0])
        for batchrecs in recordsForBatch:
            audit.logging.info("\tID: "+str(batchrecs[0])+"\tStatus: "+batchrecs[1]+"\tTask Type: "+batchrecs[2])
        # audit.logging.info(r[0])
        takeAction = "\tTake action on this batch?"
        actionAnswer = common.yes_or_no(takeAction)
        audit.logging.debug(takeAction + " :" + str(actionAnswer))
        if actionAnswer == True:
            cancelBatch = "\t\tCancel this batch?"
            cancelAnswer = common.yes_or_no(cancelBatch)
            audit.logging.debug(cancelBatch + " :" + str(cancelAnswer))
            if cancelAnswer == True:
                audit.logging.info("\t\t\tCancelling ["+r[0]+"]...")
                paramslist = []
                param = ("closed_on",str(datetime.now()))
                paramslist.append(param)
                param = ("closure_id","N\A")
                paramslist.append(param)
                param = ("closure_ref","Admin Cancelled")
                paramslist.append(param)
                statusID = taskdb.getID(tablename="TaskStatus", criteria="status_name = 'Cancelled'", maxrecords=1)
                param = ("task_status",str(statusID))
                paramslist.append(param)
                recsToUpdate = taskdb.updateTasks("batch_id='"+r[0]+"'",paramslist,0)
                if recsToUpdate == "Records Updated":
                    queueRecordsUpdated = taskdb.getRecords("TaskQueue","batch_id = '"+r[0]+"'",0)
                    audit.logging.debug("Cancelled records....")
                    for upd in queueRecordsUpdated:
                        audit.logging.debug(upd)

            else:
                resetBatch = "\t\tReset this batch?"
                resetAnswer = common.yes_or_no(resetBatch)
                audit.logging.debug(resetBatch + " :" + str(resetAnswer))
                if resetAnswer == True:
                    audit.logging.info("\t\t\tResetting ["+r[0]+"]...")
        print("")




def getTaskActiveByBatchID(BatchID):
    queueRecords = taskdb.getCustomRecordList("Select * FROM atm.vw_tasks_active WHERE batch_id='"+BatchID+"'")
    for r in queueRecords:
        audit.logging.debug(r[0])
    return queueRecords


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



def getPickList(listtype):
    audit.print_subheading("Task "+ listtype + " List")
    Records = taskdb.getRecords("Task" + listtype)

    for rec in Records:
        # print(rec[0], rec[1])
        print(rec)

    audit.print_line()
   
    return Records
