# RadarCore — User Guide

> **For educational purposes only. Not financial advice.**

---

## What is RadarCore?

The stock market is noisy. Every day, thousands of companies have their prices moving up and down, and most of the interesting moments — the ones where a solid company has dropped significantly and appears to be recovering — happen quietly, without anyone noticing. RadarCore is a scanning tool designed to cut through that noise. It systematically checks hundreds of stocks every day, looking for a very specific pattern: companies that have fallen significantly from their recent high and are starting to recover. Instead of reading the news or following tips, you let the mathematics work for you.

The typical RadarCore user is someone who has little time to monitor markets daily but wants a structured, data-driven way to identify potential swing trading opportunities. You don't need to be a professional trader or a financial analyst. You don't need to know advanced mathematics. You just need to understand what you're looking at — and that is exactly what this guide is for.

RadarCore is **not** a crystal ball. It does **not** predict whether a stock will go up or down. It does not give you financial advice, and it does not tell you to buy or sell anything. What it does is identify historical patterns in price data and score how strong those patterns look — nothing more. All investment decisions are yours alone, and all investing carries risk, including the risk of losing your entire capital.

---

## Key Concepts (before you start)

### Stock market / equities

**In simple words:** A place where you can buy small ownership pieces of real companies.

**The analogy:** Imagine a bakery that divides ownership into 1,000 slices. You can buy one slice — that's a share. The stock market is the global marketplace where these slices of thousands of companies are traded every day.

**Why it matters in RadarCore:** RadarCore scans this marketplace looking for companies whose share price has dropped and is bouncing back.

---

### Ticker symbol

**In simple words:** A short code that uniquely identifies a company on a stock exchange.

**The analogy:** Like a car's license plate — `AAPL` means Apple, `MSFT` means Microsoft, `SAN.MC` means Santander listed in Madrid.

**Why it matters in RadarCore:** Every result in the scanner and every chart is identified by its ticker. You can click any ticker in the History table to open the corresponding Yahoo Finance page.

---

### OHLCV data (Open, High, Low, Close, Volume)

**In simple words:** The five key numbers that describe how a stock behaved during any given day.

**The analogy:** Think of it like a weather report for a stock — the opening temperature, the daily high, the daily low, the closing temperature, and how many people "showed up" (volume) to trade it.

**Why it matters in RadarCore:** Every chart and every calculation in the scanner uses OHLCV data downloaded from Yahoo Finance. Without this data, there is nothing to scan.

---

### Market capitalization

**In simple words:** The total money-value of a company on the stock market, calculated as (share price × total number of shares).

**The analogy:** If a company has 1 million shares priced at $100 each, the market cap is $100 million. Large caps (>$10 billion) are generally safer and more liquid than small caps.

**Why it matters in RadarCore:** The strategy parameters include a minimum market cap filter (default: $10 billion) to avoid scanning tiny, illiquid companies — the ones most likely to give false signals.

---

### Swing trading (vs day trading vs buy and hold)

**In simple words:** Attempting to profit from medium-term price swings — holding positions for days to weeks, not seconds or decades.

**The analogy:** Imagine buying an umbrella at the end of summer when it's cheap, and selling it at the first rain. You're not a street vendor (day trader) nor are you buying a wardrobe full of umbrellas for your whole life (buy and hold). You're spotting a temporary mispricing and capturing it.

**Why it matters in RadarCore:** RadarCore is built specifically for swing trading logic. Its patterns, scores, and phases are all designed around the timeframe of a typical swing trade: a few days to a few months.

---

### Technical analysis vs fundamental analysis

**In simple words:** Technical analysis studies the price chart. Fundamental analysis studies the company's finances.

**The analogy:** Fundamental analysis asks "is this a good bakery?" (profits, staff, recipe). Technical analysis asks "is the queue at the door growing or shrinking today?".

**Why it matters in RadarCore:** RadarCore is primarily a technical analysis tool. It reads price patterns, not balance sheets. The AI-generated reports add a layer of fundamental context, but the scanner decisions are driven by price behavior.

---

### Support and resistance levels

**In simple words:** Price levels where a stock has historically had difficulty going below (support) or above (resistance).

