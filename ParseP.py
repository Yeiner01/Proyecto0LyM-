import re

def tokenize(text):
    token_specs = [
        ('ASSIGN',   r':='),   # operador de asignación
        ('HASHID',   r'#[A-Za-z_][A-Za-z0-9_]*'),  # ej: #chips, #north
        ('NUMBER',   r'\d+'),
        ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
        ('PIPE',     r'\|'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('COLON',    r':'),
        ('DOT',      r'\.'),
        ('COMMA',    r','),    # para separar variables locales
        ('SKIP',     r'[ \t]+'),
        ('NEWLINE',  r'\n'),
        ('MISMATCH', r'.'),
    ]
    token_regex = "|".join("(?P<%s>%s)" % (name, pattern) for name, pattern in token_specs)
    regex = re.compile(token_regex)
    
    tokens = []
    line_num = 1
    line_start = 0
    
    for mo in regex.finditer(text):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            tokens.append((kind, int(value), line_num, column))
        elif kind in ('ID', 'HASHID'):
            tokens.append((kind, value, line_num, column))
        elif kind in ('PIPE', 'LBRACKET', 'RBRACKET', 'COLON', 'DOT', 'COMMA', 'ASSIGN'):
            tokens.append((kind, value, line_num, column))
        elif kind == 'NEWLINE':
            line_num += 1
            line_start = mo.end()
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Unexpected character {value!r} on line {line_num}")
    return tokens

def parse_program(tokens):
    global pos
    pos = 0
    program = {}
    program['variables'] = parse_variable_declaration(tokens)
    program['procedures'] = []
    while pos < len(tokens) and tokens[pos][0] == 'ID' and tokens[pos][1] == 'proc':
        program['procedures'].append(parse_procedure_definition(tokens))
    program['main'] = parse_code_block(tokens) if pos < len(tokens) and tokens[pos][0] == 'LBRACKET' else []
    return program

def parse_variable_declaration(tokens):
    global pos
    vars_list = []
    if pos < len(tokens) and tokens[pos][0] == 'PIPE':
        pos += 1
        while pos < len(tokens) and tokens[pos][0] == 'ID':
            vars_list.append(tokens[pos][1])
            pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'COMMA':
                pos += 1
        if pos < len(tokens) and tokens[pos][0] == 'PIPE':
            pos += 1
        else:
            raise SyntaxError("Expected '|' at end of variable declaration")
    return vars_list

def parse_procedure_definition(tokens):
    global pos
    if pos >= len(tokens) or tokens[pos][0] != 'ID' or tokens[pos][1] != 'proc':
        raise SyntaxError("Expected 'proc' keyword")
    pos += 1
    if pos >= len(tokens) or tokens[pos][0] != 'ID':
        raise SyntaxError("Expected procedure name")
    proc_name = tokens[pos][1]
    pos += 1
    params = []
    while pos < len(tokens) and tokens[pos][0] in ('COLON', 'ID'):
        if tokens[pos][0] == 'COLON':
            pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'ID':
                params.append(tokens[pos][1])
                pos += 1
            else:
                raise SyntaxError("Expected parameter name after ':'")
        elif tokens[pos][0] == 'ID' and tokens[pos][1].startswith("and"):
            pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'COLON':
                pos += 1
                if pos < len(tokens) and tokens[pos][0] == 'ID':
                    params.append(tokens[pos][1])
                    pos += 1
                else:
                    raise SyntaxError("Expected parameter name after 'and...:'")
    body = parse_code_block(tokens)
    return {'name': proc_name, 'params': params, 'body': body}

def parse_code_block(tokens):
    global pos
    if pos >= len(tokens) or tokens[pos][0] != 'LBRACKET':
        raise SyntaxError("Expected '[' at beginning of code block")
    pos += 1
    instrs = []
    while pos < len(tokens) and tokens[pos][0] != 'RBRACKET':
        instrs.append(parse_instruction(tokens))
    if pos < len(tokens) and tokens[pos][0] == 'RBRACKET':
        pos += 1
    else:
        raise SyntaxError("Expected ']' at end of code block")
    return instrs

def parse_instruction(tokens):
    global pos
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input in instruction")
    token = tokens[pos]
    if token[0] == 'ID' and pos + 1 < len(tokens) and tokens[pos+1][0] == 'ASSIGN':
        return parse_assignment(tokens)
    return parse_procedure_call(tokens)

def parse_assignment(tokens):
    global pos
    var_name = tokens[pos][1]
    pos += 1
    pos += 1
    expr = tokens[pos][1]
    pos += 1
    return ('assign', var_name, expr)

def parse_procedure_call(tokens):
    global pos
    proc_name = tokens[pos][1]
    pos += 1
    args = []
    while pos < len(tokens) and tokens[pos][0] == 'COLON':
        pos += 1
        args.append(tokens[pos][1])
        pos += 1
    return ('proc_call', proc_name, args)

def check_syntax(text):
    try:
        tokens = tokenize(text)
        parse_program(tokens)
        return True
    except Exception as e:
        return False
