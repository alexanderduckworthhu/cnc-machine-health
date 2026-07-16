# Deploy (Render or Railway)

## Render
1. New **Web Service** from this folder (or its own git repo).
2. Build: `pip install -r requirements.txt && python scripts/build_demo_data.py && python scripts/train_isolation_forest.py`
3. Start: `gunicorn app:server --bind 0.0.0.0:$PORT`
4. Health check path: `/`

## Railway
1. New project → deploy from directory `cnc-machine-health`.
2. Start command: `gunicorn app:server --bind 0.0.0.0:$PORT`
3. Add a pre-deploy / start hook that runs the two scripts above if `data/processed/machine_snapshots.json` is missing (`app.py` also bootstraps on first boot).

## Env
No secrets required for the demo. Do not commit plant credentials if you later point the OPC-UA client at a real endpoint.

## Post-deploy
- Paste the URL into `README.md`
- Record a 90s walkthrough clicking a red card → sensor spike → alert text
