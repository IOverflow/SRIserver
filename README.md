# SRIserver
Server to host search engine for Information Recovery project.

# Introduccion

"Informacion es poder", una frase autocontenida, que encierra las necesidades
siempre crecientes de nosotros como cientificos, y de nuestros usuarios como 
beneficiarios directos del producto que sale de nuestros programas. Esta necesidad
se vio grandemente reflejada en el ultimo proyecto "freelance" de nosotros (los autores),
cuando intentamos crear una herramienta que sirviera de ayuda a los heroes veraderos de estos
momentos, el personal medico. Sickipedia nace como un modulo que, desde hace algun tiempo, tenemos en mente incorporar al conjunto de funcionalidades de dicho proyecto, y hasta ahora
no era mas que una simple idea. El siguiente proyecto de SI, intenta servir de base para la implementacion de dicho modulo. Esta es la razon de que el conjunto de datos que elegimos sea
referente a la salud.

# Que se espera del sistema ?

En su integracion final, el sistema tiene que ser capaz de recibir una consulta (mas adelante
explicamos las estructuras de estas consultas y como las manejamos) propiciada por el usuario,
(que puede ser un personal medico o un paciente) y debe responder con un conjunto de enfermedades que mas se adecue a "lo que el usuario quiere recibir".

Esta descripcion es quizas un poco vaga, pero asi lo son generalemente los problemas
a los que nos enfrentamos. Podemos pensar que cualquier usuario, siempre va a querer
recibir enfermedades como resultado, pero lo mas importante es saber cuales les vamos a
propiciar.

# Estructura interna del sistema

Nuestro sistema debe manejar enfermedades, asi que hay que comenzar por representar dichas
enfermedades. 

## Enfermedades

Estas entidades conformaran los documentos de nuestro sistema, a cada una le asignaremos un ID,
por conveniencia sera un entero secuencial, de modo que el ID de un elemento permita acceder a 
este si decidimos almacenarlo en un array en memoria. Ademas cada enfermedad contara con una
descripcion, un nombre, un conjunto de sintomas y un tratamiento. Cada uno de estos campos sera
un string en ingles.

Estos campos permiten crear las enfermedades como objetos JSON y almacenarlas en un archivo
"diseases.json" o crear una representacion en una tabla y utilizar una base de datos relacional
para el almacenamiento (en la implementacion nos preocupamos por que fuera posible ambas opciones, por defecto se usa json como almacenamiento por comodidad, pero hacer un setup para
usar sqlite, posgresql o mysql no es dificil. Incluso se puede usar un schema de una bd no relacional como Mongo.)

El vocabulario de terminos que usara nuestro sistema estara compuesto por cada palabra que aparezca en cualquier campo de las efermedades, quitando algunas como preposiciones, conjunciones, articulos, comas, etc.

La representacion de las enfermedades nos da una idea inmediata de hacia donde esta dirigida nuestra implementacion. Evidentemente, esperamos que en la query hayan algunos terminos que pertenezcan
al vocabulario, lo que significa que aparecen en algun campo de las enfermedades, y por tanto hay
alguna enfermedad con algun nivel de similitud entre la query y algunos documentos. Es perfectamente
posible que en la query no aparezcan terminos del vocabulario, en este caso el sistema no deberia devolver ningun documento como relevante.

## Modelo

En un primer momento, el problema planteado puede llevar a pensar que el modelo boleano es el
indicado para resolverlo. Ciertamente, este modelo cumple la restriccion de que solo devuelva 
documentos que contengan algun termino de la query, pero rapidamente este modelo devuelve resultados
no deseados, ademas de que no es capaz de establecer una diferencia entre dos documentos devueltos, no
existe nocion de orden de relevancia. Por lo tanto pasamos al modelo vectorial. Este modelo resulta
adecuado para nuestro problema por el hecho de que necesitamos asignar un peso a cada termino en los
documentos, y que este peso este influido por la cantidad de veces que aparece este termino en el documento (esta idea responde a que un termino que aparezca en el nombre de una enfermedad, es menos
probable que aparezca mas repetido que un termino que aparezca en los sintomas, por lo que deberia
tener mayor impacto en la busqueda). Por supuesto, la habilidad de nuestros usuarios de conjurar
querys adecuadas puede influir positivamente en la precision de nuestro modelo, por lo que dedicamos
esfuerzos a indicar algunas ayudas para que el usuario genere mejore sus consultas a traves de 
funcionalidades como autocompletamiento y sugerencia de terminos relacionados que les permita extender
su consulta.

En general, el proceso de obtencion de los resultados en el sistema se ve asi:

!["./SystemStructure.png"](./SystemStructure.png)

## Procesamiento de la query
(TODO) ESTO ES TUYO ELI, aqui va todo lo del autocompletamiento, extension de la query, etc.
(OJO) SOlO la descripcion de como se hace, y porque, aqui no va nada de implementacion ni codigo ni nada.

## Vectorizacion

La vectorizacion comprende el proceso de convertir la query y cada
documento de la coleccion en un vector. Para la query, calculamos la maxima frequencia
de los terminos del vocabulario en la propia query, y luego generamos un vector con N componentes (donde N
es la cantidad de terminos en el vocabulario) donde cada componente i se calcula de la siguiente forma:

![](./wiq.png)

En este punto, es necesario aclarar una modificacion que le hacemos al modelo. Es posible que
la maxima frequencia sea 0, en caso de que ningun termino de la query aparezca en el vocabulario. En este caso decidimos devolver el vector (0, 0, ..., 0), lo que provoca que todo documento tenga similitud 0 con esta query, y por tanto no se devuelva ningun documento.
Este comportamiento es consistente con el hecho de que un documento es relevante si al menos
un termino de la query esta en el, y ademas, se logra que terminos aleatorios no tengan ningun peso en la busqueda.

Para los documentos, se sigue una idea parecida, se calculan las frequencias de cada termino
del documento y la frecuenia de ocurrencia del termino, lo que se conoce como "algoritmo
tf-idf". En la implementacion pudieramos haber utilizado un modulo experimental de keras
que aplica este algoritmo automaticamente, pero queda mucho mejor hecho a mano (y se aprende mas :).

## Calculo de similitud

## Filtrado de relevancia

![](./Network.png)