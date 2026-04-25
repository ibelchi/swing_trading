# RadarCore Technical Reference

This document provides a comprehensive technical reference for the RadarCore analysis system, documenting all constants, formulas, and logic derived directly from the source code.

## 1. Paràmetres de configuració globals

El sistema utilitza una combinació de paràmetres configurables des de la interfície (Streamlit) i constants definides al codi.

| Paràmetre | Valor per defecte | Rang (UI) | Ubicació | Impacte |
| :--- | :--- | :--- | :--- | :--- |
| **Minimum Drop (%)** | 10.0% | 5.0 - 50.0 | `app.py`, `BuyTheDipStrategy` | Caiguda mínima des del màxim del període per considerar l'actiu. |
| **Historical Window** | 60 dies | 20 - 250 | `app.py`, `BuyTheDipStrategy` | Període retroactiu per buscar el màxim i mínim local. |
| **Minimum Rebound (%)** | 2.0% | 0.0 - 15.0 | `app.py`, `BuyTheDipStrategy` | Rebot mínim des del mínim del període per confirmar el gir. |
| **Min Mkt Cap (B $)** | 2.0 | 0.0 - 1000.0 | `app.py`, `UniverseFilter` | Capitalització mínima per evitar "small caps" il·líquids. |
| **Min Avg Vol (M)** | 0.5M | 0.0 - 100.0 | `app.py`, `BuyTheDipStrategy` | Volum mitjà diari mínim per garantir liquiditat. |
| **Min Relative Drop** | 5.0% | *Hardcoded* | `SystemicFilter` | Diferència mínima entre la caiguda de l'actiu i l'SPY. |

## 2. BuyTheDipStrategy — Lògica de detecció

La detecció d'oportunitats es basa en el càlcul de la "caiguda i recuperació".

### Fórmules exactes
- **Drop from High (Pct)**: 
  `((period_high - period_low) / period_high) * 100`
- **Rebound (Pct)**: 
  `((current_price - period_low) / period_low) * 100`
- **Confidence Formula**:
  `confidence = (conf_drop + conf_rebound + conf_pattern) * 100`
  - `conf_drop`: `min(drop_from_high_pct / 40.0, 1.0) * 0.50` (Pes: 50%)
  - `conf_rebound`: `min(rebound_pct / 10.0, 1.0) * 0.35` (Pes: 35%)
  - `conf_pattern`: `0.15` (Pes: 15% - Valor fix per detecció tècnica bàsica)

### Condicions per `is_opportunity = True`
1. `market_cap >= min_market_cap_b`
2. `avg_volume_10d >= min_volume_m`
3. `drop_from_high_pct >= min_drop_pct`
4. `rebound_pct >= min_rebound_pct`

## 3. PatternClassifier — Classificació de buckets

El sistema classifica les oportunitats en 5 "buckets" basats en puntuacions (scorers). El desempat segueix l'ordre de la llista: **SWING, RISE, LATERAL, HIGHS, DESCENDING**.

### Condicions de Scoring

#### 🟢 SWING (Rebot des de mínims)
- **Upside ATH 3Y**: +30 pts si >= 20%, +15 pts si >= 10%.
- **Recència del mínim**: +25 pts si fa entre 5 i 30 dies, +10 pts si > 30 dies.
- **Volum**: +20 pts si el volum darrers 5 dies > mitjana 20 dies.
- **Tendència**: +10 pts si el preu darrers 5 dies ha pujat.

#### 🔵 RISE (Tendència alcista confirmada)
- **ERA Sequence**: +40 pts si darrers 3 segments són "UP", +20 pts si en són 2.
- **EMAs**: +30 pts si `Close > EMA50 > EMA200`.
- **Upside ATH 3Y**: +30 pts si > 15%.

