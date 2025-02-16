from ParseP import check_file
import ParseP as PP

def main():
    filename = input("Ingrese el nombre del archivo a cargar (ej: caso_prueba.txt): ").strip()
    result = PP.check_file(filename)
    print(result)

if __name__ == '__main__':
    main()