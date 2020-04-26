from importlib import reload as rl
import sys

def createFile(pyCode):
    strOfTemp = 'def main():\n\ttry:\n\t\treturn '
    endOfTemp = '\n\texcept SyntaxError as err:\n\t\treturn err\n\nif __name__ == \'__main__\':\n\tmain()'
    f = open("temp.py", "w+")
    f.write(strOfTemp + pyCode + endOfTemp)
    f.close()

    return executer()


def executer():

    try:
        import temp
        rl(temp)
        response = temp.main()
        return response
    except (ModuleNotFoundError, SyntaxError, UnboundLocalError) as err:
        if err is SyntaxError:
            str = 'Internal error code, load of temp file not performed. HINT: syntax error in temp.py'
            return str






        



