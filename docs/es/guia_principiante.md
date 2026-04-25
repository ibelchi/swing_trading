# RadarCore — Guía Completa para Principiantes
### De cero a entender el swing trading y cómo usar el software

> **Aviso importante:** Este documento es exclusivamente educativo. RadarCore es una herramienta de aprendizaje y análisis técnico. Nada de lo que encontrarás aquí constituye consejo financiero. Invertir conlleva riesgo de pérdida de capital. Consulta siempre a un profesional regulado antes de tomar decisiones financieras reales.

---

## Cómo usar esta guía

No hace falta que la leas toda de golpe. Está estructurada como un recorrido: empieza desde el principio si no sabes nada de finanzas, o ve directamente a la sección que te interesa si ya tienes alguna base. Cada concepto importante aparece en **negrita** la primera vez que se menciona y se explica inmediatamente con ejemplos del mundo real.

---

# PARTE 1 — El mundo de las inversiones, explicado desde cero

## Capítulo 1: ¿Por qué la gente invierte?

Imagina que tienes 1.000€ guardados en el colchón. Al cabo de un año, siguen siendo 1.000€. Pero los precios han subido un 3% (el pan, la luz, el alquiler). En términos reales, esos 1.000€ ahora valen menos: con ellos puedes comprar menos cosas que hace un año.

Esto se llama **inflación**: la pérdida de poder adquisitivo del dinero con el tiempo. Es el enemigo silencioso de los ahorros inactivos.

La gente invierte para intentar que su dinero crezca a un ritmo superior a la inflación. En lugar de un colchón, ponen el dinero a trabajar.

### Las tres grandes opciones de inversión

**1. Renta fija (bonos, depósitos):** Le dejas el dinero a un banco o a un gobierno a cambio de un interés pactado. Riesgo bajo, rendimiento bajo. Ejemplo: un depósito al 2% anual.

**2. Renta variable (acciones):** Compras una pequeña parte de una empresa. Si la empresa va bien, el valor de tu parte sube. Si va mal, baja. Riesgo más alto, pero potencial de rendimiento muy superior.

**3. Activos alternativos (inmuebles, oro, criptomonedas):** Cada uno con sus propias reglas.

RadarCore trabaja exclusivamente con **renta variable**, concretamente con **acciones** de grandes empresas cotizadas en bolsa.

---

## Capítulo 2: ¿Qué es una acción y cómo funciona la bolsa?

### La acción como trozo de empresa

Cuando una empresa grande quiere crecer y necesita dinero, en lugar de pedir un préstamo al banco puede decidir "vender trozos de sí misma" al público. Cada trozo es una **acción** (en inglés, *stock* o *share*).

**Ejemplo real:** Apple tiene aproximadamente 15.000 millones de acciones en circulación. Si compras una, eres propietario de una quincemilmillonésima parte de Apple. ¿Poco? Sí. Pero si Apple vale más mañana, tu trozo también vale más.

### El ticker: el nombre código de cada empresa

Cada empresa cotizada tiene un código abreviado único que se usa en todo el mundo financiero. Se llama **ticker symbol** o simplemente **ticker**.

| Empresa | Ticker |
|---|---|
| Apple Inc. | AAPL |
| Microsoft | MSFT |
| Visa Inc. | V |
| Inditex (IBEX) | ITX.MC |

En RadarCore verás siempre los tickers en la columna **Symbol** de la tabla de resultados, y puedes hacer clic en ellos para ir directamente a Yahoo Finance.

### La bolsa como mercado

La **bolsa** (o mercado de valores) es simplemente el lugar donde compradores y vendedores de acciones se encuentran. Hoy es electrónica: no hay ninguna sala física con gente gritando. Cada segundo, millones de órdenes de compra y venta se cruzan automáticamente.

El **precio** de una acción en cada momento es simplemente el último precio al que alguien estuvo dispuesto a comprar y otro a vender. Si hoy más gente quiere comprar Apple que vender, el precio sube. Si hay más vendedores que compradores, baja.

### OHLCV: los cinco datos de cada día

Para cada acción y cada día de mercado, se registran cinco datos fundamentales. Los encontrarás en cualquier gráfico profesional y en RadarCore:

- **O (Open):** Precio de apertura. El primer precio del día.
- **H (High):** Precio máximo alcanzado durante la sesión.
- **L (Low):** Precio mínimo de la sesión.
- **C (Close):** Precio de cierre. El último precio del día. Es el más importante y el que RadarCore usa para la mayoría de cálculos.
- **V (Volume):** Número de acciones que han cambiado de manos ese día.

**¿Por qué importa el volumen?** Un movimiento de precio con volumen alto es mucho más significativo que el mismo movimiento con volumen bajo. Si una acción sube un 5% pero poquísima gente ha comprado, puede ser ruido. Si sube un 5% con el doble de volumen habitual, es una señal de convicción real del mercado.

---

## Capítulo 3: Los índices de referencia

Seguir 500 empresas una por una sería imposible. Por eso existen los **índices de mercado**: cestas de empresas que representan un conjunto más amplio.

### Los principales índices que usa RadarCore

**S&P 500 (USA):** Las 500 empresas más grandes de los Estados Unidos por capitalización de mercado. Es el termómetro de la economía americana y, por extensión, de la economía global. Incluye Apple, Microsoft, Amazon, NVIDIA, JPMorgan, etc.

**NASDAQ 100 (USA):** Las 100 empresas no financieras más grandes del NASDAQ, la bolsa tecnológica americana. Muy concentrado en tech: Apple, Microsoft, NVIDIA, Meta, Alphabet, Tesla...

**IBEX 35 (España):** Las 35 empresas más líquidas de la bolsa española. Santander, Inditex, BBVA, Iberdrola, Telefónica...

**DAX 40 (Alemania):** Las 40 principales empresas alemanas. SAP, Siemens, Volkswagen, BMW, Allianz...

**EuroStoxx 50 (Europa):** Las 50 empresas más grandes de la zona euro, de todos los sectores y países.

**Nikkei 225 (Japón):** 225 empresas líderes japonesas. Toyota, Sony, SoftBank...

**Nifty 50 (India):** Las 50 empresas principales de la bolsa de Bombay.

### ¿Por qué el S&P 500 es el "termómetro global"?

Cuando el S&P 500 cae fuertemente, casi todo el mundo financiero lo nota. Los inversores institucionales (fondos de pensiones, bancos, aseguradoras) mueven billones de dólares y cuando venden acciones americanas, también venden en otros mercados para cubrir las pérdidas. Por eso RadarCore usa siempre el S&P 500 como referencia para detectar si una caída es global o específica de una empresa.

### Capitalización de mercado: el tamaño de una empresa

La **capitalización de mercado** (*market cap*) es el valor total d una empresa en bolsa. Se calcula multiplicando el precio de una acción por todas las acciones existentes.

```
Market Cap = Precio por acción × Número total de acciones
Ejemplo: Apple a $200 × 15.000M acciones = ~$3 billones
```

