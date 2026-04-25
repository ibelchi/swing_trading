# RadarCore — Roadmap de Futures Implementacions

> Document de referència per al desenvolupament futur de RadarCore.
> Cada millora inclou la justificació, l'impacte esperat, la complexitat
> tècnica estimada i els detalls necessaris per implementar-la.
>
> **Filosofia:** Totes les implementacions segueixen el criteri KISS
> (Keep It Simple, Stupid) i han de complementar, no substituir,
> el judici humà en la decisió d'inversió final.

---

## Índex per prioritat

| Prioritat | Millora | Impacte | Complexitat |
|-----------|---------|---------|-------------|
| 🔴 Alta | Sistema de backtest sintètic | Molt alt | Alta |
| 🔴 Alta | Matriu de correlació de cartera | Alt | Baixa |
| 🟡 Mitjana | Integració de notícies (Finnhub) | Alt | Baixa |
| 🟡 Mitjana | Alertes Telegram/Email | Mitjà | Mitjana |
| 🟡 Mitjana | Seguiment de posicions obertes | Alt | Mitjana |
| 🟢 Baixa | Backtest real sobre trades propis | Molt alt | Baixa* |
| 🟢 Baixa | Control d'exposició sectorial | Alt | Mitjana |
| 🟢 Baixa | Integració EDGAR/SEC automàtica | Mitjà | Mitjana |
| 🟢 Baixa | Ajust automàtic de paràmetres (ML) | Alt | Molt alta |

*Baixa un cop tinguis 30+ trades reals registrats.

---

## 1. Sistema de Backtest Sintètic 🔴

### Per qué és la millora més important

Sense backtest, tots els paràmetres de RadarCore (el 10% de caiguda mínima, el 2% de rebot, els pesos de la Confidence, els llindars VALLEY/MID/MATURE/LATE) son opinions no validades. Trazo va descobrir que "L-Inclinada breakout" té un 17.7% de win rate — sense backtest hauria estat recomanant una estratègia fallida.

El backtest sintètic respon la pregunta: **"Si hagués aplicat l'estratègia actual als últims 3 anys, quants trades haurien funcionat i quant haurien guanyat?"**

### Limitacions importants a tenir en compte

- **Hindsight bias:** En el passat "saps" quan acaba la recuperació. En el present no.
- **Look-ahead bias:** Cal assegurar-se que els càlculs no usen informació futura.
- **Survivorship bias:** yfinance no té dades d'empreses que han desaparegut — el backtest sera optimista.
- **Slippage i comissions:** El backtest no captura la dificultat real d'entrar i sortir al preu exacte.

### Arquitectura tècnica

```
src/backtesting/
    __init__.py
    backtester.py          ← Motor principal
    signal_extractor.py    ← Detecta senyals en dades historials
    trade_simulator.py     ← Simula l'execució del trade
    results_analyzer.py    ← Calcula estadístiques
    results/               ← JSONs amb resultats guardats
```

### Lògica del backtester

```python
# Pseudocodi de la lògica principal

for ticker in universe:
    data = yfinance.download(ticker, period="3y")
    
    # Finestra rodant de 60 dies
    for window_end in range(60, len(data)):
        window = data[window_end-60:window_end]
        
        # Aplica l'estratègia actual
        result = BuyTheDipStrategy.analyze(
            ticker, window, strategy_params
        )
        
        if result["is_opportunity"]:
            entry_price = window["Close"].iloc[-1]
            entry_date = window.index[-1]
            bucket = PatternClassifier.classify(window)
            phase = PatternClassifier.analyze_phase(window)
            
            # Simula el trade: aguanta N dies
            future_data = data[window_end:window_end+hold_days]
            
            trade_result = {
                "ticker": ticker,
                "entry_date": entry_date,
                "entry_price": entry_price,
                "bucket": bucket["bucket"],
                "phase": phase["phase"],
                "final_price": future_data["Close"].iloc[-1],
                "return_pct": (final - entry) / entry,
                "hit_t1": max_price >= entry * 1.10,
                "hit_t2": max_price >= ath_3y,
                "days_to_t1": ...,
                "max_drawdown": ...,
            }
```

### Estadístiques a generar

