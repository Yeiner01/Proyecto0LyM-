from ParseP import d
import ParseP as PP

def main():
    filename = input("Ingrese el nombre del archivo a cargar (ej: caso_prueba.txt): ").strip()
    result = PP.check_syntax(filename)
    print(result)

if __name__ == '__main__':
    main()