import atm_logger as audit
import atm_taskdb as taskdb


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
    # getSomeTasks(10)







def getSomeTasks(howmany):
    audit.print_subheading("Task Queue List Sample")
    QueueRecords = taskdb.getRecords("TaskQueue","",howmany)

    for queuerec in QueueRecords:
        print(queuerec)

    return QueueRecords


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
