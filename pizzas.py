class Guardar:
    @staticmethod
    
    def unapizza(tamaño, ingredientes, numero):
         try:
        
            if tamaño == 'chica':
                costo_tamaño = 40
            elif tamaño == 'mediana':
                costo_tamaño = 80
            elif tamaño == 'grande':
                costo_tamaño = 120
            else:
                raise ValueError("Tamaño de pizza no válido")

            subtotal = costo_tamaño * numero

         
            if ingredientes.get('jamon', False):
                subtotal += 10*numero
            if ingredientes.get('piña', False):
                subtotal += 10*numero
            if ingredientes.get('champiñones', False):
                subtotal += 10*numero
            
            

            ingredientes_seleccionados = [ingrediente for ingrediente, seleccionado in ingredientes.items() if seleccionado]
            with open('pizzas.txt', 'a') as archivo_texto:
                cadena_ingredientes = ', '.join(ingredientes_seleccionados)
                archivo_texto.write(f'\n{tamaño}-{cadena_ingredientes }-{numero}-{subtotal}')
                with open('pizzas.txt', 'r') as archivo_texto:
                  lineas = archivo_texto.readlines()
                  datos_archivo = Guardar.leer_datos_archivo()
            return "¡Muy bien insertado correctamente!"
         except Exception as e:
            return f"Error al insertar la palabra: {e}"

    @staticmethod
    def leer_datos_archivo():
     datos = []
     try:
        with open('pizzas.txt', 'r') as archivo_texto:
            lineas = archivo_texto.readlines()
            for idx, linea in enumerate(lineas):
                try:
                    partes = linea.strip().split('-')
                    if len(partes) == 4:
                        tamaño, ingredientes, numero, subtotal = partes[0], partes[1], int(partes[2]), int(partes[3])
                        datos.append({'tamaño': tamaño, 'ingredientes': ingredientes, 'numero': numero, 'subtotal': subtotal})
                    else:
                        print(f"Advertencia: Ignorando línea con formato incorrecto en la línea {idx + 1}: {linea}")
                except Exception as e:
                    print(f"Error al procesar línea {idx + 1}: {e}")
     except Exception as e:
        print(f"Error al leer el archivo: {e}")
     return datos

    @staticmethod
    def sumar_subtotales():
        try:
            with open('pizzas.txt', 'r') as archivo_texto:
                lineas = archivo_texto.readlines()

            total_subtotales = sum(int(linea.strip().split('-')[3]) for linea in lineas if len(linea.strip().split('-')) == 4)

            return total_subtotales
        except Exception as e:
            return f"Error al sumar los subtotales: {e}"
    @staticmethod  
    def eliminar_ultima_pizza():
        try:
            with open('pizzas.txt', 'r') as archivo_texto:
                lineas = archivo_texto.readlines()

            if lineas:
                lineas.pop()  

            with open('pizzas.txt', 'w') as archivo_texto:
                archivo_texto.writelines(lineas)

            return "Eliminada correctamente la última pizza"
        except Exception as e:
            return f"Error al eliminar la última pizza: {e}"
        
    @staticmethod
    def modificar_pizza(indice, nuevo_dato, campo_a_modificar):
     try:
        with open('pizzas.txt', 'r') as archivo_texto:
            lineas = archivo_texto.readlines()

        if indice < 0 or indice >= len(lineas):
            return "Índice de pizza fuera de rango"

        pizza_actual = lineas[indice].split('-')
        if campo_a_modificar == 'tamaño':
            pizza_actual[0] = nuevo_dato
        elif campo_a_modificar == 'ingredientes':
            pizza_actual[1] = nuevo_dato
        elif campo_a_modificar == 'numero':
            pizza_actual[2] = nuevo_dato
        elif campo_a_modificar == 'precio':
            pizza_actual[3] = nuevo_dato
        else:
            return "Campo a modificar no válido"

        lineas[indice] = '-'.join(pizza_actual)

        with open('pizzas.txt', 'w') as archivo_texto:
            archivo_texto.writelines(lineas)

        return f"Modificado correctamente el campo {campo_a_modificar} para la pizza"
     except Exception as e:
        return f"Error al modificar la pizza: {e}"


if __name__ == "__main__":
    indice_a_modificar = 2
    nuevo_dato_pizza = "Nuevos ingredientes modificados"
    campo_a_modificar = 'numero'

    resultado = Guardar.modificar_pizza(indice_a_modificar, nuevo_dato_pizza, campo_a_modificar)
    print(resultado)