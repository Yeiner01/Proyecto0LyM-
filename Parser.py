import re 
import ro



def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo .txt y lo devuelve como una cadena."""
    nombre_archivo += "ejemplo.txt"  

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        return f"Error: El archivo '{nombre_archivo}' no existe."
    except Exception as e:
        return f"Ocurrió un error: {e}"  
def tokenizer(text):
    archivo = leer_archivo(text)
    keywords = {
        'move', 'turn', 'face', 'put', 'pick', 'jump', 'nop',
        'if', 'then', 'else', 'while', 'do', 'repeat', 'for',
        'canPut', 'canPick', 'canMove', 'canJump', 'not', 'goto', "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    }
    variable_declaration = re.compile(r'^\s*\|[a-z][a-zA-Z0-9]*(\s*[a-z][a-zA-Z0-9]*)*\|\s*$')
    procedure_declaration = re.compile(r'^\s*proc\s+[a-z][a-zA-Z0-9]*:\s*[a-z][a-zA-Z0-9]*(\s*and:\s*[a-z][a-zA-Z0-9]*)*\s*\[\s*\]$')
    directions = {'#north', '#south', '#west', '#east', '#front', '#right', '#left', '#back', '#around'}
    types = {'#balloons', '#chips'}
    
    lines = archivo.split('\n')
    valid_tokens = []

    
    for line in lines:
        tokens = line.strip().split()
        if not tokens:
            continue
        
        
        if tokens[0] in keywords:
            if tokens[0] == 'goto:':
                if len(tokens) >= 4 and tokens[2] == 'with:':
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'move:':
                if len(tokens) >= 2:
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'turn:':
                if len(tokens) >= 2 and tokens[1] in {'#left', '#right', '#around'}:
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'face:':
                if len(tokens) >= 2 and tokens[1] in directions:
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'put:' or tokens[0] == 'pick:':
                if len(tokens) >= 4 and tokens[2] == 'ofType:' and tokens[3] in types:
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'if:':
                if len(tokens) >= 4 and tokens[2] == 'then:':
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'while:':
                if len(tokens) >= 3 and tokens[2] == 'do:':
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'repeat:':
                if len(tokens) >= 3 and tokens[1] == 'for:':
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'canPut:' or tokens[0] == 'canPick:' or tokens[0] == 'canMove:' or tokens[0] == 'canJump:':
                if len(tokens) >= 4 and tokens[2] == 'ofType:' and tokens[3] in types:
                    valid_tokens.extend(tokens)
            elif tokens[0] == 'not:':
                if len(tokens) >= 2:
                    valid_tokens.extend(tokens)
        
        elif len(tokens) >= 3 and tokens[1] == ':=': #Verifica si es una asignación de variable
            valid_tokens.extend(tokens)

        
        elif len(tokens) >= 2 and tokens[0] == 'facing:' and tokens[1] in directions: # Verifica si es una condición de dirección
            valid_tokens.extend(tokens)
        
        elif len(tokens) >= 4 and tokens[2] == 'ofType:' and tokens[3] in types: # Verifica si es una operación con tipos
            valid_tokens.extend(tokens)
    
    return valid_tokens



    
    for line in lines:
        tokens = line.strip().split()

        if tokens.startswith('|') and tokens.endswith('|'):
            valid_tokens.extend(tokens)
            continue