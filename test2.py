def limpiar_diccionarios(array_de_dicts):
    for diccionario in array_de_dicts:
        # Utilizamos list(diccionario) para iterar sobre una copia de las claves
        # ya que no se pueden modificar las claves de un diccionario mientras se itera sobre ellas
        for clave in list(diccionario):
            if isinstance(diccionario[clave], dict):
                # Si el valor es otro diccionario, llamamos recursivamente a la función
                limpiar_diccionarios([diccionario[clave]])
                if not diccionario[clave]:  # Eliminamos el campo si el diccionario interno quedó vacío
                    del diccionario[clave]
            elif diccionario[clave] == "":
                # Eliminamos el campo si el valor es una cadena vacía
                del diccionario[clave]

# Ejemplo de uso:
array_de_dicts = [
    {"nombre": "John", "edad": "", "direccion": {"calle": "", "ciudad": "New York"}},
    {"nombre": "Jane", "edad": "25", "direccion": {"calle": "Main St", "ciudad": ""}},
    {"nombre": "", "edad": "30", "direccion": {"calle": "Broadway", "ciudad": "Los Angeles"}},
]

limpiar_diccionarios(array_de_dicts)

print(array_de_dicts)
