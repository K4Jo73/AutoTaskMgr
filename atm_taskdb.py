import sys
from datetime import datetime

import mysql.connector

import atm_logger as audit

# */99+* run this in cmd or Powershell to install
# * python -m pip install mysql-connector-python
print("script name is " + __name__)
# audit.logging.info("script name is " + __name__)

schemaname = "atm"


def getCustomRecordList(sql):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    try:
        records = runDbSelect(sql)
        return records

    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}")
        # raise


def listRecords(tablename, criteria="", maxrecords=0):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    try:
        cols = getTableColumns(tablename)
        audit.logging.debug("Columns: "+str(cols))
        results = getRecords(tablename, criteria, maxrecords)
        audit.logging.debug("Results: "+str(results))
        for result in results:
            print("")
            for col, val in zip(cols, result):
                audit.logging.info(str(col[0])+": "+str(val))

    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}")
        # raise


def getRecords(tablename, criteria="", maxrecords=0):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    try:
        sql = getListSQL(tablename, criteria, maxrecords)
        records = runDbSelect(sql)
        return records

    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}")
        # raise


def resolveTableName(tablename):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    match tablename:
        case "TaskStatus":
            trueTableName = "task_status"
        case "TaskType":
            trueTableName = "task_type"
        case "TaskQueue":
            trueTableName = "task_queue"
        case "TasksActive":
            trueTableName = "vw_tasks_active"
        case "TasksClosed":
            trueTableName = "vw_tasks_closed"
        case "TasksHold":
            trueTableName = "vw_tasks_hold"
        case "TasksError":
            trueTableName = "vw_tasks_error"
        case "Menus":
            trueTableName = "menu_header"
        case "MenuOptions":
            trueTableName = "menu_options"
        case "MenuOptionParams":
            trueTableName = "vw_menu_option_params"
        case _:
            trueTableName = "INVALID"
            # trueTableName = "SELECT 'Invalid List Type Provided [" + \
            #     tablename + "]';"

    return trueTableName


def getListSQL(tablename, criteria="", maxrecords=0, isselect=1):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    script = ""

    if isselect == 1:
        script = "SELECT * FROM " + schemaname

    script += "." + resolveTableName(tablename)

    if criteria != "":
        script += " WHERE " + criteria

    if maxrecords != 0:
        script += " limit " + str(maxrecords)

    audit.logging.debug(tablename + " script: " + script)

    return script


def getTableColumns(tablename):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")

    tbl = resolveTableName(tablename)
    audit.logging.debug(
        "Provided tablename ["+tablename+"] resolved to ["+tbl+"]")

    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = '" + \
        tbl + "' ;"
    audit.logging.debug("SQL: "+sql)

    records = runDbSelect(sql)
    for rec in records:
        # print(rec[0])
        audit.logging.debug(rec[0])
    return records


def getID(tablename, criteria="", maxrecords=1):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    allrecs = getRecords(tablename, criteria, maxrecords)
    for rec in allrecs:
        audit.logging.debug(tablename + " - " + criteria +
                            " - RETURNED RECORD: " + str(rec))
        return rec[0]


def updateTasks(criteria, paramlist, maxrecords):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.info("Received parameters:")
    UpdateList = ""
    listSeparator = ""
    for p in paramlist:
        audit.logging.info("\tProperty:" + p[0] + "\t\t" + "Value:" + p[1])
        if p[1] != "NULL":
            UpdateList += listSeparator+p[0]+" = '"+p[1]+"'"
        else:
            UpdateList += listSeparator+p[0]+" = NULL"
        listSeparator = ","
    audit.logging.info("Received Criteria: "+criteria)
    audit.logging.info("SET String: "+UpdateList)

    UpdateList += listSeparator+"updated_on='"+str(datetime.now())+"'"
    audit.logging.debug("Generated Update List:"+UpdateList)

    sql = getListSQL("TaskQueue", criteria, maxrecords, isselect=0)
    sql = "UPDATE "+schemaname+".task_queue SET "+UpdateList+" "+sql
    runDbUpdate(sql)
    return "Records Updated"


