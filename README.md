# 🦅 Alpha Institutional Terminal (v4.0)
### 🚀 Creator & Fund Manager — Biswajit Jana (Green Bull Rider)

Welcome to the **Alpha Institutional Terminal**, a high-performance, modular, and cloud-deployed algorithmic portfolio tracker and factor screener designed specifically for advanced trading and fund management operations.

---

## 📂 Modular Architecture Blueprint

The terminal is engineered using a robust **MVC (Model-View-Controller)** pattern split into logical micro-layers for optimal execution speed, data hygiene, and dynamic rendering on both desktop and mobile viewports.

* **`core/engine.py` (The Mathematical Engine):** Handles all core processing including data fetch from live markets, Indian stock market friction charges (STT, GST, Exchange fees, DP charges), and mathematical indicator matrix generation (EMAs, Max Drawdown, Beta coefficients).
* **`core/styles.py` (The User Interface Customizer):** Injects a premium, modern high-contrast **Cyber-Glow Dark Theme** featuring glowing responsive metric blocks and Bloomberg-inspired telemetry indicators.
* **`app.py` (The Controller):** Operates as the core system routing engine. It links the UI components with the math matrix, manages data states, and drives the smooth multi-page sidebar navigation experience.
* **`stocks.py` (The Watchlist Data Core):** Houses the active token assets list and high-momentum institutional filter scopes.

---

## ⚡ Key Integrated Ecosystems

### 1. Multi-Factor Flow Screener
* Custom dual-slider mechanics to filter trailing sales growth and return on equity (ROE) benchmarks concurrently.
* Real-time structural alignment scanner that flags whether an asset is sitting in deep trend reversal or premium long-term continuation.

### 2. Micro-Friction Transaction Desk
* **Buy/Accumulate Architecture:** Automatically merges top-up orders into a single row using precise **Weighted Average Pricing (WAP)** metrics.
* **Sell/Liquidation Architecture:** Deducts precise Indian market transactional friction fees (including DP execution slabs) out of gross revenue before storing audited profit/loss accounts.

### 3. Pure Alpha Risk Dashboard
* Computes the systemic risk index (**Portfolio Beta Coefficient**) against macro indices dynamically.
* Real-time data visualization showing capital diversification spreads and peak-to-trough Max Drawdown (MDD) protection.

### 4. Post-Tax Audited Ledger History
* An encrypted ledger environment that tracks closed positions and metrics such as historical net capital gain and system strategy win rates.

---
*Developed under extreme risk-management paradigms. Locked and secured for institutional deployment.*