| Categoría | Market Cap | Ejemplos |
|---|---|---|
| Mega-cap | > $200B | Apple, Microsoft, NVIDIA |
| Large-cap | $10B - $200B | Visa, McDonald's, Nike |
| Mid-cap | $2B - $10B | muchas empresas sólidas |
| Small-cap | $300M - $2B | empresas pequeñas |
| Micro-cap | < $300M | muy especulativas |

RadarCore por defecto solo analiza empresas con **Min Mkt Cap ≥ $10B** para evitar el ruido y la manipulación de las empresas pequeñas.

---

# PARTE 2 — Estrategias de inversión: ¿cómo gana la gente?

## Capítulo 4: Las tres filosofías principales

### Buy & Hold (Comprar y mantener)
La filosofía de Warren Buffett. Compras acciones de empresas excelentes y las guardas durante años o décadas sin vender. Funciona muy bien para quien tiene paciencia y horizonte largo. El problema: requiere mucho tiempo y es emocionalmente difícil aguantar caídas del 40-50% sin vender.

### Day Trading (Operar intradiario)
Compras y vendes el mismo día, aprovechando movimientos de minutos u horas. Requiere mucho tiempo, acceso a plataformas profesionales, capital importante y una tolerancia al riesgo extrema. Estudios muestran que la gran mayoría de day traders pierden dinero a largo plazo.

### Swing Trading (La estrategia de RadarCore)
El término medio. **Swing trading** significa aprovechar las "oscilaciones" (*swings*) del precio de una acción en un horizonte de **días a semanas** (típicamente 2-6 semanas). No estás delante de la pantalla todo el día, pero tampoco compras y olvidas durante años.

La idea central: los precios de las acciones no van en línea recta. Suben, bajan, se consolidan, vuelven a subir. Un swing trader intenta detectar cuándo una acción ha bajado por motivos temporales y comprarla antes de que vuelva a subir.

---

## Capítulo 5: La estrategia "Buy the Recovery" de RadarCore

### La intuición detrás de la estrategia

Imagina una empresa sólida, digamos Visa (la de las tarjetas de crédito). Un trimestre tiene resultados ligeramente por debajo de las expectativas de los analistas, o hay un momento de pesimismo general en el mercado. El precio cae un 20% en pocas semanas.

Pero Visa sigue procesando miles de millones de transacciones cada día. Su negocio no ha cambiado fundamentalmente. Aquella caída del 20% es una **oportunidad temporal** para comprar una empresa sólida a precio de descuento.

Esto es lo que busca RadarCore: empresas que han caído por motivos temporales y que ya muestran señales de haber tocado suelo y estar recuperándose.

### ¿Por qué "Buy the Recovery" y no "Buy the Dip"?

"Buy the Dip" (comprar la caída) sería comprar mientras la acción sigue bajando. El problema es que nadie sabe cuándo tocará suelo. Podrías comprar a -20% y que siga bajando hasta -60%.

"Buy the Recovery" espera la confirmación: la acción ya ha tocado el mínimo y ha reboteado un poco. Pierdes los primeros centímetros de la recuperación, pero confirmas que el suelo ya está aquí. Es menos emocionante pero mucho más disciplinado.

### El patrón que buscamos: la forma de "V" o "L"

Visualmente, la estrategia busca dos patrones principales:

**Patrón V (V-RECOVERY):**
```
     Máximo
    /       \
   /         \         Recuperación
  /           \       /
 /             \ Mín /
```
Caída rápida y fuerte seguida de una recuperación igualmente rápida. Alta volatilidad. Puede ser muy rentable pero también arriesgado.

**Patrón L (L-BASE):**
```
     Máximo
    /       \
   /         \___________  ← Base lateral (acumulación)
  /                       \
 /                         Recuperación lenta pero sólida
```
Caída seguida de un período de consolidación horizontal. Los inversores institucionales "acumulan" acciones sin prisa mientras el precio se mantiene estable. Cuando finalmente rompe al alza, suele ser un movimiento más sólido.

**Para RadarCore, L-BASE es considerado de más calidad que V-RECOVERY** porque la base lateral sugiere que los grandes compradores se están posicionando discretamente.

---

# PARTE 3 — Conceptos técnicos fundamentales

## Capítulo 6: El Drawdown, el Rebote y la Recuperación

### Drawdown: cuánto ha caído una acción

El **drawdown** es la caída porcentual desde un máximo hasta un mínimo posterior. Es la medida del "dolor" que ha sufrido una acción.

```
Cálculo del Drawdown:
Máximo reciente: $100
Mínimo posterior: $75
Drawdown = (100 - 75) / 100 = 25%
```

En RadarCore, la columna **Drop %** muestra exactamente este valor: cuánto ha caído la acción desde su máximo de los últimos X días (configurable con el parámetro *Historical Window*) hasta su mínimo.

**Por ejemplo:** Si Visa tenía un máximo de $360 y cayó hasta $290, el Drop % sería:
```
(360 - 290) / 360 = 19.4%
```

### El Rebote: primera señal de vida

El **rebote** (*rebound*) mide cuánto ha subido la acción desde su mínimo hasta el precio actual. Es la confirmación de que la caída se ha detenido.

```
Cálculo del Rebound:
Mínimo: $75
Precio actual: $82
Rebound = (82 - 75) / 75 = 9.3%
```

En RadarCore, la columna **Rebound %** muestra este valor. El parámetro *Minimum Rebound (%)* (por defecto 2%) filtra las acciones que todavía no han mostrado ninguna señal de recuperación.

### ¿Por qué RadarCore exige un rebote mínimo?

Para evitar comprar "cuchillos que caen". Si una acción ha bajado un 30% pero sigue bajando, el rebote es 0%. No hay confirmación de giro. RadarCore espera a que el precio haya demostrado que el mínimo ya ha quedado atrás.

---

## Capítulo 7: La Caída Idiosincrásica vs. la Caída Sistémica

Esta distinción es **la más importante de toda la estrategia**. Entendiéndola triplicarás la calidad de tus decisiones.

### Caída Sistémica: el mercado explica la caída

Si el mercado entero (el S&P 500) cae un 20%, es normal que muchas empresas caigan un 20-25%. En este caso, la caída no es culpa de la empresa: es el contexto global. Comprar en un entorno de caída general es arriesgado porque no hay un "suelo" claro.

### Caída Idiosincrásica: la empresa cae sola

Si el mercado sube un 5% pero una empresa cae un 25%, aquella caída es **idiosincrásica** (es decir, específica de esa empresa). Puede ser por resultados decepcionantes, cambio de directivo, problema regulatorio temporal o simplemente miedo exagerado de los inversores.

Estas caídas idiosincrásicas en empresas fundamentalmente sólidas son las **mejores oportunidades de swing trading**, porque:
1. La empresa no ha caído porque el mundo esté mal.
2. Cuando el miedo pasa, el precio tiende a recuperarse hacia el nivel anterior.

**En RadarCore verás:** `✅ Idiosyncratic drop (+16.6% vs SPY)` en los resultados del escaneo. Significa que la empresa ha caído un 16.6% MÁS que el mercado, confirmando que su caída es específica suya.

### ¿Cómo lo calcula RadarCore?

