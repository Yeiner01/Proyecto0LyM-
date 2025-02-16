import Parser as P

def main():
    nombre_archivo = input("Dijite el archivo txt: ")  # Asegúrate de que el archivo exista en el mismo directorio que tu script o ajusta la ruta adecuadamente.
    
    # Procesamiento del archivo usando las funciones definidas
    valid_tokens = P.tokenizer(nombre_archivo)
    
    # Intentar parsear los tokens válidos y manejar cualquier error de sintaxis
    try:
        P.parser(valid_tokens)
        print("Parsing completado con éxito.")
        print(valid_tokens)  # Opcional: imprimir los tokens válidos para verificación
    except SyntaxError as e:
        print(str(e))

if __name__ == "__main__":
    main()

