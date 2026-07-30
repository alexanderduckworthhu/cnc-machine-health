# Precision manufacturing framing

Target context: **precision manufacturing**, **microtechnology**, and **job-shop CNC cells**
where spindle uptime and scrap avoidance drive margin.

## Shared pain (map the demo to it)

| Employer pain | How this project maps |
|---------------|------------------------|
| Unplanned spindle / process downtime | Health cards + amber/red triage before scrap cascade |
| Quality drift on micron-scale features | Vibration + thermal channels as early process-health signals |
| Sparse labeled failure data | Isolation Forest, unsupervised first, labels later |
| IT/OT gap (historians, OPC-UA, MES) | Mock OPC-UA client façade shows you know the OT vocabulary |
| Need for explainable shop-floor tools | Percentile health + thresholds beat black-box “risk 0.73” |

## Pitch variants (30 seconds)

### Applied sensing / industrial R&D
> “I care about applied sensing + trustworthy ML for industry. This demo shows windowed multi-sensor anomaly detection with an honest proxy dataset and an OPC-UA-shaped data path, the kind of bridge between lab methods and plant middleware precision teams need.”

### Precision manufacturing
> “Watch and micro-component cells lose money when wear shows up as scrap. I built a spindle-health board: vibration, temperature, current → health score → maintenance alert, scoped so a production engineer can argue with it on Monday.”

### Microtech SME
> “SMEs rarely have a data science team. I shipped a small Dash monitor with clear green/amber/red states and a mock OPC-UA layer so the architecture is plant-ready without pretending I already have your historian.”

## CV bullet (one line)
Built a Plotly Dash CNC spindle health monitor: CMAPSS-proxy multivariate sensors, Isolation Forest health scoring (0–100), TTF heuristic, mock OPC-UA tags, scoped for precision manufacturing stakeholders.

## Languages
Keep README/docs in English; be ready to walk the dashboard in **French** (status labels, alert meaning, disclaimer). EN/FR UI copy is a natural v1.1 if stakeholders ask for localized shop-floor language.