#### 🟡 LATERAL (Consolidació o Base)
- **Range 15d**: +40 pts si rang < 5%, +20 pts si < 8%.
- **Durada**: +30 pts si la consolidació dura >= 20 dies.
- **Volum**: +30 pts si el volum darrers 5 dies és inferior a la mitjana de 20.

#### 🟠 HIGHS (A prop de màxims)
- **Distància màxim**: +50 pts si preu està a <= 2% del màxim de 60 dies.
- **RSI(14)**: +30 pts si RSI > 70.
- **Volum**: +20 pts si el volum és decreixent.

#### 🔴 DESCENDING (Tendència baixista — Evitar)
- **ERA Sequence**: +40 pts si darrers segments són "DOWN".
- **EMAs**: +40 pts si `Close < EMA50 < EMA200`.
- **Volum**: +20 pts si el volum augmenta en la caiguda.

## 4. Algorisme RDP (Ramer-Douglas-Peucker)

L'algorisme RDP s'utilitza per simplificar la corba de preus en "pivots" (pics i valls).

- **Epsilon (Sensibilitat)**: Es calcula inicialment com:
  `max(price_range * 0.03, daily_vol * avg_price * 10)`
- **Ajust Dinàmic**: El sistema ajusta l'epsilon iterativament (màx. 20 vegades) per mantenir el nombre de pivots entre **6 i 16**.
  - Si pivots > 16: `epsilon *= 1.4`
  - Si pivots < 6: `epsilon *= 0.7`
- **Visualització**: Els punts resultants es marquen com `Pn` (Pics) o `Tn` (Valls) a la gràfica.

## 5. Trazo Phase Analysis

Analitza la posició del preu respecte el cicle de recuperació de 3 anys.

- **Pivot Price**: Mínim dels darrers 90 dies.
- **ATH 3Y**: Màxim dels darrers 756 dies (252 * 3).
- **Progress %**: `(current_price - pivot_price) / (ath_3y - pivot_price) * 100`
- **Llindars de Fase**:
  - **VALLEY (Start)**: `< 20%`
  - **MID (Sweet Spot)**: `20% - 65%`
  - **MATURE**: `65% - 85%`
  - **LATE**: `>= 85%`

## 6. Filtre de mercat relatiu (SPY)

Determina si una caiguda és específica de l'empresa (idiosincràtica) o del mercat general (sistèmica).

