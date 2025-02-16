import re

def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo .txt y lo devuelve como una cadena."""
    nombre_archivo += ".txt"  

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
        'canPut', 'canPick', 'canMove', 'canJump', 'not', 'goto'
    }
    variable_declaration = re.compile(r'^\s*\|[a-z][a-zA-Z0-9]*(\s*,\s*[a-z][a-zA-Z0-9]*)*\|\s*$')
    procedure_declaration = re.compile(r'^\s*proc\s+[a-z][a-zA-Z0-9]*:\s*[a-z][a-zA-Z0-9]*(\s*and:\s*[a-z][a-zA-Z0-9]*)*\s*\[\s*\]$')
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
        'OPERATION': [],
        'COMMA': [],  # Nueva categoría para comas
        'OTHER': []
    }

    for line in lines:
        tokens = re.findall(r':=|\w+|\S', line.strip())  # Usamos regex para capturar comas y otros tokens
        if not tokens:
            continue
        
        if variable_declaration.match(line):
            valid_tokens['VARIABLE_DECLARATION'].append(tokens)
            continue
        if procedure_declaration.match(line):
            valid_tokens['PROCEDURE_DECLARATION'].append(tokens)
            continue
        
        # Verificar si el primer token es una palabra clave
        if len(tokens) > 0 and tokens[0] in keywords:
            if tokens[0] == 'goto:':
                if len(tokens) >= 4 and tokens[2] == 'with:':
                    valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] == 'move:':
                if len(tokens) >= 2:
                    valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] == 'turn:':
                if len(tokens) >= 2 and tokens[1] in {'#left', '#right', '#around'}:
                    valid_tokens['DIRECTION'].append(tokens)
            elif tokens[0] == 'face:':
                if len(tokens) >= 2 and tokens[1] in directions:
                    valid_tokens['DIRECTION'].append(tokens)
            elif tokens[0] in {'put:', 'pick:'}:
                if len(tokens) >= 4 and tokens[2] == 'ofType:' and tokens[3] in types:
                    valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] == 'if:':
                if len(tokens) >= 4 and tokens[2] == 'then:':
                   valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] == 'while:':
                if len(tokens) >= 3 and tokens[2] == 'do:':
                    valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] == 'repeat:':
                if len(tokens) >= 3 and tokens[1] == 'for:':
                    valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] in {'canPut:', 'canPick:', 'canMove:', 'canJump:'}:
                if len(tokens) >= 4 and tokens[2] == 'ofType:' and tokens[3] in types:
                    valid_tokens['KEYWORD'].append(tokens)
            elif tokens[0] == 'not:':
                if len(tokens) >= 2:
                    valid_tokens['KEYWORD'].append(tokens)
        
        elif len(tokens) >= 3 and tokens[1] == ':=': # Verifica si es una asignación de variable
            valid_tokens['ASSIGNMENT'].append(tokens)

        elif len(tokens) >= 2 and tokens[0] == 'facing:' and tokens[1] in directions: # Verifica si es una condición de dirección
            valid_tokens['CONDITION'].append(tokens)
        
        elif len(tokens) >= 4 and tokens[2] == 'ofType:' and tokens[3] in types: # Verifica si es una operación con tipos
            valid_tokens['OPERATION'].append(tokens)
        
        elif ',' in tokens:  # Captura las comas
            valid_tokens['COMMA'].append(tokens)
        
        else:
            valid_tokens['OTHER'].append(tokens)
    
    return valid_tokens

def parser(valid_tokens):
    for token_type, tokens in valid_tokens.items():
        if token_type == "KEYWORD":
            for token in tokens:
                if len(token) > 0 and token[0] in {"move", "turn", "face", "put", "pick", "jump", "nop"}:
                    if not parse_command(token):
                        return False
                elif len(token) > 0 and token[0] in {"if", "while", "repeat"}:
                    if not parse_control_structure(token):
                        return False
        elif token_type == "PROCEDURE_DECLARATION":
            for token in tokens:
                if not parse_procedure(token):
                    return False
        elif token_type == "ASSIGNMENT":
            for token in tokens:
                if not parse_assignment(token):
                    return False
        elif token_type == "OTHER":
            return False
    return True

def parse_command(token):
    if len(token) >= 2 and token[0] == "move" and token[1].isdigit():
        return True
    elif len(token) >= 2 and token[0] == "turn" and token[1] in {"#left", "#right", "#around"}:
        return True
    elif len(token) >= 2 and token[0] == "face" and token[1] in {'#north', '#south', '#west', '#east'}:
        return True
    elif len(token) >= 4 and token[0] in {"put", "pick"} and token[2] == "ofType:" and token[3] in {'#balloons', '#chips'}:
        return True
    return False

def parse_control_structure(token):
    if len(token) >= 4 and token[0] == "if" and token[2] == "then":
        return True
    elif len(token) >= 3 and token[0] == "while" and token[2] == "do":
        return True
    elif len(token) >= 3 and token[0] == "repeat" and token[1] == "for":
        return True
    return False

def parse_procedure(token):
    if len(token) >= 3 and token[0] == "proc" and token[1].isidentifier():
        return True
    return False

def parse_assignment(token):
    if len(token) >= 3 and token[1] == ":=":
        return True
    return False
