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


3. A continuación muestro la deriva de la posicion real con eulerint usando 1k subdivisiones.Como se puede ver el error es mayor al 1% pero se demoraba al rededor de 30 min por lo que no seguí intentando. Aún asi se ve claramente que el error mejora y que la tardanza se debe a la poca eficiencia del método.

![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Diferencia%20eulerin%20vs%20real%20con%20mil%20subdivisiones.png?raw=true)

4. Luego de implementar las correcciones de J2 y J3 se ven mejoras considerables. Primero mostraré el grafico de posicion donde la línea azul es la orbita real (obtenida del archivo EOF) y la naranja es la predicha.Luego mostraré la deriva utilizando odeint de la orbitra predicha vs la real. 

![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Posicion%20con%20Correccion.png?raw=true)


![alt text](https://github.com/FelipeAravenaR98/MCOC2020-P1/blob/master/Entrega%205/Deriva%20Correccion%20Odeint.png?raw=true)


Como se puede ver, la deriva utilizando odeint disminuye a un error de 100 km solamente. Los tiempos en obtener los gráficos son practicamente los mismos y no note diferencia aplicando la correccion que sin aplicar. Esto me hace pensar que el problema de demora en eulerint es por la ineficiencia del algoritmo simplemente.






