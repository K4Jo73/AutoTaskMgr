import atm_logger as audit

audit.setup_logging("./logs/")

audit.logging.info('_' * 50)
audit.logging.info(' ' * 50)
audit.logging.info(' ' * 13 + 'Automation Task Manager' + ' ' * 14)
audit.logging.info('_' * 50)
# audit.logging.info('\n' * 2)
audit.logging.debug("debug test message")
audit.logging.warning("warning test message")
audit.logging.error("error test message")
audit.logging.critical("critical test message")
audit.logging.info('\n' * 2)
audit.logging.info('_' * 50)