**The analogy:** A ceiling and a floor in an apartment — the price bounces between them until it breaks through one.

**Why it matters in RadarCore:** The Pivots chart view marks historical peaks (resistance) and troughs (support), helping you understand where the price has historically reacted.

---

### Drawdown and recovery

**In simple words:** Drawdown is how much the price has fallen from its peak. Recovery is how much it has bounced back from the bottom.

**The analogy:** A ball dropped from a table — the drawdown is how far it fell, the recovery is how high it bounced back.

**Why it matters in RadarCore:** The `Drop %` and `Rebound %` columns in the results table are exactly this. RadarCore looks for stocks with a meaningful drawdown and a visible early recovery — the "bounce" pattern.

---

### Moving averages (EMA)

**In simple words:** A line that smooths out the price over a given number of days, making the trend easier to see.

**The analogy:** Instead of looking at your daily weight (which fluctuates), you track your weekly average — the trend becomes clearer.

**Why it matters in RadarCore:** The scanner and scoring systems internally use EMAs to detect the direction and momentum of price trends before assigning a bucket classification.

---

### RSI (Relative Strength Index)

**In simple words:** A 0–100 indicator that measures whether a stock is overbought (above 70) or oversold (below 30).

**The analogy:** A thermometer for buying pressure. Below 30 means the market may be over-panicking about a stock; above 70 means investors may be over-excited.

**Why it matters in RadarCore:** Bucket scorers internally use RSI as a component in calculating the confidence score for certain patterns like `RISE` and `SWING`.

---

### ATR (Average True Range)

**In simple words:** A measure of how much a stock's price typically moves day-to-day — its "volatility ruler".

**The analogy:** A calm lake (low ATR) vs rough ocean waves (high ATR). Knowing the wave size helps you decide how much risk you're taking.

**Why it matters in RadarCore:** ATR is used internally to normalize signals across stocks of different volatility profiles, making the confidence scores more comparable.

---

### Earnings dates

**In simple words:** The days when a company publicly announces its financial results (quarterly profits, revenues, guidance).

**The analogy:** The school report card day — prices can jump wildly up or down based on whether results beat or missed expectations.

**Why it matters in RadarCore:** The scanner flags stocks with upcoming earnings events in red (HIGH risk, <14 days) or orange (MEDIUM risk, <30 days). A stock approaching earnings is inherently unpredictable, regardless of its technical pattern.

---

### Market index (S&P 500, Nasdaq 100)

**In simple words:** A basket of top companies grouped together to represent an overall market or sector.

**The analogy:** Instead of tracking every player's score in a football league, you track the league standings — that's an index.

**Why it matters in RadarCore:** You choose which index universe to scan (S&P 500, Nasdaq 100, IBEX 35, etc.). RadarCore also downloads SPY (the S&P 500 ETF) in the background to provide relative market context — helping distinguish a stock that dropped because of company-specific news vs a market-wide crash.

---

## Step-by-Step Walkthrough

### Step 1 — Choose your universe

A "universe" is simply the list of stocks the scanner will check. RadarCore supports several predefined universes corresponding to major global indices.

| Universe | Stocks | Best for |
|---|---|---|
| S&P 500 | ~500 US large caps | Beginners — most liquid, best data quality |
| Nasdaq 100 | ~100 US tech & growth | Tech-focused traders |
| IBEX 35 | 35 Spanish companies | Spanish-market traders |
| DAX 40 | 40 German companies | European-market traders |
| EuroStoxx 50 | 50 European blue chips | Broad European exposure |

**Recommendation for beginners:** Start with the **S&P 500**. These are the 500 largest US companies — highly liquid, with excellent historical data and very few data gaps. They represent the broadest, most studied universe in the world.

The **Nasdaq 100** is more tech-heavy. It tends to be more volatile, which produces more signals — but also more false positives. Only move to narrower universes once you understand how to read the scanner output.

---

### Step 2 — Understanding scan modes

RadarCore has two scanning modes, selectable from the sidebar:

**Automatic mode (default, ON)**
The scanner runs across all stocks in the chosen universe and evaluates every single one. Any stock that passes the strategy criteria is added to History automatically. This is the recommended mode for beginners — you simply point, scan, and review results.

