# radarcore: Investment Guide (Concepts & Practice)

Welcome to **radarcore**. This manual will help you understand how the **Buy the Recovery** strategy works and how you can use this software to learn about finance and swing trading from scratch.

---

## 1. What is the "Buy the Recovery" Strategy?

Historically, many people have heard the term "Buy the Dip". In RadarCore, we call it **Buy the Recovery** because it is more precise: we don't buy when the stock is actively crashing (a "falling knife"), but when it has already found a floor and has starting to recover.

The goal is to take advantage of the fact that the price tends to return to its average after a temporary setback.

---

## 2. Before Starting: Configuring the Scanner

When you configure the scanner, you see a series of parameters. Here is what they mean in plain language:

*   **Lookback Days**: This is how far back we look at the past to find the stock's highest price point. If you set 60 days, we look for the "Record" price of those 2 months to compare it with today's price.
*   **Min Drop %**: How much of a "discount" you want the stock to have before notifying you. If you set 15%, we only look for companies that have fallen at least 15% from their 60-day high.
*   **Min Rebound %**: This is the confirmation that we are no longer falling. If you set 2%, you want the stock to have already risen 2% from its lowest point.
*   **Symbol Limit**: How many companies in the market you want to analyze (0 to analyze them all, but it will take longer).

---

## 3. Pattern Buckets & Phase Model

Instead of just one strategy, RadarCore classifies every stock into a **Bucket** (Pattern) and a **Phase** (Timing).

### The Primary Buckets
*   **SWING**: The classic setup. A deep drop followed by a clear bounce.
*   **RISE**: The stock is already in a steady uptrend. Lower room for growth but more stable.
*   **LATERAL**: The stock is moving sideways. Accumulation phase.

### The Lifecycle (Phases)
The program tells you where you are in the "journey" back to the previous highs:
*   🟢 **VALLEY**: You are at the bottom. Highest potential profit, but highest risk.
*   🟡 **MID**: The recovery is confirmed. You are in the "sweet spot" of the trend.
*   🟠 **MATURE**: Most of the recovery has happened. Be careful about entering now.
*   🔴 **LATE**: The stock is already back at its highs. The trade is over.

---

## 4. Key Financial Concepts

### Stop Loss (SL)
This is your **safety handbrake**. Imagine you buy a stock at $10. If suddenly the company continues to do poorly, the Stop Loss is an order that tells your bank: "If the stock drops back to $9, sell it immediately."
*   **What is it for?** Because if the company goes bankrupt, you will have only lost $1 (from 10 to 9), but you will have saved yourself from losing all $10. RadarCore marks this line in red on the charts.

### Targets (T1 and T2)
These are your "sell goals" where you collect profits.
*   **T1 (Conservative Target)**: Is a halfway recovery point (usually marked at 85% approximation to the previous high). This is where you might decide to sell half to lock in quick profits.
*   **T2 (Ideal Target)**: This is when the stock returns exactly to the peak price it had before falling. This is where the strategy is successfully completed.

### Reference Markets (The S&P 500 Case)
Even though you can scan other markets, the program always uses the "American Market" (**SPY / S&P 500**) as a global reference. If the American market falls hard, it is very difficult for any stock to rise healthily. It serves as a thermometer for global crisis vs isolated company problems.

---

## 5. Practical Case: Interpreting Charts

When you open a chart in RadarCore, look for these colors:

1.  **The Mountain (Gold)**: Shows the 2-year trend. Look for a "U" or "V" shape.
2.  **Troughs (Green Triangles)**: These are the floors. The most recent green triangle marks the start of the current recovery.
3.  **Peaks (Red Triangles)**: These are the ceilings. They show where the stock met resistance before.

## Golden Rule: Diversification
Never put all your savings into a single stock. The correct strategy involves having, for example, 10 different trades at the same time. This way, if one goes wrong and the **Stop Loss** is triggered, the other 9 can continue their course towards **T2** and give you an overall profit.
