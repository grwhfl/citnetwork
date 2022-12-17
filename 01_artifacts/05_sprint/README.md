## How to run it

### Start server for predictions
Run this command and wait for "Application startup complete.
" log.

`OMP_NUM_THREADS=1 uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Start dashboard
After server started run 

`python3 dashboard.py`