```
Caída relativa = Drawdown de la empresa - Drawdown del SPY
                   en el mismo período de tiempo

Si Caída relativa > 5% → Caída idiosincrásica ✅
Si Caída relativa ≤ 5% → Caída sistémica ⚠️
```

---

## Capítulo 8: Medias Móviles (EMA)

### ¿Qué es una media móvil?

Imagina que quieres saber si una persona tiene fiebre. No miras la temperatura de un segundo: la mides a lo largo del tiempo. Las **medias móviles** hacen lo mismo con el precio de una acción: suavizan el ruido diario para mostrar la tendencia real.

Una **EMA (Exponential Moving Average)** es una media móvil exponencial que da más peso a los precios recientes que a los antiguos. Reacciona más rápido a los cambios que una media simple.

### EMA 50 y EMA 200: las más importantes

**EMA 50:** La media de los últimos 50 días de cotización. Representa la tendencia a medio plazo.

**EMA 200:** La media de los últimos 200 días. Representa la tendencia a largo plazo. Muchos inversores institucionales consideran que una acción está "en tendencia alcista" cuando cotiza por encima de su EMA 200.

### El Cruce Dorado y el Cruce de la Muerte

**Cruce Dorado (Golden Cross):** Cuando la EMA 50 supera por arriba a la EMA 200. Señal alcista fuerte. Muchos algoritmos automáticos compran en ese momento.

**Cruce de la Muerte (Death Cross):** Cuando la EMA 50 cae por debajo de la EMA 200. Señal bajista.

```
Precio > EMA50 > EMA200 → Tendencia alcista sólida (RISE)
Precio < EMA50 < EMA200 → Tendencia bajista (DESCENDING)
Precio oscila alrededor de EMA50 → Posible SWING o LATERAL
```

---

## Capítulo 9: RSI — El índice de fuerza relativa

### ¿Qué mide el RSI?

El **RSI (Relative Strength Index)** es un indicador que mide la velocidad y magnitud de los movimientos de precio recientes en una escala de 0 a 100. Lo crearon en los años 70 y sigue siendo uno de los más usados del mundo.

**Interpretación clásica:**
- RSI > 70 → La acción puede estar **sobrecomprada** (ha subido demasiado rápido, posible corrección)
- RSI < 30 → La acción puede estar **sobrevendida** (ha bajado demasiado rápido, posible rebote)
- RSI entre 40-60 → Zona neutral

**Cómo lo usa RadarCore:** El RSI en el mínimo del suelo es un confirmador de calidad. Si una acción llega a su mínimo con RSI < 30 y después el RSI comienza a recuperarse hacia 40-50, es una señal de que la sobreventa se ha agotado y que el rebote puede tener continuidad.

**Importante:** El RSI por sí solo nunca es suficiente para tomar decisiones. Es un confirmador, no un predictor.

---

## Capítulo 10: ATR — La volatilidad real de cada acción

### ¿Qué es el ATR?

El **ATR (Average True Range)** mide cuánto se mueve una acción de media cada día. No dice la dirección (si sube o baja), sino la magnitud típica del movimiento.

**Ejemplo:**
- Si Apple tiene un ATR de $5, significa que de media cada día el precio oscila $5 entre el mínimo y el máximo.
- Si una empresa de $10 tiene un ATR de $2, ¡es enormemente volátil (20% diario)!

### ¿Para qué sirve el ATR en RadarCore?

**Para calcular el Stop Loss de manera inteligente.** En lugar de poner un stop fijo (por ejemplo, "vendo si baja un 8%"), usamos el ATR para adaptar el stop a la volatilidad real de cada acción:

```
Stop Loss = Mínimo del suelo - (ATR × 1.5)
```

Para una acción muy volátil, el stop será más amplio (para evitar ser "salpicado" por movimientos normales). Para una acción tranquila, el stop será más estrecho.

---

## Capítulo 11: El concepto de Pivot y el Algoritmo RDP

### ¿Qué es un pivot?

Un **pivot** (o punto de giro) es un máximo local o un mínimo local en el gráfico de una acción. En un gráfico de dos años, puede haber decenas de movimientos, pero los pivots son los "momentos clave": los picos y los valles estructurales del precio.

- **Peak (Pico, marcado como P1, P2...):** Un máximo local, desde donde el precio giró a la baja.
- **Trough (Valle, marcado como T1, T2...):** Un mínimo local, desde donde el precio giró al alza.

### El Algoritmo RDP: filtrar el ruido del mercado

El mercado financiero está lleno de ruido. Cada día el precio sube y baja por cientos de motivos triviales. El reto es separar el movimiento meaningful (estructural) del ruido irrelevante.

**RDP (Ramer-Douglas-Peucker)** es un algoritmo matemático diseñado originalmente para simplificar líneas en cartografía digital. Si tienes una costa con mil pequeñas bahías, el RDP te ayuda a dibujarla con 20 puntos esenciales en lugar de 1.000, manteniendo la forma global.

RadarCore lo aplica al precio de una acción: simplifica los dos años de cotización a entre 6 e 16 puntos clave (los pivots), eliminando el ruido de días concretos para revelar la estructura real del movimiento.

**Visualmente en RadarCore:** En la vista "Pivots" del gráfico, ves la línea discontinua blanca (los pivots RDP) sobre la línea dorada (el precio real). La línea blanca te muestra la "narrativa" de la acción, sin ruido.

---

## Capítulo 12: Las Eras — la narrativa del precio

### Segmentos y Eras

Una vez el algoritmo RDP ha identificado los pivots, RadarCore clasifica cada segmento entre dos pivots consecutivos:

- **UP:** El segmento sube más de un 3%.
- **DOWN:** El segmento baja más de un 3%.
- **FLAT:** El cambio es inferior al 3% (consolidación lateral).

Una secuencia de segmentos es lo que RadarCore llama las **Eras** de una acción. La secuencia de eras es la "historia" de la acción explicada en palabras simples.

**Ejemplos de secuencias:**
```
UP-UP-UP               → Tendencia alcista clara (RISE)
DOWN-DOWN-UP-DOWN-UP   → Oscilación con potencial de swing (SWING)
DOWN-FLAT-FLAT-FLAT    → Caída y base lateral (L-BASE / LATERAL)
UP-DOWN-UP-DOWN        → Swing regular (SWING)
```

**En la UI verás:** `Last segment FLAT (-0.6%) · Second-to-last UP (+3.8%) · Recovery at 24% of peak-valley range · Valley 0 days ago`

Esto te dice: el último movimiento estructural es lateral (consolidación), el anterior fue una subida del 3.8%, y la acción ha recuperado el 24% del camino desde su mínimo hasta el máximo previo.

---

# PARTE 4 — El sistema de clasificación de RadarCore

## Capítulo 13: Los Cinco Buckets (Categorías)

RadarCore clasifica cada acción en una de las cinco categorías estructurales. No es un sistema binario (oportunidad sí/no), sino una clasificación de en qué "estado" se encuentra la acción.

### SWING 🔄
La acción muestra un patrón de oscilación: ha subido, ha bajado, y potencialmente volverá a subir. Es el patrón más buscado para swing trading. La condición esencial es que haya caído lo suficiente desde un máximo reciente y haya demostrado que el mínimo ya ha quedado atrás con un rebote inicial.

