# PROJECTE.md — radarcore (Swing Trading Scanner)

Document de context per a sessions d'IA. Mantingues aquest fitxer actualitzat amb cada decisió important.

## 1. Què és
**radarcore** és un escàner de mercat professional dissenyat per a l'estratègia de Swing Trading. El seu objectiu principal és automatitzar la detecció d'oportunitats basades en correccions tècniques (caigudes i rebots) en índexs globals (S&P 500, NASDAQ, IBEX 35, etc.). 

**Filosofia:**
- **Educativa:** Ajuda l'usuari a entendre el "per què" de cada senyal.
- **Modular:** Arquitectura basada en estratègies i mòduls de dades intercanviables.
- **Robustesa:** Ingesta de dades preparada per evitar bloquejos i garantir la persistència.

## 2. Stack tecnològic
| Capa | Tecnologia | Versió |
| :--- | :--- | :--- |
| **Llenguatge** | Python | 3.9+ |
| **Frontend / UI** | Streamlit | >=1.30.0 |
| **Base de Dades** | SQLite / SQLAlchemy | 2.0+ |
| **Ingesta de dades** | yfinance | 0.2.30+ |
| **Processament** | Pandas / NumPy | 2.0+ |
| **Visualització** | Plotly / TradingView | 6.0+ |
| **IA / LLM** | Google Gemini / OpenAI | Latest |
| **Framework AI** | LangChain | 0.0.6+ |

## 3. Estructura de carpetes
```text
radarcore/
├── app.py                      # Punt d'entrada de l'aplicació Streamlit
├── data/                       # Emmagatzematge persistent
│   └── radarcore.db            # Base de dades SQLite principal
├── src/                        # Codi font modular
│   ├── ai/                     # Motors de RAG i generació d'informes
│   ├── analysis/               # Càlculs avançats (correlacions, etc.)
│   ├── data/                   # Ingesta i neteja de dades
│   ├── database/               # Esquemes i gestió de sessions
│   ├── scanner/                # Lògica de l'escàner de mercat
│   ├── strategies/             # Definicions d'estratègies de trading
│   ├── ui/                     # Components visuals i gràfics
│   └── utils/                  # Utilitats transversals
├── docs/                       # Manuals d'inversió (EN/CA/ES)
└── assets/                     # Recursos visuals (logos, captures)
```

## 4. Model de dades
Esquema principal gestionat via SQLAlchemy a `src/database/db.py`:

- **`Opportunity`**: Registra cada senyal detectat.
    - `metrics` (JSON): Conté dades tècniques (RSI, drop %, rebound %).
    - `market_context` (Text): Anàlisi generat per IA sobre el context macro.
    - `confidence` (Float): Score de 0-100 basat en la qualitat del senyal.
- **`Watchlist`**: Tickers en seguiment actiu.
    - `active` (Boolean): Permet esborrat lògic (soft delete).
- **`StrategyConfig`**: Persisteix els paràmetres de l'escàner (presets).

## 5. Variables d'entorn
Necessàries per a les funcions d'IA (actualment en refactorització):
- `GOOGLE_API_KEY`: Clau per a models Gemini (Principal).
- `OPENAI_API_KEY`: Clau per a models GPT (Opcional).

## 6. Decisions d'arquitectura
- **SQLite + SQLAlchemy**: Triat per la seva simplicitat en desplegaments locals i per evitar la sobrecàrrega de servidors externs.
- **Arquitectura Anti-Bloqueig (YFinance)**: S'ha implementat una capa d'ingesta amb retards exponencials i detecció d'errors 429 per evitar banneigs d'IP.
- **Presets de l'Escàner**: Les configuracions (Conservative, Default, Aggressive) es defineixen com a diccionaris immutables per evitar efectes secundaris durant el runtime.
- **Soft Delete a la Watchlist**: No s'esborren dades físicament per mantenir un històric de l'activitat de l'usuari.

## 7. API Routes
*No s'aplica.* L'aplicació és una SPA (Single Page Application) monolítica amb Streamlit. La comunicació amb el backend és directa a través del codi de Python.

## 8. Fases del projecte
- **Fase 1: Escàner i Estratègies** ✅ Completada
- **Fase 2: Persistència i Històric** ✅ Completada
- **Fase 3: Visualització Avançada** ✅ Completada
- **Fase 4: Motor de RAG i Informes IA** 🔄 En curs (**Disseny completat**)
- **Fase 5: Backtesting Històric** ⏳ Pendent
- **Fase 6: Alertes en Temps Real** ⏳ Pendent