Per a cada combinació de **bucket × fase**:

| Mètrica | Descripció |
|---------|------------|
| N deteccions | Total de senyals detectats |
| Win Rate | % que acaba positiu als N dies |
| Win Rate T1 | % que assoleix +10% |
| Win Rate T2 | % que assoleix l'ATH 3Y |
| Guany mig (winners) | Guany percentual mig quan guanya |
| Pèrdua mitja (losers) | Pèrdua percentual mig quan perd |
| Dies migs fins T1 | Velocitat de la recuperació |
| Profit Factor | Guanys totals / Pèrdues totals |
| Max Drawdown mig | Pitjor moment durant el trade |

### Resultat esperat (hipotètic)

| Bucket × Fase | Win Rate esperat | Qualitat senyal |
|--------------|-----------------|----------------|
| SWING × VALLEY | 45-55% | Alt potencial, alt risc |
| SWING × MID | 55-65% | Sweet spot ← **el que volem confirmar** |
| RISE × MID | 60-70% | Bon momentum |
| LATERAL × MID | 50-60% | Depèn del breakout |
| HIGHS × qualsevol | 30-40% | Risc alt |
| DESCENDING × qualsevol | 20-35% | Evitar |

### Integració a la UI

Nova pestanya "📈 Backtest" amb:
- Selector de mercat i dates (start/end)
- Slider "Hold days" (default 30, rang 5-90)
- Botó "Run Backtest" amb avís que triga 2-5 minuts
- Resultats en taula amb possibilitat de filtrar per bucket i fase
- Gràfica de "equity curve" simulada

---

## 2. Matriu de Correlació de Cartera 🔴

### Per qué importa

Si RadarCore detecta cinc oportunitats i quatre son empreses tecnològiques grans (MSFT, META, NVDA, AAPL), entrar en totes és equivalent a tenir una sola posició de Nasdaq. Quan el Nasdaq cau, salten els quatre stop loss simultàniament.

La correlació mesura quant es mouen juntes dues accions. Correlació 0.9 = es mouen quasi idèntiques. Correlació 0.1 = independents.

### Alertes concretes a generar

```
⚠️ Alta concentració detectada:
   MSFT ↔ META: 0.89 (molt alta)
   MSFT ↔ NVDA: 0.85 (molt alta)
   → Considera entrar en màxim 2 de les 3

📊 Correlació mitja del portfolio: 0.71
   → Alt risc en caigudes de mercat
```

---

## 3. Sistema de Seguiment de Posicions Obertes 🟡

### Justificació

RadarCore detecta oportunitats però no sap quines has executat. No pots saber si el teu "portfolio actual" de trades oberts té massa correlació o massa concentració sectorial.

### Funcionalitat

Una taula simple "My Open Positions" on registres manualment:
- Ticker, Data entrada, Preu entrada, Stop Loss, T1, T2
- Accions / Inversió total
- RadarCore calcula automàticament: P/L actual, % vs T1, % vs T2, dies obert, R/R actual

### Integració amb el full de càlcul

Exportació directa de la taula "My Open Positions" a CSV per importar al full de càlcul de swing trading existent.

---

## 4. Alertes Telegram / Email 🟡

### Justificació

RadarCore s'ha d'executar manualment. Si una oportunitat de qualitat surt al mercat dimecres a les 16:00 però no obres l'app fins al dijous, has perdut el moment òptim d'entrada.

### Arquitectura

```
src/alerts/
    alert_manager.py       ← Lògica de condicions
    telegram_sender.py     ← Integració bot Telegram
    email_sender.py        ← SMTP simple
```

### Condicions d'alerta configurable

- Nova oportunitat Top Pick detectada (SWING×MID, upside >15%)
- Oportunitat de la Watchlist entra en fase VALLEY
- RSI d'una posició oberta supera 75 (venda parcial?)
- Earnings en menys de 7 dies per a posicions obertes

### Implementació Telegram (la més simple)

1. Crear bot via @BotFather a Telegram (2 minuts)
2. Obtenir TELEGRAM_BOT_TOKEN i TELEGRAM_CHAT_ID
3. Una crida HTTP POST a `api.telegram.org` per enviar el missatge