def addTask(tasktype, paramlist=None):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    if paramlist is not None:
        audit.logging.info("Received parameters:")
        for p in paramlist:
            audit.logging.info("\tProperty:" + p[0] + "\t\t" + "Value:" + p[1])

    audit.logging.info("Getting TypeID")
    typeID = getID(tablename="TaskType",
                   criteria="type_name = '" + tasktype + "'", maxrecords=1)
    audit.logging.debug("TaskType:" + tasktype + " ID:" + str(typeID))
    if typeID is None:
        audit.logging.error("NO TASK TYPE RECORD FOUND!")
        return "Failed - Bad Type ID"
    else:
        audit.logging.info("Getting StatusID")
        statusID = getID(tablename="TaskStatus",
                         criteria="status_name = 'New_Pending'", maxrecords=1)
        audit.logging.debug("StatusName:'New_Pending' ID:" + str(statusID))
        if statusID is None:
            audit.logging.error("NO TASK STATUS RECORD FOUND!")
            return "Failed - Bad Status ID"
        else:
            separator = ","
            colnames = "task_type,task_status"
            colvalues = str(typeID) + separator + str(statusID)
            if paramlist is not None:
                for param in paramlist:
                    colnames += separator + param[0]
                    colvalues += separator + "'" + param[1] + "'"
            sql1 = "INSERT INTO " + schemaname + \
                ".task_queue (" + colnames + ") VALUES (" + colvalues + ") "
            audit.logging.debug("script: "+sql1)
            try:
                records = runDbAdd(sql1)
                id = 0
                for rec in records:
                    id = rec[0]
                    break
                return id

            except BaseException as err:
                audit.logging.error(
                    sys._getframe().f_code.co_name + f" - Unexpected {err=}, {type(err)=}")
                # raise
                return "Error Saving New Task"


def addType(typename, description):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    sql1 = "INSERT INTO " + schemaname + \
        ".task_type (type_name,type_desc,type_active) VALUES ('" + \
        typename + "','" + description + "',1) "
    audit.logging.debug("script: "+sql1)
    try:
        records = runDbAdd(sql1)
        id = 0
        for rec in records:
            id = rec[0]
            break
        return id

    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}")
        # raise
        return "Error Saving New Task Type"


def addStatus(statusname, description, isOpen=1, isHold=0, isError=0):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    sql1 = "INSERT INTO " + schemaname + \
        ".task_status (status_name,status_desc,status_active,is_open,is_hold,is_error) "
    sql1 += " VALUES ('" + statusname + "','" + description + "',1," + \
        str(isOpen) + "," + str(isHold) + "," + str(isError) + " ) "
    audit.logging.debug("script: "+sql1)
    try:
        records = runDbAdd(sql1)
        id = 0
        for rec in records:
            id = rec[0]
            break
        return id

    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}")
        # raise
        return "Error Saving New Task Status"


def connectDb():
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    db = mysql.connector.connect(
        host="localhost",
        user="atmapp",
        password="SnakeCodeWin12",
        database=schemaname
    )
    # print(db)
    return db


def runDbAdd(sql):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.debug(sql)
    try:
        dbConnector = connectDb()
        datacursor = dbConnector.cursor()
        audit.logging.debug("script: "+sql)
        datacursor.execute(sql)
        dbConnector.commit()
        sql2 = "SELECT LAST_INSERT_ID(); "
        datacursor2 = dbConnector.cursor()
        datacursor2.execute(sql2)
        records = datacursor2.fetchall()
        audit.logging.debug("Record query added " +
                            str(datacursor.rowcount) + " rows")
        dbConnector.commit()
        return records
    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}\n"+sql)


def runDbUpdate(sql):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.debug("script: "+sql)
    try:
        dbConnector = connectDb()
        datacursor = dbConnector.cursor()
        datacursor.execute(sql)
        audit.logging.debug("Record query updated " +
                            str(datacursor.rowcount) + " rows")
        dbConnector.commit()
    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}\n"+sql)


def runDbSelect(sql):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    audit.logging.debug("script: "+sql)
    try:
        dbConnector = connectDb()
        datacursor = dbConnector.cursor()
        datacursor.execute(sql)
        records = datacursor.fetchall()
        audit.logging.debug("Record query returned " +
                            str(datacursor.rowcount) + " rows")
        dbConnector.commit()
        return records
    except BaseException as err:
        audit.logging.error(sys._getframe().f_code.co_name +
                            f" - Unexpected {err=}, {type(err)=}\n"+sql)
