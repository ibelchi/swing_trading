# radarcore: Guía de Inversión (Conceptos y Práctica)

Bienvenido a **radarcore**. Este manual te ayudará a entender cómo funciona la estrategia **Buy the Recovery** (Compra la Recuperación) y cómo puedes usar este software para aprender sobre finanzas y swing trading desde cero.

---

## 1. ¿Qué es la estrategia "Buy the Recovery"?

Históricamente, mucha gente ha oído el término "Buy the Dip" (comprar la caída). En RadarCore la llamamos **Buy the Recovery** porque es más precisa: no compramos cuando la acción está cayendo activamente (un "cuchillo cayendo"), sino cuando ya ha encontrado un suelo y ha comenzado a recuperarse.

El objetivo es aprovechar que el precio tiende a volver a su media tras un susto temporal.

---

## 2. Antes de empezar: Configurando el Escáner

Cuando configuras el escáner, ves una serie de parámetros. Aquí tienes lo que significan en lenguaje sencillo:

*   **Lookback Days (Días de mirada atrás)**: Es cuánto tiempo atrás miramos en el pasado para buscar el punto más alto de la acción. Si pones 60 días, buscamos el "Récord" de precio de esos 2 meses para compararlo con el precio de hoy.
*   **Min Drop % (Caída mínima %)**: Cuánta "rebaja" quieres que tenga la acción antes de notificarte. Si pones 15%, solo buscamos empresas que hayan caído al menos un 15% desde su máximo de 60 días.
*   **Min Rebound % (Rebote mínimo %)**: Es la comprobación de que ya no estamos cayendo. Si pones 2%, quieres que la acción ya haya subido un 2% desde su punto más bajo.
*   **Symbol Limit**: Cuántas empresas del mercado quieres analizar (0 para analizarlas todas).

---

## 3. El Modelo de Cubetas (Buckets) y Fases

En lugar de una sola estrategia rígida, RadarCore clasifica cada acción en una **Cubeta** (Patrón) y una **Fase** (Timing).

### Las Cubetas Principales (Buckets)
*   **SWING**: La configuración clásica. Una caída profunda seguida de un rebote claro.
*   **RISE**: La acción ya está en una tendencia alcista constante. Menor recorrido de crecimiento pero más estable.
*   **LATERAL**: La acción se mueve de lado. Fase de acumulación.

### El Ciclo de Vida (Fases)
El programa te indica en qué momento del "viaje" de vuelta a los máximos te encuentras:
*   🟢 **VALLEY (Valle)**: Estás en el fondo. Máximo beneficio potencial, pero máximo riesgo.
*   🟡 **MID (Punto medio)**: La recuperación está confirmada. Estás en el "punto dulce" de la tendencia.
*   🟠 **MATURE (Maduro)**: La mayor parte de la recuperación ya ha pasado. Cuidado al entrar ahora.
*   🔴 **LATE (Tarde)**: La acción ya ha vuelto a sus máximos. La oportunidad se ha agotado.

---

## 4. Conceptos Financieros Clave

### Stop Loss (SL)
Es tu **freno de mano de seguridad**. Imagina que compras una acción a 10$. Si de pronto la empresa sigue yendo mal, el Stop Loss es una orden que le dice a tu banco: "Si la acción vuelve a caer hasta 9$, véndela inmediatamente".
*   **¿Para qué sirve?** Porque si la empresa quiebra, tú solo habrás perdido 1$ (de 10 a 9), pero te habrás salvado de perder los 10$ enteros. RadarCore marca esta línea en rojo en los gráficos.

### Objetivos (T1 y T2)
Son tus "metas de venta" donde recoges beneficios.
*   **T1 (Objetivo Conservador)**: Es un punto intermedio de recuperación (habitualmente al 85% del máximo anterior). Donde podrías decidir vender la mitad para asegurar ganancias rápidas.
*   **T2 (Objetivo Ideal)**: Cuando la acción vuelve exactamente al precio máximo que tenía antes de caer. La estrategia se ha completado con éxito.

### Mercados de Referencia (El S&P 500)
Aunque escanees otros mercados, el programa siempre usa el "Mercado Americano" (**SPY / S&P 500**) como referencia global. Si la bolsa americana cae fuerte, es difícil que cualquier acción suba de forma sana. Sirve como termómetro para saber si la caída es un caso aislado o una crisis mundial.

---

## 5. Caso Práctico: Interpretando Gráficos

Cuando abras un gráfico en RadarCore, busca estos colores:

1.  **La Montaña (Oro)**: Muestra la tendencia de 2 años. Busca formas de "U" o "V".
2.  **Triángulos Verdes (Valles)**: Son los suelos. El triángulo verde más reciente marca el inicio de la recuperación actual.
3.  **Triángulos Rojos (Picos)**: Son los techos. Muestran dónde la acción encontró resistencia anteriormente.

## Regla de Oro: Diversificación
Nunca pongas todos tus ahorros en una sola acción. La estrategia correcta consiste en tener, por ejemplo, 10 operaciones diferentes a la vez. Así, si una sale mal y salta el **Stop Loss**, las otras 9 pueden seguir su curso hacia el **T2** y darte un beneficio global.