**Watchlist mode (OFF)**
The scanner only analyzes the tickers you have manually added to your Watchlist. Use this when you already have a curated list of companies you follow and want to scan only those.

**How to build up to manual mode:**
1. Start with Auto mode and scan the S&P 500 several times over a few weeks.
2. Notice which sectors and patterns appear most often when the market dips.
3. Research those sectors and add your favorites to the Watchlist.
4. Switch to Watchlist mode once you trust your curated list.

---

### Step 3 — Running a scan

Once you've chosen your universe and mode, hit **Run Scan**.

#### Symbol limit
Leave at `0` to scan the full universe. During your first test, set it to `20–50` to get a quick feel for the output without waiting several minutes.

#### Pre-filter universe toggle
This optional toggle (**Pre-filter universe**, in the sidebar) runs an additional eligibility check on each stock before applying the strategy:
- **OFF (default):** All stocks pass to the strategy scorer. Faster, more results.
- **ON:** Only stocks with sufficient volume, history, market cap, and resilience history reach the strategy. Slower, but higher-quality results.

Recommended for beginners: start with **OFF** to see more results, then enable it when you want to reduce noise.

#### Min Score slider (in History & Reports tab)
After scanning, the **Min Score** filter controls which results appear in the table. **Start at 0** — this shows every single detected opportunity, regardless of confidence. As you gain experience, raise it to 50 or 60 to focus only on high-confidence signals.

#### Bucket filter
**Start with "All"** — this shows all pattern types together. Once you understand the different patterns, use the filter buttons (SWING, RISE, LATERAL…) to focus on the ones you're most comfortable trading.

---

### Step 4 — Reading the results table

After a scan completes, go to the **History & Reports** tab. You will see a table sorted by quality — the most promising opportunities appear at the top.

#### Symbol
The ticker code of the company. **Clickable** — opens Yahoo Finance in a new tab. Verify the company name and sector before doing anything else.

#### Drop %
How far the stock has fallen from its recent high (within the lookback window, default: 60 days). A `Drop %` of 25% means the stock is trading 25% below where it peaked two months ago. The strategy requires a minimum drop (default: 15%) to qualify.

#### Rebound %
How much the stock has already bounced from its recent low. A `Rebound %` of 5% means the price has already moved up 5% from the bottom. This is the early "recovery signal" RadarCore looks for.

#### Pattern
The type of price pattern detected by the automated classifier. Patterns correspond to **buckets**:

| Pattern | Meaning |
|---|---|
| **SWING** | Classic swing: significant drop followed by an early rebound. The archetypal buy-the-dip setup. |
| **SWING → BREAKOUT** | Swing pattern where the price has already broken above a recent resistance level. More mature signal. |
| **SWING → PULLBACK** | Swing pattern where the price is dipping again slightly after an initial recovery. Can be a re-entry opportunity. |
| **RISE** | Stock in an upward trend, not heavily dropped but maintaining a consistent climb. |
| **LATERAL** | Stock trading sideways in a horizontal range. Low momentum, watchful holding pattern. |
| **DESCENDING** | Stock in a downward trend. RadarCore flags these but they are generally not buy candidates. |
| **HIGHS** | Stock near its all-time highs. Very low upside remaining unless it breaks out to new highs. |

#### Phase
Where the stock stands within its current pattern's lifecycle:

| Phase | Meaning | What to do |
|---|---|---|
| 🟢 **VALLEY** | Price is at or very near the bottom of the drop. Earliest possible entry. Highest risk, highest potential. | Watch closely. |
| 🟡 **MID** | Recovery is underway — price is in the middle of the climb. Better confirmation, less upside remaining. | Standard entry zone. |
| 🟠 **MATURE** | Recovery is well advanced. Less room to the top, but trend is confirmed. | Be cautious about chasing. |
| 🔴 **LATE** | Price is near the top of the expected range. Most of the move has happened. | Consider avoiding or exiting. |
| ⚪ **NO PATTERN** | The classifier could not assign a clear phase. | Requires manual review. |

#### Upside 3Y
The percentage distance between the **current price** and the **ATH (All-Time High) reached over the last 3 years**. Represents the theoretical maximum recovery if the stock returns to its 3-year peak.

