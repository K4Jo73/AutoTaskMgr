import atm_logger as audit
import atm_taskdb as taskdb

audit.setup_logging("./logs/")

audit.logging.info('_' * 50)
audit.logging.info(' ' * 50)
audit.logging.info(' ' * 13 + 'Automation Task Manager' + ' ' * 14)
audit.logging.info('_' * 50)
# audit.logging.info('\n' * 2)
# audit.logging.debug("debug test message")
# audit.logging.warning("warning test message")
# audit.logging.error("error test message")
# audit.logging.critical("critical test message")
# audit.logging.info('\n' * 2)
# audit.logging.info('_' * 50)



print()
print("Task Status List")
print("=" * 15)

# statusRecords = taskdb.getTaskStatusList()
statusRecords = taskdb.getRecordList("TaskStatus")

for statusrec in statusRecords:
    print(statusrec[1])

print()
print("Task Type List")
print("=" * 15)

# typeRecords = taskdb.getTaskTypeList()
typeRecords = taskdb.getRecordList("TaskType")

for typerec in typeRecords:
    print(typerec[1])


print()
