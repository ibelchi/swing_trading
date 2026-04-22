# radarcore: Especificación Técnica (Inteligencia de Patrones Agrupados)

Documentación orientada a analistas financieros y diseñadores de algoritmos cuantitativos.
RadarCore es un terminal de análisis multibucket basado en la **Reconstrucción de la Acción del Precio** y el **Agrupamiento de Tendencias**.

---

## 1. Arquitectura de Detección: Clustered Bucketing
A diferencia de los escáneres tradicionales de estrategia única, RadarCore utiliza un **PatternClassifier** para agrupar los activos en 5 "cubetas" (buckets) de comportamiento basados en los últimos 252 días:

*   **SWING**: Setups de reversión a la media de alta convicción. Gran caída seguida de una recuperación estructural.
*   **RISE**: Momentum alcista sostenido. Caracterizado por máximos y mínimos crecientes.
*   **LATERAL**: Consolidación en rango. Compresión de volatilidad horizontal.
*   **HIGHS**: Activos cotizando cerca de sus máximos de 52 semanas (y 3 años). Poco upside inmediato.
*   **DESCENDING**: Tendencia bajista. El filtrado automático suele descartar estos candidatos.

### Subtipos de Patrón
Para los buckets `SWING` y `RISE`, el motor identifica subtipos tácticos:
- **BREAKOUT**: El precio cruza por encima de un pico anterior (resistencia).
- **PULLBACK**: Retroceso correctivo temporal dentro de una recuperación o tendencia alcista.
- **RETEST**: El precio vuelve a probar un valle estructural previo (soporte).

---

## 2. Motor de Reconstrucción (Pivot Points)
El sistema utiliza el algoritmo **Ramer-Douglas-Peucker (RDP)** para filtrar el ruido e identificar macroscópicamente los **Pivot Points**:
*   **Valles (Troughs - T)**: Mínimos locales que marcan bases de soporte potencial.
*   **Picos (Peaks - P)**: Máximos locales que marcan zonas de resistencia.

---

## 3. Fases Dinámicas (Ciclo de Vida)
RadarCore modela el camino de recuperación relativo al Máximo Histórico de 3 años (ATH 3Y):
1.  **🟢 VALLEY (Descubrimiento)**: < 20% de progreso desde el pivote hacia el ATH. Máxima ratio riesgo/beneficio.
2.  **🟡 MID (Punto dulce)**: 20–65% de progreso. Recuperación estructural confirmada con alpha restante.
3.  **🟠 MATURE (Distribución)**: 65–85% de progreso. Momentum decreciente, zona de posible reversión.
4.  **🔴 LATE (Agotamiento)**: > 85% de progreso. El activo está cerca del ATH; la operación está estadísticamente agotada.

---

## 4. Puntuación de Confianza (Modelo Ponderado)
Cada bucket utiliza un módulo de puntuación personalizado (ej: `SwingScorer`). Para el bucket **SWING**, la nota se calcula:
1.  **Potencial de Upside (30%)**: Escalado según la distancia hasta el ATH 3Y.
2.  **Recencia (25%)**: Bonus si el valle estructural se ha producido en los últimos 5–30 días.
3.  **Confirmación de Volumen (20%)**: Positivo si el volumen medio reciente (5d) supera la media trimestral (20d).
4.  **Pendiente de Momentum (10%)**: Correlación positiva de los últimos 5 días de cierre.

---

## 5. Riesgo y Contexto Relativo
*   **Stop Loss (SL)**: Referenciado al `Period_Low`. Invalidación técnica de la posición alcista.
*   **Objetivos**: T1 (85% de recuperación), T2 (100% de reversión al pico anterior).
*   **Alfa de Mercado**: Cálculo de `Relative_Drop = Asset_Drop - SPY_Drop`.
    - `Relative_Drop >= 5%`: **Movimiento Idiosincrásico** (Alta calidad).
    - `Relative_Drop < 5%`: **Movimiento Sistémico** (Dependiente del mercado general).