## 9. Workflow de desenvolupament
- **Execució:** `streamlit run app.py` o via `Start_Assistant.bat`.
- **Dependències:** Gestió via `requirements.txt` i entorn virtual `venv`.
- **Logs:** Sistema de diagnòstic a `src/logging/` per traçar errors de l'escàner.

---

## 10. Disseny Detallat: Fase 4 — Motor de RAG i Informes IA

### Visió general
La Fase 4 implementa un **analista IA** que s'activa quan radarcore detecta una oportunitat. Combina tres fonts d'informació: coneixement estructural persistent (RAG), notícies recents en temps real (Live Search), i l'anàlisi tècnic de radarcore. El principi de disseny fonamental és la **citació obligatòria**: tota afirmació factual ha d'anar acompanyada de font i data. Si el model no disposa d'informació suficient, ho declara explícitament en lloc d'inferir.

### Fase 4a — Construcció del RAG estàtic
**Objectiu:** Tenir indexada una fitxa estructurada per cada ticker de la Watchlist, basada en documents reals amb procedència traçable.
**Trigger:** Botó "Sincronitza RAG" a la UI de la Watchlist. Per cada ticker:
1. **Comprova la caché** — consulta si ja existeix una fitxa indexada i si el document font és recent (llindar configurable, p.ex. 90 dies).
2. **Descàrrega de documents** — en paral·lel: `SEC EDGAR API` (10-K/Q), `CNMV API` (Hechos Relevantes), `Finnhub` (Earnings) i `yfinance` (info).
3. **Extracció estructurada via Gemini** — extracció pura de dades (negoci, riscos, macro, guidance) en format JSON.
4. **Validació i Indexat** — emmagatzematge a ChromaDB amb metadades per a invalidació selectiva.

**Fitxers afectats:** `src/ai/rag_builder.py`, `src/ui/watchlist_ui.py`, `src/database/db.py`.

### Fase 4b — Pipeline d'anàlisi per oportunitat
**Objectiu:** Generar un informe fonamental automàtic per a cada nova `Opportunity`.
**Trigger:** Hook post-insert o botó manual "Analitza".

**Pipeline en paral·lel:**
- **Capa 1 (Live news):** `yfinance.news` i `Finnhub` (últims 30 dies).
- **Capa 2 (RAG retrieval):** Cerca al vector store del perfil estructural de l'empresa.
- **Capa 3 (Context tècnic):** Mètriques de radarcore (RSI, drop, support, confidence).

**Síntesi final:** Prompt d'analista sènior amb regla de citació crítica. Genera un JSON amb resum executiu, causa de la caiguda, riscos, catalitzadors i nivell de convicció.

**Fitxers afectats:** `src/ai/analyst_pipeline.py`, `src/ai/prompts.py`, `src/ui/opportunity_detail_ui.py`.

### Fase 4c — Refresc semi-dinàmic del RAG
**Objectiu:** Mantenir les fitxes actualitzades (earnings, guidance, investor days) sense contaminar amb el soroll diari.
**Mecanisme:** Invalidació per hash (`version_hash`) quan es detecta un nou event corporatiu a Finnhub. Les notícies diàries NO entren al RAG per evitar "soroll", es consulten en viu.

**Fitxers afectats:** `src/ai/rag_refresher.py`, `src/utils/scheduler.py`.

### Nou model de dades — `RAGIndex`
```python
class RAGIndex(Base):
    __tablename__ = "rag_index"
    id            = Column(Integer, primary_key=True)
    ticker        = Column(String, nullable=False, index=True)
    document_type = Column(String)        # "10-K", "earnings_transcript", etc.
    document_date = Column(Date)
    source_url    = Column(String)
    version_hash  = Column(String)        # per invalidació
    needs_refresh = Column(Boolean, default=False)
    indexed_at    = Column(DateTime)
    profile_json  = Column(JSON)          # la fitxa extreta
```

### Fonts de dades i cost estimat
| Font | Dades | Cost |
|:---|:---|:---|
| `yfinance` | info, news | Gratuït |
| `SEC EDGAR` | 10-K, 10-Q, 8-K | Gratuït |
| `CNMV` | Hechos relevantes | Gratuït |
| `Finnhub` | News, earnings | Tier gratuït (60 req/min) |
| `Gemini 1.5 Pro`| Extracció + síntesi | Tier gratuït (50 req/dia) |
