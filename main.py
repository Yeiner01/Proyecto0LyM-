import Parser as P

def main():
    nombre_archivo = input("Dijite el archivo txt: ")  
    valid_tokens = P.tokenizer(nombre_archivo)
    try:
        P.parser(valid_tokens)
        print("Parsing completado con éxito.")
        print(valid_tokens)
    except SyntaxError as e:
        print(str(e))

if __name__ == "__main__":
    main()

