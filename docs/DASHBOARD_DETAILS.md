# Document Intelligence Dashboard — Full Documentation

## Overview

The dashboard is an interactive **Streamlit** web app that combines **Document Intelligence POC** metrics (VPU / Environmental & Social) with **real data from the World Bank Open Data API**. It provides multiple indicators, time-series trends, country rankings, growth-rate analysis, correlation (e.g. GDP vs CO₂), composite snapshot tables, heatmaps, and a dedicated **ML & DL Analytics** tab with simulated training curves and retrieval metrics.

- **Run locally:** `RUN_DASHBOARD.bat` or `streamlit run dashboard.py --server.port 8502`
- **URL:** **http://localhost:8502**
- **Design:** Light background (`#f5f5f5`), muted chart palette (slate, blue, grey), fonts: **Sora** (headings, futuristic geometric), **DM Sans** (body, easy on the eyes).

---

## Data Sources

### 1. World Bank Open Data API

- **Base URL:** `https://api.worldbank.org/v2/`
- **Usage:** Indicators and time series are fetched with `urllib`, cached for **1 hour** (`@st.cache_data(ttl=3600)`).
- **Countries (default):** USA, China, India, Brazil, South Africa, Germany, United Kingdom, France, Japan, Mexico (code: `USA;CHN;IND;BRA;ZAF;DEU;GBR;FRA;JPN;MEX`).
- **Date:** Latest single year (e.g. 2021) for cross-sectional charts; range `2016:2022` for time-series and growth analysis.
- **Fallback:** If the API times out or errors, the dashboard uses built-in fallback datasets so all sections still show data.

### 2. World Bank Indicators Used (full list)

| Indicator ID        | Short name              | Description                                      | Unit / note                    |
|---------------------|-------------------------|--------------------------------------------------|---------------------------------|
| `EN.ATM.CO2E.PC`    | CO₂ emissions           | CO₂ emissions (metric tons per capita)           | Environmental                  |
| `AG.LND.FRST.ZS`    | Forest area             | Forest area (% of land area)                     | Environmental                  |
| `EG.FEC.RNEW.ZS`    | Renewable energy        | Renewable energy consumption (% of total)        | Environmental                  |
| `NY.GDP.PCAP.CD`    | GDP per capita          | GDP per capita (current US$)                     | Economic                       |
| `SP.DYN.LE00.IN`    | Life expectancy         | Life expectancy at birth                         | Years, health                  |
| `SH.H2O.BASW.ZS`    | Basic drinking water    | People using at least basic drinking water (%)   | Social / WASH                  |
| `SH.STA.BASS.ZS`    | Basic sanitation        | People using at least basic sanitation (%)       | Social / WASH                  |
| `EG.USE.ELEC.KH.PC` | Electric power          | Electric power consumption (kWh per capita)      | Energy access                  |
| `SI.POV.DDAY`       | Poverty $2.15/day       | Poverty headcount ratio at $2.15/day (%)         | Social / poverty               |
| `SG.GEN.PARL.ZS`    | Women in parliament     | Proportion of seats held by women in parliament (%) | Governance / gender        |
| `SE.PRM.ENRR`       | Primary enrollment      | School enrollment, primary (% gross)             | Education                      |
| `SP.POP.TOTL`       | Population              | Total population                                 | Raw count; shown in millions when large |
| `SL.UEM.TOTL.ZS`    | Unemployment            | Unemployment (% total labor force)               | Labor                          |
| `SH.XPD.CHEX.GD.ZS` | Health expenditure      | Health expenditure (% of GDP)                     | Health                         |
| `SP.URB.TOTL.IN.ZS` | Urban population        | Urban population (% of total)                     | Demographics                   |
| `IT.NET.USER.ZS`    | Internet users          | Individuals using the Internet (%)                | Digital access                 |

### 3. Time-Series Indicators (for trend and growth analysis)

