from colorama import Fore



def log(msg, severity = "default"): 
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

    print(color + msg + Fore.RESET)
        


if __name__ == "__main__": 
    log("HELLO WORLD", "error")