import os
import time
import inspect

def debug_print(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    caller_function = inspect.stack()[1][3]
    formatted_message = f"\033[1;30;40m{timestamp}\033[1;33;40m DEBUG    \033[1;30;40m{caller_function}() \033[1;37;00m{message}"
    print(formatted_message)

# Example usage
# debug_print("This is a debug message.")
