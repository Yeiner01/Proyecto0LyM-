def lexer_parser(Str_ingresado: str):
    Str_ingresado = ["n" if i.isdigit() else i for i in [i for i in Str_ingresado.replace("\n", "").replace("\t", "").replace("|", "-|-")
              .replace(" ", "-").replace("[", "-[-").replace("]", "-]-").replace("--", "-").split("-") if i]]
    
    variables_globales, variables_locales, aperturas, procedimientos = [], [], [], []
    local, variables, apertura_block, parametro, validez = False, False, False, False, True
    
    for i in Str_ingresado:
        if i == "|" and not variables and not apertura_block:
            variables = True
            aperturas.append("|")
            Str_ingresado[Str_ingresado.index(i)] = "("
        elif i == "|" and variables and not apertura_block:
            Str_ingresado[Str_ingresado.index(i)] = "("
            variables = False
            aperturas.pop()
        elif variables and not local and not apertura_block:
            variables_globales.append(i)
            Str_ingresado[Str_ingresado.index(i)] = "("
        elif i in variables_globales:
            Str_ingresado[Str_ingresado.index(i)] = "n"
        elif i == "proc":
            local = True
            procedimientos.append([])
            Str_ingresado[Str_ingresado.index(i)] = "("
        elif local:
            if i == "[":
                apertura_block = True
            elif i == "]":
                apertura_block =  False
                local = False
                variables_locales = []
            elif ":" in i and not apertura_block:
                parametro = True
                procedimientos[-1].append(i)
                Str_ingresado[Str_ingresado.index(i)] = "("
            elif parametro and not apertura_block:
                if ":" not in i and "[" not in i and "]" not in i:
                    variables_locales.append(i)
                    Str_ingresado[Str_ingresado.index(i)] = "("
                    parametro = False
                else:
                    validez = False
            elif apertura_block:
                if i == "|" and not variables:
                    variables = True
                    aperturas.append("|")
                    Str_ingresado[Str_ingresado.index(i)] = "("
                elif i == "|" and variables:
                    Str_ingresado[Str_ingresado.index(i)] = "("
                    variables = False
                    aperturas.pop()
                elif variables:
                    variables_locales.append(i)
                    Str_ingresado[Str_ingresado.index(i)] = "("
                elif i in variables_locales:
                    Str_ingresado[Str_ingresado.index(i)] = "n"
            elif not apertura_block:
                procedimientos[-1].append(i)
                Str_ingresado[Str_ingresado.index(i)] = "("
        
    Str_ingresado = [i for i in (" ".join([i for i in Str_ingresado if i not in ["("]]).replace("n := n .", "").replace("nop .", "").split()) if i]
    
    turn = False
    for idx, i in enumerate(Str_ingresado):
        if i == "turn:":
            turn = True
        elif turn and i in ["#left", "#right", "#around"]:
            Str_ingresado[idx], turn = "&", False
        elif turn:
            validez = False
    
    Str_ingresado = ["D" if i in ["#north", "#south", "#east", "#west"] else
               "X" if i in ["#balloons", "#chips"] else
               "O" if i in ["#front", "#left", "#right", "#back"] else i
               for i in Str_ingresado]
                    

            
            