**Subtipos de SWING:**
- **SWING → BREAKOUT:** La acción acaba de superar su último máximo local significativo. Señal de fuerza, pero hay que vigilar que no sea una trampa.
- **SWING → PULLBACK:** Después de un breakout, la acción ha retrocedido un poco. Si el retroceso se mantiene por encima del soporte, puede ser una segunda oportunidad de entrada mejor que el breakout original.
- **SWING → RETEST:** La acción ha vuelto a testear el nivel de su mínimo anterior (sin romperlo). Si el soporte aguanta, es una confirmación muy potente.

### RISE 📈
La acción está en una tendencia alcista clara y sostenida. No hay grandes oscilaciones: simplemente sube de manera consistente. Para swing trading puro es menos interesante (ya no tiene la caída previa), pero indica una empresa con fuerte momentum que puede seguir subiendo.

**Subtipos de RISE:**
- **RISE → BREAKOUT:** Superando nuevos máximos anuales. Muy fuerte, pero puede estar "demasiado cara".
- **RISE → PULLBACK:** Retroceso dentro de una tendencia alcista. Puede ser un punto de entrada para los que creen en la continuación de la tendencia.

### LATERAL 〰️
La acción no hace nada: se mueve en un rango estrecho sin tendencia clara ni arriba ni abajo. Puede estar "acumulando" (preparándose para subir) o simplemente dormida. Por sí solo no es una señal de acción, pero si viene precedido de una caída es lo que RadarCore llama **L-BASE**.

### HIGHS 🔝
La acción cotiza cerca de su máximo reciente. Alto riesgo de corrección. RadarCore la marca por información pero no la considera una oportunidad de "Buy the Recovery" (no hay caída previa desde donde recuperarse).

### DESCENDING 📉
La acción está en una tendencia bajista clara. El mercado le da la espalda. Evitarla para compras. Puede ser interesante para ventas en corto (*short selling*), pero esto es una estrategia avanzada fuera del alcance de esta guía.

---

## Capítulo 14: Las Fases de Trazo — ¿Dónde estás dentro del recorrido?

Saber que una acción es SWING es útil, pero no te dice si estás entrando al principio de la recuperación o cuando ya se ha movido mucho. Las **fases** responden exactamente a esta pregunta.

### La fórmula del Progress

```
Progress % = (Precio actual - Mínimo del Pivot) 
             / (ATH 3 años - Mínimo del Pivot) × 100
```

Esta fórmula mide cuánto del recorrido posible ya se ha recorrido. Si el máximo de los últimos 3 años es $100 y el mínimo del pivot fue $60, y ahora la acción está a $70:

```
Progress = (70 - 60) / (100 - 60) × 100 = 25%
```

La acción ha recorrido el 25% del camino posible entre su mínimo y su máximo anterior.

### Las cuatro fases

**🟢 VALLEY (< 20% de progress)**
La acción acaba de rebotar del mínimo. Tienes la máxima distancia para recorrer hasta el máximo anterior (el máximo upside posible). Pero también el máximo riesgo: no sabes si el rebote es real o un dead cat bounce (rebote temporal antes de seguir bajando).

*Cuándo es buena opción:* Cuando el patrón es L-BASE, el volumen acompaña y la caída es idiosincrásica.

**🟡 MID (20%-65% de progress)**
La recuperación ya lleva un cierto camino. La tendencia alcista empieza a estar confirmada por los mercados. Te queda recorrido hasta el máximo anterior pero has perdido la parte inicial. Es el **"sweet spot"** que Trazo y RadarCore consideran el mejor equilibrio entre riesgo y oportunidad.

*Cuándo es buena opción:* Casi siempre. La relación riesgo/recompensa es la mejor de estas cuatro.

**🟠 MATURE (65%-85% de progress)**
La acción ha recuperado la mayor parte del terreno perdido. El recorrido restante hasta el máximo es limitado. El riesgo de una nueva corrección es elevado porque muchos inversores que compraron a precios altos ahora tienen la oportunidad de "recuperar lo que habían perdido" y venden.

*Cuándo tener cuidado:* Observa el volumen. Si la subida se hace con volumen decreciente, puede ser una trampa.

**🔴 LATE (> 85% de progress)**
La acción ya ha vuelto casi al máximo anterior. Poco margen de subida adicional, mucha presión vendedora. RadarCore la muestra por información pero no la considera candidata para una nueva entrada.

### Upside: cuánto le queda por subir

En la tabla de resultados verás **Upside 3Y** y **Upside 5Y**. Estos porcentajes indican cuánto podría subir la acción si volviera a su máximo de los últimos 3 o 5 años.

```
Upside 3Y = (ATH 3 años - Precio actual) / Precio actual × 100
```

Una acción con Phase VALLEY y Upside 3Y del 40% es mucho más interesante que una con Phase LATE e Upside 3Y del 5%.

---

## Capítulo 15: La Confianza (Confidence) — ¿cómo se calcula?

El **Confidence %** que ves en la columna **Conf.** es una puntuación compuesta que RadarCore calcula para ordenar las oportunidades de mejor a peor. No es magia: es la suma ponderada de cuatro factores.

### Las cuatro componentes de la Confianza

**1. Calidad de la Caída (30% del total)**
Cuanto más cercana al 40% sea la caída real (de máximo a mínimo), mayor puntuación. Una caída del 20% recibe menos puntos que una del 35%. Porque caídas mayores implican "descuentos" mayores y potencial de recuperación superior.

```
Puntuación = min(Drop% / 40%, 1.0) × 0.30
```

**2. Calidad del Rebote (20% del total)**
Un rebote entre el 5% y el 10% desde el mínimo es el más valorado. Demasiado poco (<2%) no confirma el giro. Demasiado (>15%) puede significar que ya hemos perdido la mejor entrada.

```
Puntuación = min(Rebound% / 10%, 1.0) × 0.20
```

**3. Forma del Patrón (25% del total)**
- **L-BASE o LATERAL:** Máxima puntuación (0.25). La base lateral sugiere acumulación institucional.
- **V-RECOVERY o SWING:** Puntuación media (0.15). La recuperación rápida es menos predecible.
- **EARLY:** Puntuación baja (0.05). Demasiado incipiente para confiar.

**4. Contexto de Mercado (25% del total)**
- **Caída idiosincrásica confirmada:** 0.25 puntos. La caída es específica de la empresa.
- **Datos de mercado no disponibles:** 0.10 puntos. Beneficio de la duda.
- **Caída sistémica:** 0 puntos. El mercado lo explica todo.

**Ejemplo práctico:**
```
MSFT: Drop 26% → 0.195 | Rebound 17% → 0.20 | 
      Patrón V-RECOVERY → 0.15 | Idiosincrásica ✅ → 0.25
      
Confidence = (0.195 + 0.20 + 0.15 + 0.25) × 100 = 79.5%
```

---

## Capítulo 16: Stop Loss, Targets y el Ratio R/R

### Stop Loss: protegiendo el capital

