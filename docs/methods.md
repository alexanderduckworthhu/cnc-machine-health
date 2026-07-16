# Preprocessing + Isolation Forest + health score

Companion to `REVERSE_ENGINEERING.txt` — code is source of truth.

## 1. Multivariate preprocess

```
raw → plausibility(NaN) → missing flags → ffill(≤3 cycles) → median → StandardScaler
    → windows(30, stride=3) → [mean, std, last, slope] × sensors
```

| Step | Ship bar | Over-build |
|------|----------|------------|
| Missing | ffill limit + median | MICE, Gaussian processes |
| Normalize | global StandardScaler | per-recipe robust scalers |
| Features | 4 stats × 6 channels | FFT, wavelets, embeddings |

## 2. Isolation Forest

```python
IsolationForest(
    n_estimators=200,
    contamination=0.05,
    max_samples="auto",
    random_state=42,
)
# Fit on early IF_HEALTHY_FRACTION (50%) of each machine's cycles
scores = model.decision_function(X)  # higher = more normal
```

## 3. Health formula

```
z = (score - median_healthy) / (1.4826 * MAD_healthy)
health = clip(85 + 12 * z, 0, 100)
```

| Band | Rule | Shop-floor label |
|------|------|------------------|
| Green | ≥ 75 | Looking good |
| Amber | 50–74 | Keep an eye on it |
| Red | < 50 | Needs a look |

## 4. TTF proxy

```
ttf_cycles = 200 * (health/100)^γ
```

γ chosen so health 50 ≈ 40 cycles; hours = cycles × 6 min / 60.  
Label it **proxy** in every UI string that matters.