> **Example:** Upside 3Y = 80% means the stock would need to rise 80% to return to where it traded at its best point 3 years ago. Higher is not always better — context matters.

#### Conf.
The confidence score (0–100%) calculated by the bucket scorer. It combines signals like volume trend, momentum, RSI level, and price slope. **Higher is better.** A score of 70%+ is considered a relatively strong signal. A score below 40% means the pattern is weak or ambiguous.

---

### Step 5 — Reading the chart

Click any row in the History table to select it, then press **View Charts**. You will see an interactive price chart below with four view modes:

#### 🏔️ Mountain (default)
A clean line chart of the closing price over 2 years, drawn in gold on a black background. This view gives you the clearest picture of the long-term trend: where the recent peak was, where the bottom formed, and where the price is recovering to. Start here.

#### 📍 Pivots
The same price chart with red/green triangles marking the algorithmically detected **pivot points**:
- **T (Trough) — green triangle below:** A local minimum — the price reversed upward from here.
- **P (Peak) — red triangle above:** A local maximum — the price reversed downward from here.

Reading the pivots helps you understand the structure of the trend: is the stock making higher lows (bullish structure) or lower highs (bearish structure)?

#### 🌊 Eras
Vertical colored bands that divide the chart into **era segments** — the periods between consecutive pivot points. Each era is color-coded by its direction and intensity. This view helps you see the rhythm of the stock: how long up-moves typically last vs down-moves, and whether the current era looks similar to previous recoveries.

#### 🕯️ Candles
Traditional candlestick chart. Each candle represents one day:
- **Green candle:** Closed higher than it opened.
- **Red candle:** Closed lower than it opened.
- **Candle body:** The difference between open and close.
- **Candle wick:** The full day range (high to low).

Use this view when you want to make a precise entry decision and need to see day-by-day price action.

#### Earnings indicators
Vertical dashed lines appear at upcoming or recent earnings dates when data is available:
- **Red dashed line:** Earnings within 14 days — high risk of volatility.
- **Orange dashed line:** Earnings 15–30 days out — moderate caution.

Avoid entering a position immediately before an earnings event unless you're comfortable with the binary risk.

---

### Step 6 — Evaluating an opportunity

When reviewing a candidate, apply this mental checklist in order:

**1. Check Phase first**
🟢 VALLEY or 🟡 MID phases are the sweet spots. MATURE is acceptable if confidence is high. Skip LATE signals unless you have a specific reason.

**2. Check Conf. second**
Aim for 60%+ for a starting position. Below 40% means the signal is weak — the pattern exists mathematically, but the supporting factors aren't strong enough.

**3. Check Upside 3Y third**
Is there enough room to grow? If the stock is already at 95% of its 3-year high, there's only 5% theoretical upside remaining — the risk/reward ratio is poor.

**4. Check the earnings badge**
If you see a ⚠️ HIGH or 📅 MEDIUM earnings alert, the upcoming announcement could move the price violently in either direction. This doesn't mean the opportunity is invalid — but set your stop-loss accordingly or wait until after earnings.

**5. Look at the chart**
Does the Mountain view confirm what the numbers say? Is the most recent pivot a confirmed trough, or is the price still falling? The Pivots view should show a clear Trough (green triangle) in the recent period.

**The ideal combination:**
> 🟢 VALLEY + SWING pattern + Conf. > 65% + Upside 3Y > 40% + No near-term earnings = worth serious consideration.

---

### Step 7 — Using the Watchlist

The **Watchlist** tab (📋) lets you maintain a personal list of tickers to track.

**When to add a ticker:**
- You've reviewed an opportunity and want to monitor it over several days before deciding.
- The phase is LATE (not ideal to enter now) but you want to revisit it after a reset.
- You track a company for fundamental reasons and want RadarCore to flag its technical setups.

**Adding tickers:**
- In the Watchlist tab, type one or more tickers separated by commas and press **Add**.
- Alternatively, after a scan in History & Reports, press **➕ Watchlist** under any analysis card.