- **Fórmula**: `relative_drop = symbol_drop - spy_drop`
- **Càlcul**: Es compara la caiguda de l'actiu amb la de l'SPY en el **mateix interval temporal** exacte (entre el màxim i mínim local de l'actiu).
- **Llindar**: Si `relative_drop <= 5%`, es considera una caiguda **sistèmica** (el mercat ha arrossegat l'actiu).

## 7. UniverseFilter (Pre-filtre de liquiditat)

S'aplica abans de l'anàlisi d'estratègia si l'usuari té activada l'opció "Pre-filter universe".

1. **Volum**: Mitjana 20 dies >= 500k accions O >= 20M$ (mitjana * preu).
2. **Història**: Mínim 126 dies de dades (~6 mesos).
3. **Market Cap**: Mínim 2.000M$ (2B$).
4. **Preu**: Preu de tancament > 5.0$.
5. **Criteri Zombie**:
   - Busca un episodi de caiguda >= 20% seguida d'una recuperació >= 50% del rang.
   - Si l'episodi és recent (darrers 2 anys / 504 dies): **PASS**.
   - Si no n'hi ha cap o són molt antics: **FAIL** (Zombie).
6. **Preu vs ATH**: El preu no pot estar a més d'un 90% de distància del seu màxim històric.

## 8. Taula de decisions del flux complet

| Pas | Filtre/Condició | Acció si es compleix | Acció si NO es compleix |
| :--- | :--- | :--- | :--- |
| **1. Data** | Ticker vàlid yfinance | Segueix al pas 2 | DESCARTAT (Download Fail) |
| **2. Universe** | Filtre de liquiditat/cap/preu | Segueix al pas 3 | DESCARTAT (Universe Filter) |
| **3. Zombie** | Recuperació històrica recent | Segueix al pas 4 | DESCARTAT (Zombie) |
| **4. L-BASE** | Consolidació estreta (<8%) | **WATCHLIST AUTOMÀTICA** | Segueix al pas 5 |
| **5. Strategy** | Drop >= X%, Rebound >= Y% | Segueix al pas 6 | DESCARTAT (Insufficient Drop/Rebound) |
| **6. Classifier** | Score de bucket > 30 | Assigna Bucket | Assigna "LATERAL" (score 20) |
| **7. Earnings** | Earnings < 7 dies | **VERDICT WAIT** (AI Report) | Segueix flux normal |
| **7. Save** | Tots els anteriors | Guardat a BD i Historial | N/A |

---

## 9. Justificació dels criteris i punts de debat

> Aquesta secció explica **per qué** existeix cada paràmetre i quines preguntes queden obertes per validar empíricament. Els valors marcats amb ⚙️ es poden canviar des de la interfície. Els marcats amb 🔒 estan fixats al codi.

### 9.1 Filtres de liquiditat bàsics

| Criteri | Valor actual | Per qué existeix | Es pot canviar? |
|---------|-------------|-----------------|----------------|
| Volum diari mínim | 500.000 accions/dia o 20M$/dia | Empreses amb poc volum son difícils de vendre quan vols sortir | ⚙️ Slider "Min Avg Vol" |
| Capitalització mínima | 2.000M$ (2 Bilions) | Empreses petites son molt volàtils i imprevisibles | ⚙️ Slider "Min Mkt Cap" |
| Preu mínim | 5,00$ | Evita "penny stocks" — accions de molt poc valor molt manipulables | 🔒 Fix al codi |
| Historial mínim | 6 mesos de dades | Sense historial no es pot calcular res | 🔒 Fix al codi |

**Pregunta per debatre:** El llindar de 2B$ de capitalització és adequat? Un valor més baix (ex: 500M$) capturaria empreses mid-cap interessants. Un valor més alt (ex: 10B$) es centraria només en empreses grans i estables.

### 9.2 El filtre zombie

RadarCore busca en els últims 5 anys si l'empresa ha tingut:
1. Una caiguda de com a mínim el **20%** des d'un màxim local
2. Seguida d'una recuperació de com a mínim el **50%** d'aquella caiguda
3. Que aquell episodi hagi passat en els **últims 2 anys**

**Pregunta per debatre:** El llindar del 50% de recuperació és el correcte? Si poses el 30% capturies més empreses però inclouries algunes que han rebotant poc. Si poses el 70% serias molt més exigent.

---

### 9.3 Fórmules de caiguda i rebot — debat de paràmetres

**Caiguda mínima (⚙️ default 10%):**
Una caiguda del 10% pot ser soroll de mercat. Una caiguda del 25-30% sol tenir una causa específica i un potencial de recuperació real.
**Pregunta:** El llindar del 10% és massa baix? Potser 15% seria un punt d'inici millor.

**Rebot mínim (⚙️ default 2%):**
Si el rebot és 0%, no sabem si la caiguda ha acabat. Un rebot confirma que el preu ha girat.
**Pregunta:** El 2% és poc? Trazo usa entre 5% i 10% per confirmar el gir. Amb 2% entres molt aviat — potencial de guany alt però risc que la caiguda segueixi. Amb 8-10% tens confirmació sòlida però entres tard.

---

### 9.4 La puntuació de confiança (Confidence) — debat de pesos

| Component | Pes | Fórmula |
|-----------|-----|---------| 
| Qualitat de la caiguda | **50%** | `min(caiguda / 40, 1.0) × 0.50` |
| Qualitat del rebot | **35%** | `min(rebot / 10, 1.0) × 0.35` |
| Detecció tècnica | **15%** | Valor fix de 0.15 |

**Exemple numèric:** Acció amb caiguda del 25% i rebot del 8%:
- Component caiguda: min(25/40, 1.0) × 0.50 = 0.625 × 0.50 = **0.3125**
- Component rebot: min(8/10, 1.0) × 0.35 = 0.80 × 0.35 = **0.280**
- Component patró: 0.15
- **Confidence = (0.3125 + 0.280 + 0.15) × 100 = 74.3%**

**Preguntes per debatre:**
1. **El pes del 50% per a la caiguda és correcte?** Una acció que cau un 40% i rebota un 1% pot treure una Confidence alta però és una senyal dolenta.
2. **El divisor de 40 per a la caiguda té sentit?** Significa que una caiguda del 40% obté la puntuació màxima. Però una del 40% és molt severa. Potser 30% hauria de ser el màxim.
3. **El component de patró fix al 15% no aporta informació.** Totes les oportunitats reben el mateix 15%, el que fa que aquest component no diferenciï.

---

### 9.5 Classificació de patrons — criteris i debat

**Ordre de desempat si dues categories empaten:** SWING > RISE > LATERAL > HIGHS > DESCENDING

**SWING — debat:**
El criteri "mínim fa entre 5 i 30 dies" (25 punts) assumeix que el timing ideal d'entrada és dins les primeres 4 setmanes del gir. Potser l'entrada òptima és més aviat o més tard.

**LATERAL — debat:**
El LATERAL pot ser tant una base de consolidació saludable com una acció que simplement no té moviment. El criteri de "volum decreixent" intenta distingir-les però és un proxy imperfecte.

**HIGHS i DESCENDING — nota:**
Un score alt en HIGHS o DESCENDING és un **senyal d'alerta**, no una oportunitat. Indica risc alt o tendència baixista.

---

### 9.6 Filtre de mercat relatiu (SPY) — debat

```
Caiguda relativa = Caiguda de l'acció - Caiguda del SPY (en el mateix interval)
```

- Si la caiguda relativa és **≤ 5%** → Caiguda **sistèmica**
- Si la caiguda relativa és **> 5%** → Caiguda **idiosincràtica**

🔒 **El llindar de 5% està fixat al codi.**

**Pregunta per debatre:** El 5% de diferència és suficient per dir que una caiguda és idiosincràtica? Si el mercat cau un 15% i l'acció cau un 20%, és idiosincràtica amb un marge de només 5 punts. Potser 8-10% seria un llindar més significatiu.

---

### 9.7 Resum dels punts de debat prioritaris

**Alta prioritat:**
1. **Minimum Drop (10% per defecte):** Massa baix? 15% capturaria oportunitats amb més recorregut i menys soroll.
2. **Confidence — pes de la caiguda (50%):** Massa alt? Una caiguda gran no implica bona oportunitat si no va acompanyada d'un rebot sòlid.
3. **Confidence — component de patró fix (15%):** No diferencia res. Caldria que reflectís el score del bucket guanyador.

**Prioritat mitjana:**
4. **Filtre zombie — recuperació del 50%:** Massa alt podria excloure empreses en recuperació inicial. Massa baix inclou zombies reals.
5. **SWING — timing 5-30 dies (25 punts):** Validat per experiència? Potser l'entrada òptima és més aviat o més tard.
6. **Llindar sistèmica/idiosincràtica (5%):** Massa permissiu? 8-10% seria més conservador.

**Prioritat baixa (interessant a llarg termini):**
7. **Llindars de fase VALLEY/MID/MATURE/LATE:** 20/65/85 estan fixats sense validació estadística.
8. **Divisor per a caiguda màxima (40%):** Una caiguda del 40% hauria de ser el màxim o ho hauria de ser el 30%?

---

*Document actualitzat: Abril 2026 · Generat a partir del codi font de RadarCore · Per a ús de revisió de criteris i debat estratègic*
