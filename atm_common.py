import sys
import atm_logger as audit

print("script name is " + __name__)


def yes_or_no(question, default_no=True):
    audit.logging.debug("["+sys._getframe().f_code.co_name+"]")
    choices = ' [y/N]: ' if default_no else ' [Y/n]: '
    default_answer = 'n' if default_no else 'y'
    reply = str(input(question + choices)).lower().strip() or default_answer
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False if default_no else True



