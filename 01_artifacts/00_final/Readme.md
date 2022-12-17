## Artefacts

### Project stucture
.
+-- EDA  
¦   L-- Eda.ipynb  
+-- Readme.md  
+-- Recomendations  
¦   +-- Rec_system  
¦   ¦   +-- dashboard  
¦   ¦   ¦   L-- dashboard.py  
¦   ¦   +-- DS  
¦   ¦   ¦   L-- co-author-recommendation.ipynb  
¦   ¦   L-- Rec_api  
¦   ¦       +-- api_params.py  
¦   ¦       +-- co_author_api.py  
¦   ¦       L-- recomendations.json  
¦   L-- train_test_split  
¦       L-- data-split.ipynb  
+-- Topic Modeling  
¦   +-- classification.ipynb  
¦   +-- classification_model_logreg.joblib  
¦   L-- clasterization_pipeline.ipynb  
L-- tree.txt  


## How to run it

### Start server for predictions: Rec_sys_articles
Run this command and wait for "Application startup complete.
" log.

`OMP_NUM_THREADS=1 uvicorn main:app --reload --host 0.0.0.0 --port 8000`