El **Stop Loss (SL)** es la orden automática de venta que ponemos para limitar las pérdidas si nos equivocamos. No es una derrota: es una parte integral de cualquier estrategia profesional.

**Regla fundamental del trading:** Preservar el capital es prioridad absoluta. Una pérdida del 50% requiere una ganancia del 100% para recuperarse. Una pérdida del 10% solo necesita una ganancia de el 11%.

```
Stop Loss = Mínimo del Pivot - (ATR × 1.5)
```

Usamos 1.5 veces el ATR porque el precio puede hacer movimientos normales dentro de su volatilidad habitual sin que la tesis de inversión se haya roto. Si el stop estuviera demasiado ajustado, saltaría por ruido normal.

**El nivel de invalidación:** Si el precio cae por debajo del Stop Loss, la tesis "Buy the Recovery" ya no es válida. El precio ha roto el soporte donde se había formado el patrón. Salir rápido y buscar la próxima oportunidad.

### Targets: recogiendo ganancias

**T1 (Target 1 — Objetivo Conservador):**
El primer punto de toma de beneficios. En RadarCore suele estar marcado alrededor del 85% de la distancia entre el mínimo y el máximo anterior. En este punto, muchos swing traders venden la mitad de la posición para asegurar ganancias y dejan el resto "correr" hacia el T2.

**T2 (Target 2 — Objetivo Ideal):**
El máximo anterior a la caída. Es el objetivo natural de "Buy the Recovery": si la empresa recupera todo el terreno perdido, el precio volvería a donde estaba antes. En la práctica, muchas recuperaciones no llegan al 100% pero sí al 70-80%.

### El Ratio Riesgo/Recompensa (R/R)

Este es el concepto **más importante** para la supervivencia financiera a largo plazo.

```
Ratio R/R = (Target - Entrada) / (Entrada - Stop Loss)
```

**Ejemplo:**
```
Entrada: $100
Stop Loss: $92  → Riesgo = $8
Target (T2): $125 → Recompensa = $25
Ratio R/R = 25 / 8 = 3.1x
```

Un ratio de 3.1x significa que por cada dólar que arriesgas, puedes ganar 3.1$. RadarCore considera como mínimo aceptable un R/R de 2.0x.

**La magia del R/R:** Imagina que haces 10 operaciones con R/R de 2x:
- 6 salen mal: pierdes 6 × $1 = -$6
- 4 salen bien: ganas 4 × $2 = +$8
- Resultado neto: +$2 **¡sin haber acertado ni la mitad!**

Con un buen R/R, puedes ser rentable incluso acertando menos del 50% de las operaciones.

---

## Capítulo 16b: Cómo leer Finviz — tu panel de control rápido

Cuando RadarCore detecta una oportunidad y haces clic en el botón **📊 Finviz** de la tabla de resultados, se abre una página que concentra mucha información en un solo lugar. Aquí te explico dónde mirar y en qué orden, para no perderse.

### ¿Qué es Finviz?

Finviz (Financial Visualizations) es una herramienta gratuita de visualización financiera usada por traders profesionales y particulares. Su página para cada ticker combina en un solo panel los datos fundamentales de la empresa, los indicadores técnicos y las noticias recientes. Para swing trading es probablemente la herramienta de "primer vistazo" más eficiente que existe.

### El circuito de lectura: 4 miradas en 2 minutos

#### Primera mirada — El gráfico (derecha de la página)

Mira el gráfico antes que cualquier número. Tu cerebro es muy bueno detectando patrones visuales, y el gráfico te confirma o desmiente lo que RadarCore ha detectado.

Busca:
- **La forma del patrón:** ¿Ves la caída y el rebote que RadarCore ha detectado? Si el gráfico muestra una línea que simplemente baja sin ninguna señal de giro, desconfía.
- **Dónde está el precio hoy:** ¿Cerca del máximo o del mínimo reciente?
- **Las barras de volumen** (debajo del gráfico): Las barras más altas indican días con mucha actividad. Si el día del giro tenía una barra muy alta, es una señal de convicción.

#### Segunda mirada — Los números clave (tabla superior izquierda)

Aquí encontrarás una tabla con muchos campos. Para swing trading, ignora la mayoría y céntrate en estos:

| Campo de Finviz | Nombre completo | Para swing trading |
|-----------------|-----------------|-------------------|
| **P/E** | Price-to-Earnings | Mide si la empresa es "cara". < 30 es razonable. "N/A" puede indicar pérdidas |
| **EPS next Y** | Beneficio por acción previsto | Debe ser positivo. Indica si la empresa crecerá |
| **Short Float** | % de inversores apostando a la baja | > 20% es peligro. Mucha gente cree que bajará |
| **RSI (14)** | Indicador de fuerza relativa | 30-70 es la zona saludable para entrar |
| **Perf Week** | Rendimiento de la semana | Confirma o contradice el rebote de RadarCore |
| **Volume / Avg Volume** | Volumen hoy vs habitual | > 1.5x indica interés institucional |
| **52W High / Low** | Rango del año | Te sitúa el precio en contexto anual |

**Cómo leer el campo "Short Float":**
Si el Short Float es del 25%, significa que el 25% de las acciones disponibles están "prestadas" por inversores que apuestan a que el precio bajará. Un Short Float alto es un riesgo: si la acción sube a pesar de las apuestas en contra, puede producirse un "short squeeze" (subida muy rápida), pero también puede indicar que profesionales del mercado ven problemas que tú no ves.

#### Tercera mirada — La sección de noticias (parte inferior)

Finviz muestra los titulares de los últimos días ordenados por fecha. **Lee los titulares de las últimas 48-72 horas.** Busca:

- **Resultados financieros recientes:** Si la empresa ha publicado resultados en los últimos días, el movimiento de precio puede estar relacionado.
- **Cambios de directivo:** Un nuevo CEO o CFO puede cambiar el rumbo de la empresa.
- **Fusiones o adquisiciones:** Cambian completamente la tesis de inversión.
- **Noticias sectoriales:** Una regulación nueva que afecte a todo el sector.

Si ves noticias positivas recientes que coinciden con el rebote detectado por RadarCore, es una confirmación de calidad. Si las noticias son negativas pero el precio rebota, entiende por qué.

#### Cuarta mirada — Los analistas (si quieres profundizar)

- **Target Price:** El precio objetivo de los analistas de Wall Street
- **Analyst Recom.:** La recomendación agregada (Buy / Hold / Sell)

Estos campos no son definitivos, pero si la recomendación es "Strong Sell" y RadarCore detecta una oportunidad, vale la pena saberlo.

### Ejemplo práctico de lectura de Finviz

RadarCore detecta MSFT como SWING en fase MID. Abres Finviz y ves:
- **Gráfico:** Clara caída desde 450$ hasta 380$ y rebote a 410$. La forma coincide con el patrón detectado ✅
- **P/E 31:** Ligeramente alto pero razonable para Microsoft ✅
- **RSI 52:** En zona neutral, ni sobrecomprado ni sobrevendido ✅
- **Short Float 0.6%:** Casi nadie apuesta a la bajada ✅
- **Perf Week +3.2%:** El rebote que RadarCore ha detectado es real y reciente ✅
- **Noticia reciente:** "Microsoft raises Azure guidance for Q4" ✅

