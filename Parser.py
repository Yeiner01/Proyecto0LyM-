import re 




def leer_archivo(nombre_archivo):
    """Lee el contenido de un archivo .txt y lo devuelve como una cadena."""
  

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read().lower()   
    except FileNotFoundError:
        return f"Error: El archivo '{nombre_archivo}' no existe."
    except Exception as e:
        return f"Ocurrió un error: {e}"  
def tokenizer(text):
    try:
        archivo = leer_archivo(text)
    except Exception as e:
        print(e)
        return []
    
    lines = archivo.split('\n')
    token_list = []
    
    for line in lines :
        tokens = line.strip().split()
        if tokens:
            token_list.append(tokens)
    return token_list


def parser(token_list):
    variables = set()
    procedimientos = {} 
    stack = [] 
    
    for line in token_list:
        if not line:
            continue

        first_token = line[0]
        if first_token.startswith("|") and first_token.endswith("|"):
            vars_def = first_token.strip("|").split()
            variables.update(vars_def)
        elif first_token == "proc":
            proc_name = line[1]
            params = []
            if ":" in proc_name:
                proc_parts = proc_name.split(":")
                proc_name = proc_parts[0]
                params.append(proc_parts[1])
            
            for i in range(2, len(line) - 1, 2):
                if line[i] == "and":
                    params.append(line[i+1])
            
            procedimientos[proc_name] = set(params)
        elif len(line) >= 3 and line[1] == ":=":
            var_name = line[0]
            if var_name not in variables:
                return False 
        elif first_token in procedimientos:
            params = [tok for tok in line if tok.isnumeric()]
            if set(params) != procedimientos[first_token]:
                return False 
        for token in line:
            if token == "[":
                stack.append("[")
            elif token == "]":
                if not stack or stack[-1] != "[":
                    return False
                stack.pop()
    
    return len(stack) == 0 