- **CO₂ emissions** (`EN.ATM.CO2E.PC`) — years 2016–2022  
- **Forest area** (`AG.LND.FRST.ZS`) — years 2016–2022  
- **GDP per capita** (`NY.GDP.PCAP.CD`) — years 2016–2022  
- **Life expectancy** (`SP.DYN.LE00.IN`) — years 2016–2022  

### 4. Document Intelligence API (local)

- **Endpoint:** `GET http://127.0.0.1:8000/api/v1/health`
- **Used for:** API status (Live/Offline) and **live vector store chunk count** when the API is running.
- **Not from World Bank:** POC metrics (documents indexed, queries, retrieval time, user adoption, ESF categories, safeguards coverage, document intelligence topics, governance, model performance) are **sample/illustrative** values in the dashboard code.

---

## Tab-by-Tab Description

### Tab 1: Executive summary

**Purpose:** High-level KPIs and ESF usage for leadership.

**Metrics (sample except chunks):**
- Documents indexed  
- Knowledge base chunks (live from API when available)  
- Queries (30d)  
- Avg. retrieval (s)  
- User adoption  

**Charts:**
- **Usage by ESF category** — Bar chart (colored) of documents per category: Biodiversity & habitats, Community health & safety, Displacement & livelihoods, Indigenous peoples, Labor & conditions, Climate & resilience, Stakeholder engagement, Grievance redress.

---

### Tab 2: World Bank indicators

**Purpose:** All World Bank datasets used in the dashboard, one chart per indicator.

**Content:**
- One **bar chart** per indicator (CO₂, Forest, Renewable, GDP, Life expectancy, Water, Sanitation, Electricity, Poverty, Women in parliament, Primary enrollment, plus Population, Unemployment, Health expenditure, Urban %, Internet).
- Each bar chart shows **latest-year** values by country with a **muted color palette** (slate, blue, grey). **Stacked bar** — normalized GDP, Life expectancy, Forest (% by country).
- Optional **raw data table** (e.g. CO₂) when “Show raw data tables” is enabled in the sidebar.

**Data source:** World Bank API, single-year request per indicator, cached 1 hour.

---

### Tab 3: Deep analysis

**Purpose:** Detailed, impressive analysis of World Bank data: trends, rankings, growth, correlation, composite snapshot.

**1. Time trends (2016–2022)**  
- **CO₂ emissions over time by country** — Line chart: year on x-axis, CO₂ (metric tons per capita) on y-axis, one line per country (colored).  
- **CO₂ emissions (area chart)** — Same data as area chart for a different visual.  
- **Forest area over time by country** — Line chart: year on x-axis, forest area (% of land) on y-axis, one line per country (colored).  

**Data source:** `fetch_world_bank_timeseries` for `EN.ATM.CO2E.PC` and `AG.LND.FRST.ZS` with date range 2016:2022.

**2. Country rankings (latest year)**  
- **GDP per capita** — Table: rank, country, GDP per capita (US$), year; sorted descending.  
- **Life expectancy** — Table: rank, country, years, year; sorted descending.  

**Data source:** Same World Bank single-year data as in Tab 2, sorted and ranked in the dashboard.

**3. Growth / change over period**  
- **CO₂ emissions change** — Percentage change from **first year to last year** in the time-series range (2016→2022) by country.  
- Displayed as a bar chart (country vs. growth %).  
- Formula: `(value_last - value_first) / value_first * 100`.  

**Data source:** Time-series data for CO₂; computed in the dashboard.

**4. Correlation — GDP per capita vs CO₂ emissions**  
- **Scatter plot:** x = GDP per capita (US$), y = CO₂ (metric tons per capita), one point per country (colored), latest year.  
- **Pearson correlation** coefficient reported below the chart (e.g. positive = higher GDP associated with higher CO₂ in the sample).  

**Data source:** Latest-year GDP and CO₂ from World Bank; correlation computed with pandas.