**Conclusión:** Todo confirma la tesis de RadarCore. Es un buen candidato para profundizar.

---

## Capítulo 16c: El botón SEC Filings — la fuente primaria de toda la información

Cuando haces clic en el botón **🏛️ SEC Filings** de RadarCore, se abre la base de datos oficial de la SEC para esa empresa.

### ¿Qué es la SEC y por qué importa?

La **SEC** (Securities and Exchange Commission) es el equivalente americano de la CNMV española: el organismo gubernamental que regula los mercados financieros de los Estados Unidos. Todas las empresas que cotizan en bolsas americanas están **obligadas por ley** a publicar información sobre cualquier hecho que pueda afectar el precio de sus acciones.

Esta información se publica en el sistema **EDGAR** (Electronic Data Gathering, Analysis, and Retrieval) de la SEC, que es público y gratuito.

La importancia para ti: **la SEC es la fuente primaria de toda la información oficial**. Yahoo Finance, Bloomberg, CNBC — todos obtienen la información de la SEC.

### El documento más importante: el formulario 8-K

El **8-K** es la obligación que tiene la empresa de notificar cualquier "hecho material" en un plazo de 4 días hábiles.

**Ejemplos de 8-K que puedes encontrar:**

| Tipo de 8-K | Significado | Impacto en el precio |
|-------------|-------------|---------------------|
| Resultados financieros (Earnings) | La empresa publica los números del trimestre | Puede subir o bajar mucho |
| Cambio de CEO o CFO | Un directivo clave entra o sale | Incierto, depende del motivo |
| Adquisición de otra empresa | Compran o son comprados | Suele subir si compran |
| Emisión de nuevas acciones | Venden acciones nuevas para captar capital | Suele bajar (dilución) |
| Demanda judicial importante | La empresa es demandada o demanda | Depende de la gravedad |

### Cuándo debes abrir SEC Filings

**Siempre que:**
- RadarCore detecta una caída grande (>25%) y no entiendes por qué ha caído
- Quieres saber si ha pasado algo importante en los últimos 30 días
- Finviz muestra una noticia reciente que no entiendes del todo

**El flujo recomendado:**
1. RadarCore detecta la oportunidad
2. Abres Finviz → miras el gráfico y los números
3. Si las noticias mencionan algo importante, abres SEC Filings para leer el 8-K oficial
4. Con toda esta información, decides si la tesis es sólida o si hay factores de riesgo que RadarCore no puede detectar

### Otros documentos útiles de la SEC

- **10-K:** El informe anual completo. La sección "Risk Factors" es valiosa.
- **10-Q:** El informe trimestral. Más frecuente que el 10-K.
- **Form 4:** Compras y ventas de acciones por parte de los directivos. Si el CEO compra muchas acciones propias, es una señal positiva.

---

## Capítulo 17: Los Earnings — el riesgo más importante del swing trading

### ¿Qué son los Earnings?

Cada trimestre (cuatro veces al año), las empresas cotizadas publican sus resultados financieros oficiales. Ingresos, beneficios, perspectivas futuras... Esta publicación se llama **Earnings Report** (informe de resultados).

El mercado suele tener expectativas sobre los resultados. Si la empresa las supera → el precio puede subir un 10-20% en un día. Si las defrauda → puede caer un 10-20% en un día.

### ¿Por qué los Earnings son peligrosos para el swing trading?

Porque **la dirección del movimiento es imprevisible hasta el último momento**, incluso para los profesionales. Ni el análisis técnico ni el patrón del gráfico te puede decir si los resultados serán mejores o peores que las expectativas.

Si tienes una posición abierta y salen los Earnings mientras la tienes, estás apostando sin saber ni cara ni cruz. Esto es especulación pura, no swing trading.

### ¿Cómo gestiona RadarCore los Earnings?

RadarCore muestra en la UI el badge de aviso:
- **⚠️ EARN Xd (rojo):** Earnings en menos de 14 días. Riesgo muy alto. Considera esperar.
- **📅 EARN Xd (amarillo):** Earnings en 15-30 días. Aviso. Vigila el timing.
- **earn Xd (gris):** Earnings en 31-60 días. Información para planificar.

**Estrategia recomendada:** Si una oportunidad tiene Earnings en menos de 14 días, tienes dos opciones:
1. **No entrar** hasta que los Earnings hayan pasado (i.e., el precio se haya estabilizado).
2. **Entrar con posición muy reducida** (menos de lo que pondrías normalmente) para limitar la exposición a la incertidumbre.

---

# PARTE 5 — Usar RadarCore paso a paso

## Capítulo 18: La Sidebar — configuración global

La **sidebar** (panel lateral izquierdo) contiene las configuraciones globales que afectan a cómo la IA analiza las oportunidades.

**AI Provider:** Elige entre Google Gemini (por defecto y recomendado) u OpenAI (GPT-4o). Afecta a la calidad y el estilo de los informes generados.

**Model:** El modelo específico dentro de cada proveedor. Para uso habitual, el modelo por defecto es suficiente.

**API Key Settings:** Si tienes tus propias claves de API, las puedes introducir aquí. No es obligatorio para las funciones básicas.

**AI Report Language:** El idioma en el que la IA redactará los informes: Catalán, Castellano o Inglés.

**Analysis Mode:**
- **Automatic mode (ON):** Todas las oportunidades detectadas pasan automáticamente por el análisis avanzado de patrones. Recomendado mientras aprendes.
- **Automatic mode (OFF):** Activa el Modo Watchlist. Solo se analizan en profundidad los tickers que tú has seleccionado manualmente en la pestaña Watchlist.

**Pre-filter universe:** Activa un filtro adicional que elimina empresas zombie (sin historial de recuperación) y empresas con liquidez insuficiente. Recomendado tenerlo desactivado mientras aprendes para ver más resultados; activarlo cuando quieras resultados de más calidad.

---

## Capítulo 19: Pestaña Market Scanner — haciendo el primer escaneo

Esta es la pantalla principal. Aquí configuras los parámetros y lanzas el escaneo.

### Seleccionar el Mercado (Market to Scan)

Elige entre los siete mercados disponibles:

| Mercado | Recomendado para... |
|---|---|
| S&P 500 (USA) | Primer aprendizaje. Empresas muy conocidas. |
| NASDAQ 100 (USA) | Interesado en tecnología |
| IBEX 35 (Spain) | Empresas españolas cercanas |
| DAX 40 (Germany) | Empresas europeas industriales |
| EuroStoxx 50 | Diversificación europea |
| Nikkei 225 | Exposición a Japón |
| Nifty 50 | Mercado emergente, India |

**Recomendación para principiantes:** Empieza con S&P 500. Las empresas te serán familiares (Apple, Microsoft, Visa...) y hay mucha información disponible para aprender.

### Symbol Limit

Pon 0 para analizar todas las empresas del mercado, o un número pequeño (20-50) para hacer pruebas rápidas. Con 0 y el S&P 500 el escaneo puede tardar 30-60 segundos.

### Strategy Parameters — los sliders de la estrategia

