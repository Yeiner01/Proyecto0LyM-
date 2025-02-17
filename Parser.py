import re 




def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo .txt y lo devuelve como una cadena."""
    nombre_archivo += ".txt"  

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read()   #se convierte todo a minusculas
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
        for token in linea:
            if token[0] in keywords:
                if not parse_command(token):
                    raise SyntaxError(f"Comando inválido: {token}")
            elif token[0] in {"if", "while", "repeat"}:
                if not parse_control_structure(token):
                    raise SyntaxError(f"Estructura de control inválida: {token}")
            elif variable_declaration.match(token):
                if not parse_assignment(token):
                    raise SyntaxError(f"Declaración de variable inválida: {token}")
            elif procedure_declaration.match(token):
                if not parse_procedure(token):
                    raise SyntaxError(f"Declaración de procedimiento inválida: {token}")
        elif token_type == "ASSIGNMENT":
            for token in tokens:
                if not parse_assignment(token):
                    raise SyntaxError(f"Asignación inválida: {token}")

def parse_command(token):
    if token[0] == "move" and len(token) >= 2 and token[1].isdigit():
        return True
    elif token[0] == "turn" and len(token) >= 2 and token[1] in {"#left", "#right", "#around"}:
        return True
    elif token[0] == "face" and len(token) >= 2 and token[1] in {'#north', '#south', '#west', '#east'}:
        return True
    elif token[0] in {"put", "pick"} and len(token) >= 4 and token[2] == "ofType:" and token[3] in {'#balloons', '#chips'}:
        return True
    return False

def parse_control_structure(token):
    if token[0] == "if:" and len(token) >= 4 and token[2] == "then":
        return True
    elif token[0] == "while:" and len(token) >= 3 and token[2] == "do":
        return True
    elif token[0] == "repeat:" and len(token) >= 3 and token[1] == "for":
        return True
    return False

def parse_procedure(token):
    if len(token) >= 3 and token[0] == "proc:" and token[1].isidentifier():
        return True
    return False

def parse_assignment(token):
    if len(token) >= 3 and token[1] == ":=":
        return True
    return False





