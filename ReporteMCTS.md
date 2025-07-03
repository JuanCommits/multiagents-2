# Monte Carlo Tree Search vs. Minimax & Random Agents

## Introducción

Este informe presenta un análisis comparativo de diferentes estrategias de agentes en dos juegos de mesa clásicos: **Tic-Tac-Toe** y **Nocca-Nocca**. El foco principal está en evaluar el rendimiento del agente basado en **Monte Carlo Tree Search (MCTS)** frente a enfoques tradicionales como los agentes **Minimax** y **Random**. Los experimentos fueron diseñados para analizar cómo se comportan estos agentes bajo diversas configuraciones, prestando especial atención al impacto de los parámetros de MCTS como el número de *rollouts*, simulaciones y estrategias de selección de acciones.

### Descripción de los Juegos

- **Tic-Tac-Toe**: Un juego simple, determinista y de información perfecta, frecuentemente utilizado como referencia para evaluar estrategias de búsqueda.
- **Nocca-Nocca**: Un juego de tablero por turnos más complejo que introduce mayor profundidad y posibilidades estratégicas, siendo ideal para probar algoritmos de búsqueda avanzados.

### Agentes

- **Agente Aleatorio**: Selecciona movimientos de forma completamente aleatoria. Sirve como línea base para la comparación de rendimiento.
- **Agente Minimax**: Implementa el algoritmo clásico de minimax con profundidad de búsqueda configurable. Es óptimo para juegos deterministas con información perfecta.
- **Agente MCTS**: Usa simulaciones aleatorias para evaluar movimientos, con parámetros configurables:
  - **Rollouts**: Número de veces que se recorre el árbol por jugada.
  - **Simulaciones**: Número de partidas simuladas por *rollout*.
  - **Estrategia de selección de acción**: Define cómo el agente elige acciones desde el árbol de búsqueda (por ejemplo, valor máximo).

## Configuración Experimental

Los experimentos fueron definidos mediante un archivo JSON que especificaba:
- Los agentes a comparar
- Tipo de juego y sus parámetros
- Número de iteraciones y tamaño de lote
- Parámetros específicos de MCTS (*rollouts*, simulaciones, selección de acciones)

Los resultados se visualizaron en gráficos de cuatro paneles para cada experimento:
1. **Recompensas acumuladas a lo largo del tiempo**
2. **Victorias por lote de partidas**
3. **Promedio de movimientos por partida**
4. **Resumen de rendimiento general**

## Resultados

### 1. MCTS vs. Minimax (Tic-Tac-Toe)

![MCTS vs Minimax TicTacToe](results/tic-tac-toe/mcts(10_rollouts,100_simulations)_vs_minimax(3_depth).png)

- **Observación**: Minimax supera consistentemente a MCTS en recompensas acumuladas y partidas ganadas.
- **Interpretación**: En un juego simple y totalmente explorable como Tic-Tac-Toe, Minimax (con profundidad suficiente) es óptimo, mientras que MCTS tiene dificultades para igualar su rendimiento debido a su naturaleza estocástica y horizonte de búsqueda limitado.

### 2. MCTS vs. Aleatorio (Tic-Tac-Toe)

![MCTS vs Random TicTacToe](results/tic-tac-toe/mcts(10_rollouts,100_simulations)_vs_random.png)

- **Observación**: MCTS domina al agente aleatorio, logrando el máximo de victorias y recompensas posibles.
- **Interpretación**: Incluso con una cantidad moderada de *rollouts* y simulaciones, MCTS supera ampliamente a la estrategia aleatoria, demostrando su capacidad de aprender estrategias efectivas mediante simulación.

### 3. MCTS vs. MCTS (Parámetros diferentes, Tic-Tac-Toe)

![MCTS vs MCTS Params TicTacToe](results/tic-tac-toe/mcts(5_rollouts,200_simulations)_vs_mcts(10_rollouts,100_simulations).png)

- **Observación**: Aumentar la cantidad de simulaciones (aunque con menos *rollouts*) puede mejorar el rendimiento, como se observa en el agente con 5 *rollouts* y 200 simulaciones superando al de 10/100.
- **Interpretación**: El balance entre *rollouts* y simulaciones es crucial; más simulaciones por *rollout* pueden permitir una exploración más profunda, pero la configuración óptima depende del juego.

### 4. MCTS (500 simulaciones) vs. Minimax (Tic-Tac-Toe)

![MCTS 500 Simulations vs Minimax TicTacToe](results/tic-tac-toe/minimax(3_depth)_vs_mcts(5_rollouts,500_simulations))

