import re 




def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo .txt y lo devuelve como una cadena."""
    nombre_archivo += ".txt"  

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read().lower()   #se convierte todo a minusculas
    except FileNotFoundError:
        return f"Error: El archivo '{nombre_archivo}' no existe."
    except Exception as e:
        return f"Ocurrió un error: {e}"  
def tokenizer(text):
    archivo = leer_archivo(text)
    
    lines = archivo.split('\n')
    token_list = []
    
    for line in lines :
        tokens = line.strip().split()
        if tokens:
            token_list.append(tokens)
    return token_list



def parser(tokens):
    token_list = tokenizer(tokens)
    keywords = {
        'move', 'turn', 'face', 'put', 'pick', 'jump', 'nop',
        'if', 'then', 'else', 'while', 'do', 'repeat', 'for',
        'canPut', 'canPick', 'canMove', 'canJump', 'not', 'goTo'
    }
    variable_declaration = re.compile(r'^\s*\|[a-z][a-zA-Z0-9]*(\s*, \s*[a-z][a-zA-Z0-9]*)*\|\s*$')
    procedure_declaration = re.compile(r'^\s*proc\s+[a-z][a-zA-Z0-9]*:\s*[a-z][a-zA-Z0-9]*(\s*and:\s*[a-z][a-zA-Z0-9]*)*\s*\[\s*\]$')
    directions = {'#north', '#south', '#west', '#east', '#front', '#right', '#left', '#back', '#around'}
    types = {'#balloons', '#chips'}
            
    for linea in token_list:
        linea1 = ''.join(linea)
        if variable_declaration.match(linea1): #una idea: si cumple con las condiciones se va eleminando de la lista
            token_list.remove(linea)
        elif procedure_declaration.match(linea1):
            token_list.remove(linea)
        elif linea[0] == 'goTo:':
            if len(linea) >= 4 and linea[2] == 'with:':
                token_list.remove(linea)
        elif linea[0] == 'move:':
            if len(linea) >= 2:
                token_list.remove(linea)
        elif linea[0] == 'turn:':
            if len(linea) >= 2 and linea[1] in {'#left', '#right', '#around'}:
                token_list.remove(linea)
        elif linea[0] == 'face:':
            if len(linea) >= 2 and linea[1] in directions:
                token_list.remove(linea)
        elif linea[0] == 'put:' or linea[0] == 'pick:':
            if len(linea) >= 4 and linea[2] == 'ofType:' and linea[3] in types:
                token_list.remove(linea)
        elif linea[0] == 'if:':
            if len(linea) >= 4 and linea[2] == 'then:':
                token_list.remove(linea)
        elif linea[0] == 'while:':
            if len(linea) >= 3 and linea[2] == 'do:':
                token_list.remove(linea)
        elif linea[0] == 'repeat:':
            if len(linea) >= 3 and linea[1] == 'for:':
                token_list.remove(linea)
        elif linea[0] == 'canPut:' or linea[0] == 'canPick:' or linea[0] == 'canMove:' or linea[0] == 'canJump:':
            if len(linea) >= 4 and linea[2] == 'ofType:' and tokens[3] in types:
                token_list.remove(linea)
        elif linea[0] == 'not:':
            if len(linea) >= 2:
                token_list.remove(linea)
        elif len(linea) >= 2 and linea[0] == 'facing:' and linea[1] in directions:
            token_list.remove(linea)
    if len(token_list) == 0:
        return True
    return False