**Minimum Drop (%) — por defecto 15%:**
Cuánto debe haber caído la acción desde su máximo reciente. Con 15%, buscas empresas que hayan perdido al menos un 15% de su valor. Si pones muy alto (>30%), verás pocas empresas pero en situación de "gran descuento". Si pones bajo (<10%), verás muchas empresas pero algunas con caídas poco significativas.

*Recomendación inicial:* 15% es un buen punto de partida. En mercados alcistas quizás hay que bajar a 10%. En mercados bajistas, las oportunidades aparecerán naturalmente a 20-30%.

**Historical Window (Days) — por defecto 60:**
En cuántos días atrás miramos el máximo de referencia. Con 60 días, el máximo es el más alto de los últimos 2 meses. Con 252 días (un año), el máximo es el anual. Ventanas más largas detectan caídas estructurales mayores; ventanas cortas detectan caídas recientes menores.

*Recomendación inicial:* 60 días para swing trading de 2-6 semanas. 120-252 días para posiciones de recuperación a largo plazo.

**Minimum Rebound (%) — por defecto 2%:**
El rebote mínimo desde el mínimo que confirma que la caída se ha detenido. Con 2%, es muy permisivo (cualquier pequeño giro). Con 8-10%, exiges una recuperación ya en marcha pero te pierdes la entrada inicial.

*Recomendación inicial:* 2-5% para capturar oportunidades en fase VALLEY. 5-10% si prefieres más confirmación y no importa perder parte del movimiento inicial.

**Min Mkt Cap (B $) — por defecto $10B:**
Filtra por capitalización de mercado mínima. $10B elimina la mayoría de small-caps especulativas. Para los que quieran explorar empresas más pequeñas (con más riesgo), se puede bajar a $2-5B.

**Min Avg Vol (M) — por defecto 1M acciones/día:**
Volumen medio mínimo. La liquidez es esencial: necesitas poder comprar y vender sin que tu orden mueva el precio. 1M acciones/día es el mínimo razonable para empresas large-cap.

### El botón Run Scan

Al pulsar **Run Scan**, RadarCore:
1. Descarga los datos de precio de cada empresa del mercado seleccionado.
2. Aplica el filtro de universo (si está activo).
3. Calcula el Drop % y el Rebound % para cada empresa.
4. Aplica los filtros de Strategy Parameters.
5. Para las que pasan los filtros, ejecuta el PatternClassifier (RDP + Eras + Buckets).
6. Calcula la Fase (VALLEY, MID, MATURE, LATE).
7. Detecta los Earnings próximos.
8. Guarda los resultados en la base de datos y los muestra en la UI.

---

## Capítulo 20: Pestaña History & Reports — interpretando los resultados

Aquí es donde ves, analizas y gestionas las oportunidades detectadas.

### La tabla de resultados

Cada fila es una empresa que ha pasado todos los filtros. Las columnas:

**Symbol:** Código de la empresa. Haz clic para ir a Yahoo Finance y ver su información completa.

**Company:** Nombre completo de la empresa.

**Drop %:** La caída real desde el máximo reciente hasta el mínimo. *Regla práctica: a más drop, más "descuento" pero también más riesgo de que la tesis no se cumpla.*

**Rebound %:** Cuánto ha subido desde el mínimo hasta hoy. *Un rebound del 5-15% en un VALLEY es ideal. Más del 30% en VALLEY puede ser excesivo (quizás ya hemos perdido la entrada).*

**Pattern:** El tipo de patrón detectado. Recordatorio rápido:
- SWING / L-BASE / V-RECOVERY → Candidatos para Buy the Recovery
- RISE → Tendencia alcista, no es "Buy the Recovery" pero puede ser interesante
- LATERAL → Acumulación posible, vigilar
- DESCENDING / HIGHS → Evitar por ahora

**Phase:** Dónde estamos dentro del recorrido. 🟢 VALLEY es el mejor momento, 🔴 LATE es demasiado tarde.

**Upside 3Y:** Cuánto podría subir si volviera al máximo de los últimos 3 años. Más del 20% es interesante.

**Conf.:** La puntuación compuesta de calidad. Ordena por esta columna de mayor a menor para ver las mejores oportunidades primero.

**Date:** Cuándo se detectó la oportunidad. Oportunidades de hace muchos días pueden haber cambiado de situación.

### Los gráficos

Selecciona una o más filas y pulsa **View Charts** para ver la representación visual.

**Vista Mountain:** La línea dorada del precio sobre fondo negro. Ideal para ver la tendencia global de manera limpia.

**Vista Eras:** Zonas coloreadas que muestran cada segmento del algoritmo RDP:
- Zonas verdes → Segmentos UP
- Zonas rojas → Segmentos DOWN
- Zonas grises → Segmentos FLAT

**Vista Pivots:** La línea discontínua blanca de los puntos clave (P1, P2... para los picos; T1, T2... para los valles) sobre la línea de precio. Te permite ver la estructura sin ruido.

**Vista Candles:** El gráfico de velas japonesas tradicional (OHLCV completo). Cada vela representa un día: verde si el precio ha subido, roja si ha bajado.

**La cabecera del gráfico** (texto pequeño sobre el gráfico): Te da información contextual importante como `Last segment UP (+3.8%) · Recovery at 24% of peak-valley range · Valley 0 days ago · RETEST`. Léela siempre como primer resumen.

**El panel Trazo Phase Analysis:** Muestra la Phase, el Progress %, el Upside 3Y, el Upside 5Y y el precio del Pivot (el mínimo del patrón). Úsalo para entender inmediatamente dónde estás dentro del recorrido posible.

---

## Capítulo 21: Pestaña Watchlist — curando manualmente las oportunidades

La **Watchlist** es el paso de curación manual que Trazo considera esencial. Funciona así:

1. El escaneo te da, por ejemplo, 25 oportunidades.
2. Miras rápidamente los gráficos de cada una (30 segundos por gráfico = 12 minutos).
3. Las que visualmente te convencen (buen patrón, buena forma) las añades a la Watchlist.
4. Sobre las de la Watchlist, haces el análisis profundo: generas el informe de IA, miras los fundamentales en Yahoo Finance, compruebas el contexto sectorial.

### Mode Automático vs. Mode Watchlist

**Modo Automático (recomendado para principiantes):** Todas las oportunidades pasan por el análisis completo. Ideal mientras estás aprendiendo y quieres ver cómo funciona el sistema.

**Modo Watchlist (recomendado cuando tengas experiencia):** Separas la detección (algoritmo) de la selección final (tú). Warren (el autor del sistema que ha inspirado parte de RadarCore) dice que él pasa 1 hora en Yahoo Finance sobre las que su bucketer selecciona. Trazo hace una primera elección visual manual. Ambos coinciden en que el ojo humano añade valor sobre el algoritmo.

---

## Capítulo 22: Pestaña Investor Knowledge — personalizando la IA

Aquí puedes subir tus propios PDFs de filosofía inversora para entrenar a la IA. Si tienes un libro de Warren Buffett, un artículo de análisis que te ha gustado, o tus propios apuntes de inversión, la IA los incorporará a sus informes para darte respuestas más alineadas con tu filosofía.

