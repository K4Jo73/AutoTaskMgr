import atm_logger as audit
import atm_taskdb as taskdb


def main():
    audit.setup_logging("./logs/")
    audit.print_heading('Automation Task Manager')
    audit.print_subheading("Task Status List")
    statusRecords = taskdb.getRecordList("TaskStatus")

    for statusrec in statusRecords:
        print(statusrec[1])

    audit.print_line()
    audit.print_subheading("Task Type List")
    typeRecords = taskdb.getRecordList("TaskType")

    for typerec in typeRecords:
        print(typerec[1])

    audit.print_line()




print ("script name is " + __name__)
if __name__ == "__main__":
    main()