- **Observación**: Incluso con 500 simulaciones por jugada, MCTS no logra superar a Minimax en Tic-Tac-Toe. Minimax sigue ganando de forma consistente, lo que demuestra que 500 simulaciones no son suficientes para igualar la búsqueda exhaustiva de Minimax en un juego pequeño.
- **Interpretación**: Aumentar las simulaciones permite que MCTS se aproxime al juego óptimo, pero Minimax sigue siendo difícil de superar en juegos completamente explorables.

### 5. MCTS vs. Aleatorio (Nocca-Nocca)

![MCTS vs Random NoccaNocca](results/nocca-nocca/mcts(10_rollouts,100_simulations)_vs_random.png)

- **Observación**: MCTS supera consistentemente al agente aleatorio, como era de esperarse.
- **Interpretación**: La capacidad de MCTS de simular y evaluar estados futuros le otorga una ventaja considerable frente al juego aleatorio.

### 6. MCTS vs. Minimax (Nocca-Nocca)

![MCTS vs Minimax NoccaNocca](results/nocca-nocca/mcts(10_rollouts,100_simulations)_vs_minimax(2_depth).png)

- **Observación**: En Nocca-Nocca, MCTS puede superar a Minimax, especialmente cuando este está limitado en profundidad.
- **Interpretación**: La complejidad de Nocca-Nocca hace inviable una búsqueda exhaustiva para Minimax con baja profundidad, permitiendo que MCTS aproveche sus simulaciones para lograr mejor desempeño.

### 7. MCTS (200 Simulaciones) vs. Minimax (Nocca-Nocca)

![MCTS 200 Simulations vs Minimax NoccaNocca](results/nocca-nocca/mcts(10_rollouts,200_simulations)_vs_minimax(2_depth).png)

- **Observación**: En Nocca-Nocca, aumentar las *simulaciones* a 200 otorga al agente MCTS una ventaja significativa frente a Minimax, especialmente cuando este está limitado por la profundidad de búsqueda.
- **Interpretación**: Más *simulaciones* permiten a MCTS explorar y evaluar mejor los posibles futuros, haciéndolo más robusto en juegos complejos donde Minimax está computacionalmente limitado.

### 8. MCTS vs. MCTS (Parámetros diferentes, Nocca-Nocca)

#### 8.1. Rollouts & Simulations
![MCTS vs MCTS Params NoccaNocca](results/nocca-nocca/mcts(5_rollouts,200_simulations)_vs_mcts(10_rollouts,100_simulations).png)

- **Observación**: Similar a Tic-Tac-Toe, el agente con más simulaciones por *rollout* tiende a tener mejor rendimiento.
- **Interpretación**: Ajustar los parámetros es esencial para maximizar el rendimiento de MCTS, especialmente en juegos más complejos.

#### 8.2. Max Value vs Max Count
![MCTS vs MCTS Params NoccaNocca](results/nocca-nocca/mcts(5_rollouts,200_simulations)_vs_mcts(5_rollouts,200_simulations)_max_value.png)

- **Observación**: Al comparar dos variantes de MCTS con los mismos parámetros de *rollouts* y simulaciones, pero diferentes estrategias de selección de acción (una elige la acción más visitada, *max count*, y la otra la de mayor valor promedio, *max value*), se observa que la estrategia *max value* obtiene consistentemente todas las victorias y recompensas positivas, mientras que *max count* pierde todas las partidas.
- **Interpretación**: En este entorno y configuración, seleccionar la acción por valor promedio (*max value*) resulta mucho más efectivo que simplemente elegir la más visitada (*max count*), ya que permite explotar mejor la información obtenida durante las simulaciones y evita sesgos por exploración excesiva.

## Impacto de los Parámetros de MCTS

- **Rollouts**: Más *rollouts* tienden a mejorar la exploración, pero pueden reducir la profundidad de cada simulación.
- **Simulaciones**: Más simulaciones por *rollout* permiten una evaluación más profunda de cada acción, lo que suele conducir a mejores decisiones.
- **Estrategia de selección de acción**: Los resultados muestran que seleccionar la acción por *valor promedio* (*max value*) puede ser significativamente superior a elegir la acción más visitada (*max count*), especialmente en configuraciones donde la exploración puede inducir a errores o sesgos. La elección de la estrategia de selección de acción tiene un impacto directo en el rendimiento final del agente MCTS.



## Conclusión Final

La búsqueda Monte Carlo en árboles (MCTS) es un enfoque poderoso y flexible tanto para juegos simples como complejos. Aunque puede no superar a algoritmos deterministas como Minimax en juegos pequeños y completamente explorables (como Tic-Tac-Toe), MCTS sobresale en entornos más grandes o complejos donde la búsqueda exhaustiva no es práctica.

El rendimiento de MCTS es altamente sensible a sus parámetros, y se requiere una afinación cuidadosa para obtener resultados óptimos. En general, MCTS representa una estrategia robusta para juegos generales, especialmente cuando el espacio de estados es demasiado amplio para métodos tradicionales.
