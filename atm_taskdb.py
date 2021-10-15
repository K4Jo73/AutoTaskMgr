import logging
import sys
import mysql.connector
# run this in cmd or Powershell to install 
# python -m pip install mysql-connector-python
print ("script name is " + __name__)

def connectDb():
    db = mysql.connector.connect(
    host="localhost",
    user="atmapp",
    password="SnakeCodeWin12",
    database="atm"
    )
    # print(db)
    return db


def getRecordList(WhatToGet):
    dbConnector = connectDb()
    datacursor = dbConnector.cursor()
    sql = getListSQL(WhatToGet)
    datacursor.execute(sql)
    records = datacursor.fetchall()
    logging.debug(WhatToGet + " list query returned " + str(datacursor.rowcount) + " rows")
    return records


def getListSQL(WhatToGet):
    match WhatToGet:
        case "TaskStatus":
            script = "SELECT * FROM atm.task_status;"
        case "TaskType":
            script = "SELECT * FROM atm.task_type;"
        case _:
            script = "SELECT 'Invalid List Type Provided [" + WhatToGet + "]';"
    logging.debug(WhatToGet + " script: " + script)
    return script



# def getTaskStatusList():
#     dbConnector = connectDb()
#     datacursor = dbConnector.cursor()
#     datacursor.execute("SELECT * FROM atm.task_status;")
#     records = datacursor.fetchall()
#     logging.debug("Task Status list query returned " + str(datacursor.rowcount) + " rows")
#     return records


# def getTaskTypeList():
#     dbConnector = connectDb()
#     datacursor = dbConnector.cursor()
#     datacursor.execute("SELECT * FROM atm.task_type;")
#     records = datacursor.fetchall()
#     logging.debug("Task Type list query returned " + str(datacursor.rowcount) + " rows")
#     return records