**5. Composite snapshot — selected indicators (latest year)**  
- **Table:** One row per country, columns: Country, CO₂ (t/cap), Forest %, Renewable %, GDP/cap (US$), Life exp (y), Water %, Sanitation %, Women parl %.  
- Intended for **cross-country E&S and development comparison**; higher is generally “better” except for CO₂.  
- **Heatmap** — Country × Indicator (normalized 0–1); color scheme: blues. Rows = country, columns = indicator; helps spot strengths/weaknesses at a glance.

**Data source:** World Bank single-year data for the listed indicators; merged by country in the dashboard.

---

### Tab 4: ML & DL Analytics

**Purpose:** ML/DL metrics for the RAG/embedding and retrieval pipeline (simulated for POC).

**Content (all simulated for POC):**
- **Training & validation curves** — Line chart: epoch (1–20) vs value for Train loss, Val loss, Train accuracy, Val accuracy.
- **Classification metrics** — Bar chart: Precision@5, Recall@5, F1@5, MRR, NDCG@10, Hit rate (retrieval quality); color scheme blues.
- **Confusion matrix** — Heatmap: Actual (Relevant / Not relevant) vs Predicted (Retrieved / Not retrieved) with counts; greys scheme.
- **Feature importance** — Horizontal bar chart: embedding dimensions Dim_1 … Dim_10 vs importance; blues scheme.
- **Model comparison** — Scatter: latency (ms) vs accuracy for MiniLM-L6, all-mpnet, OpenAI ada, E5-large, BGE-base; tooltips enabled.
- **KPIs:** Best F1@5, Avg inference (ms), Embedding dim, Drift score (weekly).

---

### Tab 5: E&S & Safeguards

**Purpose:** Environmental and social risk coverage and safeguards compliance (POC/sample data).

**Charts:**
- **Environmental and social risk coverage** — Bar chart (colored): Natural habitats & biodiversity, Pollution & resources, Community health & safety, Displacement & livelihoods, Indigenous peoples & heritage, Climate mitigation & adaptation (document counts).  
- **Safeguards compliance (document coverage %)** — Bar chart (colored): Involuntary resettlement (RAP/RPF), Indigenous peoples (FPIC), Gender & inclusion, Grievance mechanism, Labor & working conditions, Monitoring & reporting.  

**Optional:** Raw data table when “Show raw data tables” is on.

**Data source:** Sample lists in dashboard code (not World Bank).

---

### Tab 6: Document intelligence

**Purpose:** How the RAG/document Q&A system is used and what is in the knowledge base.

**Charts:**
- **Query volume by topic** — Bar chart (colored): Environmental risks, Social safeguards, Resettlement, FPIC & indigenous, Climate, Grievance, Labor, Stakeholder engagement.  
- **Chunks indexed by source type** — Bar chart (colored): ESF policy, Project E&S reports, Safeguard guidelines, Country frameworks, Training materials.  

**Live note:** When the Document Intelligence API is running, an info box shows the **actual** vector store chunk count.

**Optional:** Raw table (topic vs. queries) when “Show raw data tables” is on.

**Data source:** Sample lists in dashboard code; chunk count from `/api/v1/health`.

---

### Tab 7: Governance & quality

**Purpose:** Data governance, ethical AI, and model performance (POC/sample data).

**Charts:**
- **Data governance & ethical AI (%)** — Bar chart (colored): Data retention policy, Access controls, Bias monitoring, Privacy compliance, Audit logging, Human oversight.  
- **Model performance (MLOps)** — Bar chart (colored): Retrieval precision@5, Answer relevance, Latency p95 (×100), Uptime (30d).  

**Text:** Ethics note (local-first, no third-party document sharing unless OpenAI enabled, RAG runs in MLflow).

**Data source:** Sample lists in dashboard code.

---

## Sidebar

