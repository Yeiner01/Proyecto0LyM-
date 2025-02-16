import re 

def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo .txt y lo devuelve como una cadena."""
    nombre_archivo += ".txt"  

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read().lower()  # Se convierte todo a minúsculas para normalizar
    except FileNotFoundError:
        return f"Error: El archivo '{nombre_archivo}' no existe."
    except Exception as e:
        return f"Ocurrió un error: {e}"  

def tokenizer(text):
    archivo = leer_archivo(text)
    
    keywords = {
        'move', 'turn', 'face', 'put', 'pick', 'jump', 'nop',
        'if', 'then', 'else', 'while', 'do', 'repeat', 'for',
        'canput', 'canpick', 'canmove', 'canjump', 'not', 'goto'
    }
    variable_declaration = re.compile(r'^\s*\|[a-z][a-zA-Z0-9\s,]*\|\s*$')
    procedure_declaration = re.compile(r'^\s*proc\s+[a-z][a-zA-Z0-9]*(:\s*[a-z][a-zA-Z0-9]*(\s*and:\s*[a-z][a-zA-Z0-9]*)*)?\s*\[\s*\]$')
    directions = {'#north', '#south', '#west', '#east', '#front', '#right', '#left', '#back', '#around'}
    types = {'#balloons', '#chips'}
    
    lines = archivo.split('\n')
    valid_tokens = {
        'KEYWORD': [],
        'VARIABLE_DECLARATION': [],
        'PROCEDURE_DECLARATION': [],
        'DIRECTION': [],
        'TYPE': [],
        'ASSIGNMENT': [],
        'CONDITION': [],
        'OPERATION': []
    }

    for line in lines:
        tokens = line.strip().split()
        if not tokens:
            continue
        
        if variable_declaration.match(line):
            valid_tokens['VARIABLE_DECLARATION'].append(tokens)
            continue
        if procedure_declaration.match(line):
            valid_tokens['PROCEDURE_DECLARATION'].append(tokens)
            continue
        
        if tokens[0] in keywords:
            valid_tokens['KEYWORD'].append(tokens)
        elif len(tokens) >= 3 and tokens[1] == ':=':
            valid_tokens['ASSIGNMENT'].append(tokens)
        elif len(tokens) >= 2 and tokens[0] == 'facing:' and tokens[1] in directions:
            valid_tokens['CONDITION'].append(tokens)
        elif len(tokens) >= 4 and tokens[2] == 'oftype:' and tokens[3] in types:
            valid_tokens['OPERATION'].append(tokens)
    
    return valid_tokens

def parser(valid_tokens):
    for token_type, tokens in valid_tokens.items():
        if token_type == "KEYWORD":
            for token in tokens:
                if token[0] in {"move", "turn", "face", "put", "pick", "jump", "nop"}:
                    if not parse_command(token):
                        raise SyntaxError(f"Comando inválido: {token}")
                elif token[0] in {"if", "while", "repeat", "goto"}:
                    if not parse_control_structure(token):
                        raise SyntaxError(f"Estructura de control inválida: {token}")
        elif token_type == "PROCEDURE_DECLARATION":
            for token in tokens:
                if not parse_procedure(token):
                    raise SyntaxError(f"Declaración de procedimiento inválida: {token}")
        elif token_type == "ASSIGNMENT":
            for token in tokens:
                if not parse_assignment(token):
                    raise SyntaxError(f"Asignación inválida: {token}")

def parse_command(token):
    return (token[0] == "move" and len(token) >= 2 and token[1].isdigit()) or \
           (token[0] == "turn" and len(token) >= 2 and token[1] in {"#left", "#right", "#around"}) or \
           (token[0] == "face" and len(token) >= 2 and token[1] in {'#north', '#south', '#west', '#east'}) or \
           (token[0] in {"put", "pick"} and len(token) >= 4 and token[2] == "oftype:" and token[3] in {'#balloons', '#chips'})

def parse_control_structure(token):
    return (token[0] == "if" and len(token) >= 4 and token[2] == "then") or \
           (token[0] == "while" and len(token) >= 3 and token[2] == "do") or \
           (token[0] == "repeat" and len(token) >= 3 and token[1] == "for") or \
           (token[0] == "goto" and len(token) >= 4 and token[2] == "with")

def parse_procedure(token):
    return len(token) >= 3 and token[0] == "proc" and token[1].isidentifier()

def parse_assignment(token):
    return len(token) >= 3 and token[1] == ":="
