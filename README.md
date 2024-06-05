# Práctica Agentes Inteligentes

El objetivo de esta práctica es programar un agente inteligente para el entorno de tareas del juego de piedra papel tijera.

Preguntas a responder:

1. Especificar las características del entorno de trabajo.
2. Identificar el tipo de agente para determinar la estructura del agente.
3. Implementar en Python los componentes de la estructura del agente para construir la función agente o la función map.

## 1. El problema

Estudio de la solución del juego **piedra**, **papel**, **tijeras** a través de un agente inteligente programado en Python.

## 2. Esquema de tareas

El entorno de trabajo representa el contexto o escenario donde un agente inteligente realiza operaciones, interactúa y soluciona problemas específicos.

Identificar correctamente las propiedades de este entorno es fundamental, ya que contribuye al diseño más adecuado para el agente, mejorando así su desempeño y eficacia en la resolución de problemas.

Resumen de las caracteríasticas del entorno del RPS:

Entorno de tareas | Observable| Agentes | Determinista | Episódico | Estático | Discreto | Conocido
:---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
 RPS | Parcialmente | Multiagente | Estocástico | Episódico | Estático |  Discreto | Conocido |

- Parcialmente observable: No se puede saber qué piensa el agente rival.
- Multiagente: Existen dos jugadores (agentes) que se enfrentan.
- Estocástico: Las acciones del agente varían el resultado en cada partida.
- Episódico: Cada partida es "independiente" de la anterior.
- Estático: El medio no cambia mientras el usuario piensa su acción.
- Discreto: Las variables a tener en cuenta son limitadas y discretas.
- Conocido: Sabemos las reglas del juego en todo momento y no cambian.

## 3. Estructura del agente

Una vez se conoce en profundidad el entorno de trabajo del agente, es posible definir con mayor precisión la estructura que este tomará. Para el juego RPS, el programa del agente más adecuado sería el agente reactivo basado en modelos. La razón principal por la que se ha elegido este agente, es que en el juego de piedra, papel o tijeras es parcialmete observable, lo cual requiere un historial de partidas. De esta manera, se busca obtener la elección más acertada, teniendo como referencia la información acumulada de las partidas anteriores.

![img](doc/agenteinteligente.png)

Cuando el historial.json está vacío, o el número de partidas es menor a 3, la elección del bot se elige de manera aleatoria, ya que no se cuenta con un dataset para analizar.

Se registra el resultado de cada partida en un archivo JSON con el siguiente formato:

        {
            "player": "Paper",
            "computer": "Paper",
            "result": "Tie"
        }

Utilizando la información almacenada en el historial, se realiza un análisis de la frecuencia de cada elección por parte del "player", se obtiene la de mayor frecuencia y se elige la opción que la venza. Por ejemplo, si la elección con mayor frecuencia (en ese momento) es "tijera", la próxima elección de "computer" será "piedra".

## 4. Extensión

En este paso se plantea extender la lógica para poder jugar al piedra, papel, tijera, lagarto, Spock.

Para poder implementar este modo de juego, se deben añadir las opciones de lagarto y spock a la clase GameAction, al diccionario de victorias y a la función assess_game, para tener en cuenta las nuevas posibilidades de victoria y derrota.

Por último se debe añadir al diccionario de frecuencias, para poder comparar las veces que se repiten en el historial.


## 5. Bibliografía

Lutz, Mark. Learning Python. Sebastopol, Ca, O’reilly, 2018.

Martin, Robert C. Clean Code a Handbook of Agile Software Craftmanship. Upper Saddle River [Etc.] Prentice Hall, 2010.

Martin, Robert C. Clean Architecture: A Craftsman’s Guide to Software Structure and Design. Prentice Hall, 2018.

S. McConnel. Code Complete: A Practical Handbook of Software Construction, 2dn Edition. Microsoft Press, 2004.

Russell, Peter. ARTIFICIAL INTELLIGENCE : A Modern Approach, Global Edition. S.L., Pearson Education Limited, 2021.

[RPSLS](http://www.samkass.com/theories/RPSSL.html)