- **Reporting period** — Dropdown (Last 30 days / Last 90 days / YTD); used for labeling; World Bank data is by calendar year.  
- **Show raw data tables** — Checkbox to show/hide raw tables in World Bank indicators and E&S/Document intelligence tabs.  
- **API status** — “Live” if `http://127.0.0.1:8000/api/v1/health` is reachable; otherwise “Offline”.  
- **Vector store** — Displays current chunk count when API is Live.  
- **Links** — “Open API docs” (Swagger at /docs), “API root” (http://127.0.0.1:8000).

---

## Technical Details

| Item | Detail |
|------|--------|
| Main file | `dashboard.py` (project root) |
| Documentation | `docs/DASHBOARD_DETAILS.md` (this file) |
| Framework | Streamlit |
| Charts | Altair: bar, line, area, stacked bar, scatter (with size/opacity), heatmap (rect); fallback `st.bar_chart` if Altair unavailable |
| World Bank API | `urllib.request`; GET; User-Agent: WB_POC_Dashboard/1.0; timeout 10–12 s |
| Caching | `@st.cache_data(ttl=3600)` for all World Bank fetches (1 hour) |
| Local API | `GET /api/v1/health` for status and vector_store_count (no cache) |
| Color palette | Muted: slate, blue, grey tones (CHART_COLORS); heatmaps/metrics use blues or greys schemes. Background: light (#f5f5f5). |
| Dependencies | streamlit, altair, pandas (altair/pandas optional but required for full analysis and colored charts) |

---

## Summary of “Highly Impressive” Analysis

1. **Multiple World Bank datasets** — 16 indicators across environment, economy, health, WASH, energy, poverty, governance, education, population, employment, urban, internet.  
2. **Time-series** — CO₂ and Forest area (and GDP, Life exp) over 2016–2022 with line and **area** charts by country.  
3. **Rankings** — GDP per capita and Life expectancy tables with explicit rank column.  
4. **Growth rates** — CO₂ % change from first to last year in range, by country.  
5. **Correlation** — GDP vs CO₂ scatter plot plus Pearson correlation.  
6. **Composite snapshot** — Multi-indicator table by country; plus **heatmap** (country × indicator, normalized).  
7. **Chart variety** — Bar, line, **area**, **stacked bar**, scatter, **heatmap**; muted palette and blues/greys schemes.  
8. **ML & DL Analytics tab** — Training/validation curves, Precision/Recall/F1/MRR/NDCG, confusion matrix heatmap, feature importance, model comparison (accuracy vs latency).  
9. **Caching** — 1-hour TTL to respect API and reduce latency.  
10. **Fallback** — Graceful handling when World Bank or Altair/pandas is unavailable.  
11. **Documentation** — This file describes every dataset and analysis in one place.

---

## How to Run

1. **Install:** `pip install -r requirements.txt` (includes streamlit, altair, pandas).  
2. **Start:** Run `RUN_DASHBOARD.bat` or `python -m streamlit run dashboard.py --server.port 8502`.  
3. **Open:** **http://localhost:8502**.  
4. **(Optional)** Start the Document Intelligence API (`RUN.bat` or `python run_api.py`) so the dashboard shows “Live” and the real vector store chunk count.  
4. **(Optional)** Start the Document Intelligence API (`RUN.bat` or `python run_api.py`) so the dashboard shows **Live** and the real vector store chunk count.  
5. **Fallback:** If the World Bank API fails or times out, the dashboard uses built-in fallback data so all tabs still show content.

## Appearance

- **Background:** Light grey (`#f5f5f5`) for the main app; sidebar `#fafafa`.  
- **Charts:** Muted palette (slate, blue, grey); heatmaps use blues or greys schemes.  
- **Fonts:** Sora (headings), DM Sans (body); both modern and easy to read.  
- **Metrics:** Card-style with light border and left accent.

---

## Data and Limitation Summary

- **World Bank:** All indicator and time-series data in the dashboard are from the World Bank Open Data API; coverage depends on country and year availability.  
- **Document Intelligence:** Only the vector store chunk count is live (from `/api/v1/health`); all other POC metrics (documents, queries, retrieval time, adoption, ESF/safeguards/topics, governance, model metrics) are sample values in code.  
- **Filters:** Reporting period and “Show raw data tables” affect only display; they do not change World Bank API parameters (year/range is fixed in code).

This file is the single reference for what the dashboard does, which World Bank datasets it uses, and how each analysis is produced.
