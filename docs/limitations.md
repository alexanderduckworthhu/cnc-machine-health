# Limitations

These are known constraints of the current implementation —
properties of the industrial ML problem and demo scope,
not defects to hide.

1. **NASA CMAPSS is turbofan, not CNC.**
   Degradation physics differ; jet engine run-to-failure
   has a different wear curve than CNC spindle wear.
   The proxy dataset is appropriate for demonstrating
   the pipeline architecture and anomaly detection
   approach — not for claiming physical fidelity to
   a specific machine type.

2. **No real failure labels.**
   Isolation Forest is unsupervised — it learns
   "statistically different from the healthy regime,"
   not "this pattern precedes failure." Time-to-failure
   is a planning-order-of-magnitude heuristic derived
   from the anomaly score trajectory, not a second
   predictive model.

3. **Thresholds are dataset-relative, not machine-calibrated.**
   Green / amber / red bands are set against CMAPSS
   statistics. A production deployment would require
   per-machine, per-factory calibration against actual
   healthy baselines and confirmed failure events.

4. **Mock OPC-UA layer.**
   The tag namespace mirrors real Kepware / TwinCAT
   structure (`ns=2;s=CNC-01.Spindle.VibrationRMS`)
   but reads from in-memory demo data, not a live PLC
   or historian. The architecture is plant-ready;
   the data path is not yet wired.

5. **No tool-change or recipe context.**
   Vibration and current draw change with cutting
   parameters, material, and tool condition. Without
   that metadata, some amber alerts will be false
   positives on heavy cuts or tool changes rather
   than genuine spindle degradation.

6. **Four-machine demo scope.**
   Fleet-level statistics — peer comparison, site-wide
   health trends, cross-machine anomaly correlation —
   require a larger machine population to be
   statistically meaningful. The current scope is
   sufficient for demonstrating the cell-health concept.

7. **Single unsupervised model.**
   LSTM-RUL and supervised failure classification were
   deliberately cut from v1 to keep scope tight and the
   method explainable. A production system would layer
   supervised models once labeled failure data is
   available from the plant historian.
