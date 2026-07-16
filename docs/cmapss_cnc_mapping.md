# NASA CMAPSS as a CNC proxy

## Why CMAPSS at all?
NASA CMAPSS is a **public run-to-failure multivariate time series**. Hiring managers in manufacturing rarely care about turbofans — they care that you can:
1. clean multi-sensor streams,
2. detect unusual windows without labeled failures,
3. turn scores into **triage language** (health / status / estimated remaining life).

CMAPSS gives you (1)–(3) without needing NDA plant data.

## Honest framing sentence (memorize)
> “I used NASA CMAPSS degradation trajectories as a **stand-in** for CNC spindle wear. I remapped informative channels into vibration, temperature, and current/load — the triad a micro-machining lead expects — and I say out loud that the physics differ.”

## Column map (FD001-style → CNC vocabulary)

| CMAPSS column | CNC proxy name | Manufacturing story |
|---------------|----------------|---------------------|
| `sensor_11` | `vibration_rms` | Spindle housing vibration energy (bearing / imbalance) |
| `sensor_15` | `vibration_peak` | Transient peaks (tool hit, chatter onset) |
| `sensor_2` | `temperature_spindle_c` | Spindle thermal drift (preload / lubrication) |
| `sensor_3` | `temperature_coolant_c` | Coolant loop health (heat rejection) |
| `sensor_4` | `current_draw_a` | Spindle motor current (cutting load / friction) |
| `sensor_7` | `load_pct` | Axis / process load percentage |

Operating settings (`op_setting_*`) are **not** mapped in v1 — treat them as future “recipe / fixture mode” features if you expand.

## How to talk about units
Synthetic demo data is already in CNC-ish units (mm/s, °C, A, %).  
If you load real CMAPSS `.txt` via `src/demo_data.load_cmapss_txt`, values are **min-max rescaled** into plausible CNC bands for demo readability — say that in interviews.

## What NOT to say
- “This predicts Swatch Group machine failures.”
- “Turbofan sensor_11 *is* vibration.”
- “TTF is certified remaining useful life.”

## What TO say
- “Same structure as plant CM: healthy regime → progressive wear → end of life.”
- “Unsupervised triage first; labeled RUL later when the plant has work orders.”
- “OPC-UA-shaped client so the architecture matches industrial middleware.”
