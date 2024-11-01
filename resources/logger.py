from colorama import Fore

DEBUG_MODE = False

def log(msg, context, severity = "default"): 
    '''
        Severity possible values:
            - default: color BLACK; 
            - info: color CYAN; 
            - warning: color YELLOW; 
            - error: color RED; 

    '''

    color = Fore.WHITE

    if severity == "info": 
        color = Fore.BLUE
    elif severity == "warning": 
        color = Fore.YELLOW
    elif severity == "error": 
        color = Fore.RED

    if not DEBUG_MODE:
        print(color + f"\n[{context}] {msg}" + Fore.RESET)
        


if __name__ == "__main__": 
    log("HELLO WORLD", "error")