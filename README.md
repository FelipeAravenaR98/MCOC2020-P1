# Entrega 1

![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Trayectoria%20para%20distintos%20vientos.%20Entrega%201..png?raw=true)

# Entrega 5

1. A continuación se muestra la posición (x,y,z) en el tiempo del vector de estado de Sentinel 1A/B. Donde la línea azul es la orbita real (obtenida del archivo EOF) y la naranja es la predicha. Se ve hacia el final como se comienzan a separar:
![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Posicion%20sin%20Correccion.png?raw=true)

2.Antes de comparar los algoritmos, comparare estos con la solucion real para tener una idea de como queda.
A continuación se muestra el gráfico donde se compara  la posicion real y la de odeint:
![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Deriva%20odeint%20sin%20correccion.png?raw=true)

A continuación se muestra el gráfico donde se compara  la posicion real y la de eulerint con Nsubdivisiones = 1:
![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Deriva%20eulerint%20sin%20correccion.png?raw=true)

A continuación se muestra el gráfico donde se compara  la posicion según odeint vs eulerint con Nsubdivisiones = 1 que es lo pedido en esta ocasión:
![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Eulerint%20vs%20odeint.png?raw=true)

Se puede ver que al final del tiempo derivan en 20 mil km. Esto ya que el algoritmo de eulerint se aleja muchisimo como se puede ver en la figura de real vs eulerint. En cuanto a producir los resultados, me di cuenta que a pesar de que no es mucho tiempo, eulerint tarda más. Incluso puede tardar minutos si uno se pone a jugar con las subdivisiones.

3.

4.
