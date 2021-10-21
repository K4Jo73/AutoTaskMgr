import logging
import sys
import mysql.connector
# run this in cmd or Powershell to install
# python -m pip install mysql-connector-python
print("script name is " + __name__)

schemaname = "atm"

def connectDb():
    db = mysql.connector.connect(
        host="localhost",
        user="atmapp",
        password="SnakeCodeWin12",
        database=schemaname
    )
    # print(db)
    return db


def getRecords(tablename, criteria="", maxrecords=0):
    try:
        dbConnector = connectDb()
        datacursor = dbConnector.cursor()
        sql = getListSQL(tablename, criteria, maxrecords)
        # logging.debug(tablename + " filtered script: " + sql)
        datacursor.execute(sql)
        records = datacursor.fetchall()
        logging.debug(tablename + " record query returned " +
                  str(datacursor.rowcount) + " rows")
        return records

    except BaseException as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        # raise


def getListSQL(tablename, criteria="", maxrecords=0):
    
    script = "SELECT * FROM " + schemaname

    match tablename:
        case "TaskStatus":
            script += ".task_status"
        case "TaskType":
            script += ".task_type"
        case "TaskQueue":
            script += ".task_queue"
        case _:
            script = "SELECT 'Invalid List Type Provided [" + tablename + "]';"
            return script

    if criteria != "":
        script += " WHERE " + criteria

    if maxrecords != 0:
        script += " limit " + str(maxrecords)

    logging.debug(tablename + " script: " + script)

    return script


def getTableColumns(tablename):
    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = '" + tablename + "' ;"
    logging.debug(sql)
    dbConnector = connectDb()
    datacursor = dbConnector.cursor()
    datacursor.execute(sql)
    records = datacursor.fetchall()
    for rec in records:
        print(rec[0])



def getID(tablename, criteria="", maxrecords=0):
    allrecs = getRecords(tablename, criteria, maxrecords)
    for rec in allrecs:
        logging.debug(tablename + " - " + criteria + " - RETURNED RECORD: " + str(rec))
        return rec[0]


def addTask(tasktype,paramlist=None):
    if paramlist is not None:
        logging.info("Received parameters:")
        for p in paramlist:
            logging.info("\tProperty:" + p[0] + "\t\t" + "Value:" + p[1])

    print("Getting TypeID")
    typeID = getID(tablename="TaskType", criteria="type_name = '" + tasktype + "'", maxrecords=1)
    logging.debug("TaskType:" + tasktype + " ID:" + str(typeID))
    if typeID is None:
        logging.error("NO TASK TYPE RECORD FOUND!")
        return "Failed - Bad Type ID"
    else:
        print("Getting StatusID")
        statusID = getID(tablename="TaskStatus", criteria="status_name = 'New_Pending'", maxrecords=1)
        logging.debug("TaskType:" + tasktype + " ID:" + str(statusID))
        if statusID is None:
            logging.error("NO TASK STATUS RECORD FOUND!")
            return "Failed - Bad Status ID"
        else:
            separator = ","
            colnames = "task_type,task_status"
            colvalues = str(typeID) + separator + str(statusID)
            if paramlist is not None:
                for param in paramlist:
                    colnames += separator + param[0]
                    colvalues += separator + "'" + param[1] + "'"
            # sql = "SET autocommit = ON; "
            sql = "INSERT INTO " + schemaname + ".task_queue (" + colnames + ") VALUES (" + colvalues + ") "
            sql2 = "SELECT LAST_INSERT_ID(); "
            logging.debug(sql)
            try:
                dbConnector = connectDb()
                datacursor = dbConnector.cursor()
                # datacursor.execute(sql,multi=True)
                datacursor.execute(sql)
                """ RATHER THAN DO A MULTI LINE - RUN A SECOND EXECUTE TO GET THE ID """
                dbConnector.commit()
                datacursor2 = dbConnector.cursor()
                datacursor2.execute(sql2)
                records = datacursor2.fetchall()
                id=0
                for rec in records:
                    id = rec[0]
                    break
                dbConnector.commit()
                return id

            except BaseException as err:
                logging.error(f"Unexpected {err=}, {type(err)=}")
                # raise
                return "Error Saving New Task"


#     INSERT INTO `atm`.`task_queue`
# (`task_id`,
# `created_on`,
# `updated_on`,
# `note`,
# `task_type`,
# `task_status`)
# VALUES
# (<{task_id: }>,
# <{created_on: CURRENT_TIMESTAMP}>,
# <{updated_on: CURRENT_TIMESTAMP}>,
# <{note: }>,
# <{task_type: }>,
# <{task_status: }>);
