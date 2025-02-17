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
            
            
    lines_to_remove = []

    for i, linea in enumerate(token_list):
        linea1 = ''.join(linea)

        if variable_declaration.match(linea1) or procedure_declaration.match(linea1):
            lines_to_remove.append(i)
        elif linea[0] == 'goTo:' and len(linea) >= 4 and linea[2] == 'with:':
            lines_to_remove.append(i)
        elif linea[0] == 'move:' and len(linea) >= 2:
            lines_to_remove.append(i)
        elif linea[0] == 'turn:' and len(linea) >= 2 and linea[1] in {'#left', '#right', '#around'}:
            lines_to_remove.append(i)
        elif linea[0] == 'face:' and len(linea) >= 2 and linea[1] in directions:
            lines_to_remove.append(i)
        elif linea[0] in {'put:', 'pick:'} and len(linea) >= 4 and linea[2] == 'ofType:' and linea[3] in types:
            lines_to_remove.append(i)
        elif linea[0] == 'if:' and len(linea) >= 4 and linea[2] == 'then:':
            lines_to_remove.append(i)
        elif linea[0] == 'while:' and len(linea) >= 3 and linea[2] == 'do:':
            lines_to_remove.append(i)
        elif linea[0] == 'repeat:' and len(linea) >= 3 and linea[1] == 'for:':
            lines_to_remove.append(i)
        elif linea[0] in {'canPut:', 'canPick:', 'canMove:', 'canJump:'} and len(linea) >= 4 and linea[2] == 'ofType:' and linea[3] in types:
            lines_to_remove.append(i)
        elif linea[0] == 'not:' and len(linea) >= 2:
            lines_to_remove.append(i)
        elif len(linea) >= 2 and linea[0] == 'facing:' and linea[1] in directions:
            lines_to_remove.append(i)
    
    for index in reversed(lines_to_remove):
        del token_list[index]
        
    print(token_list)

    return len(token_list) == 0