---

## 5. Integració EDGAR/SEC Automàtica 🟢

### Justificació

Ara el botó "SEC Filings" obre el navegador. Seria molt més útil que RadarCore mostrés directament els últims 3 formularis 8-K de cada oportunitat, amb el títol i data, sense sortir de l'app.

### API pública i gratuïta

La SEC ofereix una API REST gratuïta: `https://data.sec.gov/submissions/{CIK}.json`

### Informació a mostrar

Per a cada oportunitat:
- Últims 3 formularis 8-K (títol i data)
- Data de l'últim 10-Q (resultats trimestrals)
- Alerta si hi ha un 8-K dels últims 7 dies (pot explicar la caiguda)

---

## 6. Backtest Real sobre Trades Propis 🟢

### Justificació

Un cop tinguis 30-50 trades reals registrats al full de càlcul, podràs fer el backtest més valuós de tots: comparar el que RadarCore preveia amb el que realment va passar.

### Preguntes que respondrà

- "Les oportunitats amb Confidence >70% realment guanyen més?"
- "El bucket SWING realment funciona millor que LATERAL?"
- "La fase MID realment té millor win rate que VALLEY?"
- "El meu Stop Loss del 8% és l'òptim o hauria de ser diferent?"

---

## 7. Control d'Exposició Sectorial 🟢

### Justificació

La matriu de correlació mesura com es mouen juntes les accions. El control sectorial és complementari: assegura que no tens massa exposició a un sol sector GICS (Tecnologia, Salut, Financer, Energia...).

### Implementació

```
Portfolio sector distribution:
Technology:     45% ████████████ ⚠️ Too concentrated
Healthcare:     20% ████
Financials:     15% ███
Consumer:       20% ████

Recommendation: Avoid new tech positions until
below 30% concentration.
```

El llindar recomanat: màxim 30% en un sol sector GICS.

---

## 8. Ajust Automàtic de Paràmetres (ML) 🟢

### Justificació

Un cop tinguis backtest sintètic i backtest real, pots usar Machine Learning per trobar els paràmetres òptims automàticament.

### Mètode: Bayesian Optimization

- **Funció a maximitzar:** Profit Factor del backtest sintètic
- **Paràmetres a optimitzar:** min_drop, min_rebound, pesos de Confidence, llindars de fases
- **Restriccions:** win rate > 50%, max drawdown < 15%

Llibreria Python recomanada: `optuna` (gratuïta, molt ben documentada).

> ⚠️ **Advertència:** L'ajust automàtic pot produir **overfitting**. Cal validar sempre els paràmetres òptims en un període de dades que **no** s'ha usat per entrenar.

---

## Cronograma suggerit

```
Ara (Abril 2026)
  └── Estabilitzar el sistema actual
  └── Implementar pestanya Configuration ✅
  └── Implementar matriu de correlació
  └── Integrar Finnhub (si es vol)

Maig-Juny 2026
  └── Sistema de backtest sintètic
  └── Seguiment de posicions obertes
  └── Alertes Telegram

Juliol-Setembre 2026
  └── Acumular 30+ trades reals al full de càlcul
  └── Backtest real sobre trades propis
  └── Primera revisió dels paràmetres basada en dades

A partir de tardor 2026 (si el sistema funciona bé)
  └── Control d'exposició sectorial
  └── Integració EDGAR automàtica
  └── Explorar ajust automàtic de paràmetres (ML)
```

---

## Notes sobre la filosofia del projecte

RadarCore no ha de ser un sistema que "decideixi" per tu. L'objectiu és:

1. **Filtrar el soroll:** De 500 empreses a 10-20 candidates
2. **Classificar les candidates:** Identificar el patró i la fase
3. **Contextualitzar:** Proporcionar el context macro i fonamental bàsic
4. **Facilitar la decisió:** Donar-te tots els elements per decidir tu

La decisió final sempre és humana. El backtest i els paràmetres optimitzats son eines per entendre millor el sistema, no per eliminar el judici propi.

---

*Document creat: Abril 2026 · Per a ús intern del projecte RadarCore*
*Actualitza aquest document cada cop que s'implementi una millora o canviï la prioritat.*
