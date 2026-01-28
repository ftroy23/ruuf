# Optimización de Paneles Solares  
**¿Cuántos paneles caben en un techo rectangular?**

## Descripción del problema

El objetivo es encontrar la máxima cantidad de paneles (rectángulos de `a × b` ) que caben en un techo (rectángulo de `x × y`).

* Sin restricciones de orientación en el enunciado. 
  Para acotar el problema, se consideran solo rotaciones de 90° (`a × b` o `b × a`).

* Función principal: `calculate_panels`.

---

## Planteamiento del problema

### 1. Análisis Inicial (Papel y Lápiz)
Antes de escribir código, busqué la lógica matemática. Dibujé el rectángulo de dimensiones `(x, y)` y probé ubicar los paneles `(a, b)` de forma manual, identifiqué dos puntos clave:

* **La orientación importa:** No cabe la misma cantidad si orientamos todos los paneles a lo largo que a lo ancho.
* **Límite Superior:** El máximo teórico está dado por $\frac{Area_{techo}}{Area_{panel}}$, pero este valor es solo un límite teórico

### 2. Comparación de Orientaciones Simples
Comencé con una lógica básica para comparar qué pasaba si llenábamos todo el techo con una sola orientación y otra:

```python
def how_many_boxes(H, W, h, w): 
    # Orientación A
    max_amount = (H // h) * (W // w)
    # Comparar con Orientación B (Rotada)
    if (H // w) * (W // h) > max_amount:
        max_amount = (H // w) * (W // h)
    return max_amount
```

Observé que el resultado cambiaba, por lo que surgió la pregunta: ¿Qué pasa si algunos paneles se rotan y otros no?

### 3. La Solución Final: Combinación de Rotaciones
La solución final consiste en mezclar orientaciones dividiendo el techo en secciones horizontales. El algoritmo funciona así:

* Iteración: Probamos colocar $i$ filas de paneles en orientación original.
* Sección Restante: El espacio vertical que sobra se intenta rellenar con paneles rotados 90°.
* Maximización: Se evalúan todos los valores posibles de $i$ (desde 0 hasta el máximo de filas posibles) y se conserva el resultado más alto.

## Cálculo por iteración
Para un número `i` de filas no rotadas:

```python
height_used = i * panel_height        # Altura usada por paneles no rotados
height_left = roof_height - height_used # Altura restante
```
Paneles por fila no rotada:

```python
boxes_per_row_hw = roof_width // panel_width # Paneles por fila
boxes_hw = i * boxes_per_row_hw # Total paneles no rotados 
```
Paneles rotados en el espacio restante:

```python
rotated_rows = height_left // panel_width # Filas de paneles rotados
boxes_per_row_wh = roof_width // panel_height # Paneles por fila
boxes_wh = rotated_rows * boxes_per_row_wh # Total de paneles rotados
```
Total de paneles:

```python
total = boxes_hw + boxes_wh
```
### Fórmula compacta
Toda la lógica anterior puede resumirse en una sola expresión:

```python
total = (rows * (roof_width // panel_width)) +
        ((roof_height - rows * panel_height) // panel_width) * 
        (roof_width // panel_height)
```
### Implementación final
```python
def calculate_panels(panel_width: int, panel_height: int,
                     roof_width: int, roof_height: int) -> int:

    best = 0
    best_layout = None

    for rows in range(0, roof_height // panel_height + 1):
        height_used = rows * panel_height
        height_left = roof_height - height_used

        boxes_per_row_hw = roof_width // panel_width
        boxes_hw = rows * boxes_per_row_hw

        rotated_rows = height_left // panel_width
        boxes_per_row_wh = roof_width // panel_height
        boxes_wh = rotated_rows * boxes_per_row_wh

        total = boxes_hw + boxes_wh

        if total > best:
            best = total
            best_layout = (rows, rotated_rows),
                          (boxes_per_row_hw, boxes_per_row_wh)

    return best
```

### Información adicional
La variable `best_layout` guarda:

* Número de filas no rotadas y rotadas

* Cantidad de paneles por fila en cada orientación

Esta información no se retorna ni se imprime, pero queda disponible para inspección.

### Consideración extra
#### ¿Es esta la solución absoluta?

He agregado un condicional que compara el resultado final contra el área restante. Si el área libre es mayor al área de un panel, entonces podrían caber más paneles agregando rotaciones internas.

Opté por no implementar rotaciones mixtas dentro de una misma fila (ej: un panel vertical y uno horizontal al lado) porque, aunque podrían
mejorar marginalmente el aprovechamiento del área, en una instalación real
incrementan significativamente la complejidad de montaje, alineación,
cableado y costos operativos.

### ¿Cómo ejecutar?
Igual que en las instrucciones: 

python3 main.py

:)



# Ejercicio Bonus: Paneles en un Techo Triangular

## Descripción del problema

Determinar cuántos paneles rectangulares de dimensiones `panel_width × panel_height`
pueden instalarse dentro de un **techo con forma de triángulo isósceles**, de base
`roof_width` y altura `roof_height`.

## Planteamiento del problema
Al igual que con el ejercicio rectangular, el análisis comenzó en papel. Al dibujar rectángulos dentro de un triángulo, identifiqué que el factor limitante es el ancho disponible en la parte superior del panel, ya que es el punto donde las esquinas del panel tocarían primero los lados inclinados del techo.

Identifiqué que al colocar una fila de paneles a una altura determinada, el espacio restante hacia arriba sigue siendo un triángulo semejante al original.

Utilicé esta **semejanza de triángulos** para determinar cuánto ancho queda disponible a cualquier altura $y$. La fórmula es:
$$Ancho\_disponible = \frac{Ancho\_techo \times (Altura\_techo- y)}{Altura\_techo}$$

Esta fórmula asegura que, sin importar a qué altura estemos, siempre sabremos con precisión cuántos paneles caben de forma horizontal antes de chocar con los bordes del techo.

---

### Lógica de la Solución
Debido a que el ancho cambia en cada nivel, una simple solución como no rotar las primeras filas y el resto si no es suficiente. Implementé una **solución recursiva** que explora un árbol de decisiones para maximizar el espacio:

1.  **Cálculo de Fila:** En la altura actual, calculamos cuántos paneles caben según el ancho disponible en el punto más restrictivo (la parte superior de la fila de paneles).
2.  **Ramificación (Decisión):**
    * **Opción A:** Colocar la fila actual con orientación normal (`width x height`), sumar los paneles que caben y llamar recursivamente a la función para el triángulo restante superior..
    * **Opción B:** Colocar la fila actual con orientación rotada (`height x width`), sumar los paneles y llamar recursivamente a la función para el espacio restante.
3.  **Resultado:** La función compara ambos caminos y retorna el valor máximo encontrado.