# Ship checklist, 2 weekends

## Weekend 1: Data + model
- [x] Synthetic CMAPSS-proxy fleet (`scripts/build_demo_data.py`)
- [x] Preprocess: plausibility → miss flags → ffill → median
- [x] Window features (mean/std/last/slope), stride 3
- [x] Isolation Forest on healthy regime + robust-z health + status bands
- [x] Snapshots + alerts JSON
- [x] Smoke tests (`pytest`)

**Ship bar:** model runs offline; four machines show distinct statuses.  
**Stop if tempted to:** train LSTM autoencoders, download all CMAPSS subsets, build a feature store.

## Weekend 2. Dashboard + industrial veneer + deploy
- [x] Dash layout: cards, sensor traces, alert feed
- [x] Mock OPC-UA server/client with realistic NodeIds
- [x] README + talking points + manufacturing framing
- [x] REVERSE_ENGINEERING.txt
- [ ] Deploy to Render or Railway (`docs/deploy.md`)
- [ ] Record 90s Loom walkthrough
- [ ] Optional: drop real `train_FD001.txt` into `data/raw/` and call `load_cmapss_txt`

**Ship bar:** public URL + honest disclaimer + one crisp LinkedIn post.  
**Stop if tempted to:** real OPC-UA TCP with certificates, user auth, multi-tenant plants, MQTT + InfluxDB.

## Definition of done
1. `pytest -q` green  
2. `python app.py` shows mixed green/amber/red cards  
3. You can explain health formula + OPC-UA mock in under 90 seconds  
4. Sibling projects untouched
