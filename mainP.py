from ParseP import check_file

def main():
    filename = input("Ingrese el nombre del archivo a cargar (ej: caso_prueba.txt): ").strip()
    result = check_file(filename)
    print(result)

if __name__ == '_main_':
    main()