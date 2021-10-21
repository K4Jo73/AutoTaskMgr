import atm_logger as audit
import atm_taskdb as taskdb


def main():
    audit.setup_logging("./logs/")
    audit.print_heading('Automation Task Manager')
    audit.print_subheading("Task Status List")
    statusRecords = taskdb.getRecords("TaskStatus")

    for statusrec in statusRecords:
        print(statusrec[0], statusrec[1])


    audit.print_line()
    audit.print_subheading("Task Type List")
    typeRecords = taskdb.getRecords("TaskType")

    for typerec in typeRecords:
        print(typerec[0],typerec[1])


    audit.print_line()
    audit.print_subheading("Adding New Task")
    taskTypes = taskdb.getRecords(tablename="TaskType", criteria="type_name = 'DoThing'", maxrecords=1)

    for typerec in taskTypes:
        print(typerec)


    audit.print_line()
    audit.print_subheading("Task Queue List")
    QueueRecords = taskdb.getRecords("TaskQueuex","",4)

    for queuerec in QueueRecords:
        print(queuerec)


    audit.print_line()

    # taskdb.getTableColumns("task_queue")

    #ParamList
    param1 = ("source_ref","test record")
    param2 = ("source_id","abcde-12345-abcde-98765-ZYXWV")
    param3 = ("note","change that value on users account")
    param4 = ("activity_param01","John.Smith")
    param5 = ("activity_param02","thing to be changed")
    paramslist = []
    print(paramslist)
    paramslist.append(param1)
    paramslist.append(param2)
    paramslist.append(param3)
    paramslist.append(param4)
    paramslist.append(param5)

    audit.print_line()
    addtaskresult = taskdb.addTask("DoThing",paramslist)
    audit.logging.info("Added Task ID - " + str(addtaskresult))


    audit.print_subheading("Task Queue Record Detail")
    QueueRecords = taskdb.getRecords("TaskQueue", "task_id = " + str(addtaskresult))

    for queuerec in QueueRecords:
        print(queuerec)




    audit.print_line()
    addtaskresult = taskdb.addTask("DoThing")
    audit.logging.info("Added Task ID - " + str(addtaskresult))

    audit.print_subheading("Task Queue Record Detail")
    QueueRecords = taskdb.getRecords("TaskQueue", "task_id = " + str(addtaskresult))

    for queuerec in QueueRecords:
        print(queuerec)




print("script name is " + __name__)
if __name__ == "__main__":
    main()
