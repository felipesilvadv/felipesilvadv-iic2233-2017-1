Estructura general:

Usuario --> Frontend --> Backend

Campeon Ataca:

Usuario hace click sobre objetivo--> Genera animacion del ataque --> Verifica que el ataque sea valido, baja vida del objetivo, se suma a las estadisticas generales 


Campeon se mueve:

Usuario presiona alguna de las teclas "WASD" --> campeon se mueve hacia la direccion indicada con referencia del cursor--> Verifica que no se salga de los bordes o que no haya ninguna estrucura que no debe atravesar, calcula la nueva posicion que le corresponde a ese campeon y lo actualiza en la data de posiciones.


Muerte del inhibidor:

Usuario controla a su campeon para matar el inhibidor --> Animacion del muerte del inhibidor --> Eliminar el inhibidor de los objetos con vida, cambiar el patron de generacion de subditos del equipo que destruyo el inhibidor.