**Auto mode vs Watchlist mode:**
- In **Auto mode** (sidebar toggle ON), the Watchlist has no effect on scanning — the scanner always checks the full chosen universe.
- In **Watchlist mode** (toggle OFF), only your saved tickers are scanned. This is useful when you've curated a personal shortlist of 20–50 companies you trust and want faster, more focused scans.

**Removing tickers:**
In the Watchlist table, check the **Delete** checkbox next to any ticker, then press **Save changes (Notes / Delete)**. Deletion is a soft-delete — the record remains in the database but is no longer active.

---

## Glossary

| Term | Definition |
|---|---|
| **ATH** | All-Time High — the highest price a stock has ever reached. |
| **ATR** | Average True Range — a measure of daily price volatility. |
| **Bucket** | RadarCore's classification of a stock's price pattern (SWING, RISE, LATERAL, etc.). |
| **Candle** | A chart element representing one day's price: open, high, low, close. |
| **Confidence (Conf.)** | Score 0–100% reflecting how strongly the detected pattern is supported by technical signals. |
| **Drawdown** | The percentage fall from a recent peak to the current or subsequent low. |
| **EMA** | Exponential Moving Average — a smoothed average that weights recent prices more heavily. |
| **Era** | A segment of the price timeline between two consecutive pivot points. |
| **HIGHS** | Bucket for stocks trading near their recent all-time highs. |
| **IBEX 35** | The main index of the Spanish stock exchange, comprising 35 companies. |
| **LATERAL** | Bucket for stocks moving sideways in a horizontal price range. |
| **Lookback window** | Number of historical days the scanner uses to detect patterns (default: 60 days). |
| **Market cap** | Total market value of a company = share price × total shares outstanding. |
| **MID** | Phase indicating the stock is in the middle of its recovery journey. |
| **Nasdaq 100** | US index of the 100 largest non-financial technology and growth companies. |
| **OHLCV** | Open, High, Low, Close, Volume — the five data points for each daily price bar. |
| **Peak (P)** | A local price maximum — marked with a red triangle in the Pivots view. |
| **Phase** | Where a stock sits within its current pattern cycle (VALLEY → MID → MATURE → LATE). |
| **Pivot point** | A price level where the market reversed direction (either a Peak or Trough). |
| **Pattern** | The specific subtype within a bucket (e.g., SWING → BREAKOUT). |
| **Rebound %** | How much the stock has already recovered from its recent low. |
| **RISE** | Bucket for stocks in a steady upward trend without a deep prior drop. |
| **RSI** | Relative Strength Index — a momentum indicator (0–100). Below 30 = oversold, above 70 = overbought. |
| **S&P 500** | US index of the 500 largest publicly traded companies. |
| **SPY** | The most traded ETF (Exchange-Traded Fund) tracking the S&P 500. Used internally by RadarCore for market context. |
| **SWING** | Bucket for stocks with a significant drop followed by early recovery signs. |
| **Ticker** | A unique alphabetic code identifying a company on a stock exchange (e.g., AAPL, MSFT). |
| **Trough (T)** | A local price minimum — marked with a green triangle in the Pivots view. |
| **Universe** | The set of stocks RadarCore scans (S&P 500, Nasdaq 100, etc.). |
| **Upside 3Y** | Distance (%) between current price and the 3-year all-time high. |
| **VALLEY** | Phase indicating the stock is near the bottom of its drop — earliest and highest-risk entry zone. |
| **Watchlist** | Your personal curated list of tickers to monitor or use in Watchlist scan mode. |

---

## Disclaimer

RadarCore is a **personal research and educational tool**. It is designed to help individuals learn about technical analysis patterns in financial markets through automated screening.

**RadarCore does NOT:**
- Recommend buying or selling any security.
- Predict future price movements.
- Guarantee any financial outcome.
- Constitute investment advice of any kind.

**You should always:**
- Conduct your own independent research before making any investment decision.
- Consult a qualified financial advisor if you are unsure about any investment.
- Never invest money you cannot afford to lose.
- Understand that past price patterns are not indicative of future results.

Investing in financial markets involves **substantial risk**, including the possible loss of the entire amount invested. Market prices can be affected by unexpected economic events, political developments, corporate news, and countless other factors that no algorithm can reliably predict.

---

*RadarCore — For educational purposes only.*
