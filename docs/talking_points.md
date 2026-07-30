# Interview talking points (90 seconds)

1. **Why precision manufacturing:** Precision manufacturing lives on spindle uptime and scrap avoidance. I built a cell-health board that speaks vibration / temperature / current, not generic ops dashboards.
2. **Proxy honesty:** NASA CMAPSS run-to-failure remapped to CNC vocabulary. Same degradation shape; different physics. I say that up front.
3. **Method:** Windowed multivariate features → Isolation Forest (fit on healthy regime) → health 0–100 via robust z-score → looking good / keep an eye on it / needs a look. TTF is an explicit heuristic, not a second model.
4. **Industrial detail:** Dashboard reads through an OPC-UA-shaped tag layer (`ns=2;s=CNC-01.Spindle.VibrationRMS`). Mock today; Kepware/TwinCAT tomorrow without rewriting the UI.
5. **Monday message:** Triage red/amber cells first; confirm vibration + current against last tool change; treat TTF as planning order-of-magnitude.
6. **Scope discipline:** Four machines, one unsupervised model, one Dash app, two weekends. I cut LSTM-RUL and live PLC integration on purpose.
