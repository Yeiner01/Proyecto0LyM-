import Parser as P

def main():
    nombre_archivo = input("Ingrese el nombre del archivo (sin '.txt'): ").strip()
    contenido = P.leer_archivo(nombre_archivo)
    print("\nContenido del archivo:\n")
    print(contenido)

if __name__ == "_main_":
    main() 
