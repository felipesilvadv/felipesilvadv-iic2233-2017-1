En mi tarea, logre formar una comunicacion efectiva y practica entre el server
y el client, para ejecutarlo hay q iniciar primero el server, luego el modulo
gui.py, se me olvido cambiarle los nombres, si abren el otro no se abrira la
intefaz grafica y solo se podran hacer un par de cosas.

Las ventanas de la interfaz son 4, la primera es la de ingreso, en esa uno
ingresa usuario y contraseña, si no esta registrado ese nombre de usuario se
creara uno con ese nombre y la contraseña que se de, si el nombre de usuario
ya esta cargado, entonces se revisara la contraseña dada, en caso de no 
coincidir, no permitira ingresar y se cerrara el juego, y probablemente habra 
un mensaje en consola de que la contraseña es incorrecta, la segunda parte 
de la interfaz es la de seleccion de salas, no alcance a ajustarla para que
tuviera actualizada los valores de personas y segundo de cancion, tenia
pensado poner un boton para actualizar salas, que al final lo saque, 
ahi se cargaran en una lista todas las salas disponibles, para acceder a una
hay que seleccionarla y apretar el boton seleccionar sala o elegir sala (no 
recuerdo exactamente el nombre que le puse), lo que dara ingreso a la interfaz
de juego y chat, este paso se puede demorar un poco, ya que tiene que esperar
a que el cliente reciba la cancion del server y un poco de informacion extra
(la cancion que recibe esta cortada a 20 segundos pero a veces se demora un
poco), en ese momento se abrira una ventana (la cuarta de la que cree) dando
un mensaje de que se esta cargando la sala, una vez cargada se actualiza la
pregunta y las opciones donde una es la correcta, se crea en la carpeta del 
cliente un archivo .wav que debiese reproducirse, mediante un QSound, por 
alguna razon eso no me funcionaba, pese a que la cancion se podia reproducir
en mi reproductor predeterminado de mi cpu. Dentro de esta interfaz hay un 
boton para volver a la seleccion de salas, tambien se puede abrir el tab para
el chat, este funciona solo para que lo vea quien escribe, me falto hacer la 
conexion para que se enviara a todos los de la sala (eran como 5-10 lineas, me 
falto tiempo nomas), me falto conectar el puntaje que se mostraba con el 
atributo puntaje de la clase usuario que representa a cada cliente, dentro 
del modulo server, también me falto que el proceso que genere cuando se inicia
la sala, se repitiera cada 20 segundos, para mantener de forma continua la
reproduccion de musica dentro de la sala, junto con la actualizacion de las 
tablas del tercer tab, que solo me falto hacer las conexiones 
correspondientes.

Los usuarios se guardan cada vez que se manda un mensaje hacia el servidor, en
la carpeta users/ que se crea al momento de ejecutar el servidor, al diseñar
las interfaces las pense para que fueran aplicables a cualquier plataforma, 
por eso lo hice con los tab, ya que de esa forma quedaba mas ordenado el 
layout.

El juego no permite que dos usuarios ingresen con el mismo nombre, se cierra 
automaticamente el programa y se crea una ventana que lo notifica, a veces me 
fallaba (tal vez es porque no se alcanza a captar una señal), pero en general
funcionaba bien.

Muchas clases son innecesarias dentro de los modulos, pero las defini porque
de esa forma podia mandar objetos personalizados desde el server al client y
viceversa, ya que las serializaba con pickle.

Perdon por dejar tantos print, pero no alcance a borrarlos ni comentarlos,
pero en general son de utilidad para ver que esta pasando entre el server y 
el client, hay un par que muestran cosas de la gui.

El server se demora bastante en cargar, hay q esperar a que en consola salga 
un input que diga "manda algo".