Ejemplos de documentos que puedes subir:
- Resúmenes de estrategias de swing trading
- Notas sobre sectores que te interesan
- Criterios personales de entrada y salida
- Artículos sobre empresas específicas

---

# PART 6 — Poniéndolo todo junto: el flujo completo de una operación

## Capítulo 23: Del escaneo a la decisión

### Paso 1: Configuración (5 minutos)

Abre RadarCore. En la sidebar, verifica que el idioma es el que quieres y que el modo es Automático. En Market Scanner, selecciona S&P 500. Deja los parámetros por defecto la primera vez.

### Paso 2: El escaneo (30-60 segundos)

Pulsa Run Scan. Mira los logs que aparecen mientras escanea. Verás las empresas que pasan o fallan los filtros. Cuando acabe, ve a History & Reports.

### Paso 3: Primera revisión de la tabla (5-10 minutos)

Ordena por Conf. descendente. Mira las primeras 10 filas. Filtra por SWING o LATERAL si quieres concentrarte en los patrones de recuperación.

Elimina mentalmente:
- Cualquier cosa con Phase LATE o MATURE (ya ha subido demasiado)
- Las que tengan ⚠️ EARN en menos de 14 días (si no quieres asumir el riesgo)
- Las DESCENDING (evitar para compras)

### Paso 4: Revisión visual de los gráficos (2 minutos por empresa)

Para cada una de las candidatas que quedan, pulsa View Charts. Mira:
1. Vista Mountain: La tendencia general. ¿Sube o baja de manera limpia?
2. Vista Pivots: ¿El patrón es claro? ¿Se ve la V o la L?
3. Cabecera: ¿Qué segmento es el último? FLAT es buen (base), DOWN es malo.
4. Trazo Phase Analysis: ¿Dónde está el Progress? ¿El Upside 3Y es atractivo?

### Paso 5: Análisis profundo de las candidatas (10-20 minutos)

Para las 3-5 empresas que han superado la revisión visual, genera un **informe de IA** (Generate Reports). La IA te explicará el contexto fundamental, los riesgos no técnicos (deuda, competencia, regulación) y si hay razones para no entrar.

A la vez, haz clic en el Symbol en la tabla para ir a Yahoo Finance. Mira:
- La sección de noticias recientes: ¿hay alguna razón clara para la caída?
- El "Summary" de la página: la capitalización, el P/E ratio, el dividendo.
- Los Earnings: ¿cuándo es el próximo? ¿Coincide con lo que RadarCore ha marcado?

### Paso 6: La decisión (tú, no el algoritmo)

RadarCore detecta. Tú decides. Hazte estas preguntas:
1. ¿Entiendo por qué ha caído esta empresa?
2. ¿Creo que los motivos de la caída son temporales?
3. ¿La empresa seguirá existiendo y prosperando de aquí a 6 meses? ¿Y a 2 años?
4. ¿El Ratio R/R (de Stop Loss a Target) justifica el riesgo?
5. ¿Si cae hasta el Stop Loss, estaré cómodo habiéndolo perdido?

Si las respuestas a todo esto son sí, tienes una tesis de inversión sólida. Si dudas en alguna, es mejor esperar.

---

## Capítulo 24: La Regla de Oro — Gestión del riesgo y diversificación

Ningún sistema de detección es perfecto. RadarCore te da probabilidades, no certezas. Para sobrevivir (y prosperar) a largo plazo, la gestión del riesgo es más importante que cualquier señal concreta.

### Regla 1: Nunca todo en una sola posición

Si pones todo tu capital en una empresa y sale mal, has perdido todo. Si lo distribuyes en 10 operaciones y una sale mal (y salta el Stop Loss), has perdido el 10% de una parte del capital.

**Recomendación:** Entre 8 y 15 posiciones simultáneas. Máximo un 10-15% del capital total en una sola empresa.

### Regla 2: Define el Stop Loss ANTES de entrar

Decide dónde saldrás si te encuentras equivocado ANTES de comprar. Si no lo haces, la psicología del mercado te lo hará imposible una vez estás dentro. "Esperaré a que rebote" es la frase que ha arruinado a muchos inversores.

### Regla 3: El R/R mínimo es 2x

Si la operación no tiene al menos el doble de recompensa posible respecto al riesgo asumido, no es una buena operación para swing trading.

### Regla 4: Acepta las pérdidas rápido, deja correr las ganancias

¿Salta el Stop Loss? Sal sin dudar. El mercado nunca te debe una recuperación. Pero si una posición va a favor, no la cierres por miedo: deja que llegue al T1 y decide entonces.

### Regla 5: No inviertas lo que no puedes permitirte perder

Todos los conceptos anteriores no valen de nada si el capital que inviertes es el que necesitas para pagar el alquiler del mes próximo. La presión emocional de necesitar el dinero toma las peores decisiones posibles.

---

## Glosario rápido

| Término | Definición simplificada |
|---|---|
| Acción | Trozo de propiedad de una empresa cotizada |
| ATH | All-Time High. El precio máximo histórico de una acción |
| ATR | Average True Range. Medida de la volatilidad diaria típica |
| Bolsa | Mercado electrónico donde se compran y venden acciones |
| Bucket | Categoría estructural de una acción (SWING, RISE, etc.) |
| Caída idiosincrásica | Caída específica de una empresa, no del mercado general |
| Drawdown | Caída porcentual desde un máximo hasta un mínimo posterior |
| Earnings | Resultados financieros trimestrales de una empresa |
| EMA | Exponential Moving Average. Media móvil que da más peso a los precios recientes |
| Era | Segmento del gráfico clasificado como UP, DOWN o FLAT |
| Índice | Cesta de empresas que representa un mercado (S&P 500, IBEX 35...) |
| Inflación | Pérdida de poder adquisitivo del dinero con el tiempo |
| L-BASE | Patrón de caída seguida de base lateral. Signo de acumulación |
| Liquiditad | Facilidad para comprar o vender una acción sin mover el precio |
| Market Cap | Capitalización de mercado. Valor total de una empresa en bolsa |
| OHLCV | Open, High, Low, Close, Volume. Los cinco datos diarios de una acción |
| Pivot | Punto clave de giro en el gráfico (Peak o Trough) |
| Ratio R/R | Ratio Riesgo/Recompensa. Cuantifica si una operación vale la pena |
| RDP | Ramer-Douglas-Peucker. Algoritmo para simplificar el gráfico eliminando ruido |
| Rebote | Subida del precio desde su mínimo. Confirma el giro |
| RSI | Relative Strength Index. Indicador de sobrecompra/sobreventa (0-100) |
| Stop Loss | Orden automática de venta para limitar pérdidas |
| Swing Trading | Estrategia de inversión en horizonte de días a semanas |

---

### Agradecimientos y Méritos
Este software ha sido elaborado gracias a la inspiración en el trabajo de Dani Sánchez-Crespo (https://www.skool.com/decodecore) y David Bastidas (https://www.davidbastidas.com/) además de su colaboración.
Este software ha sido programado con una intención pedagógica y gracias a Gemini y Claude.
