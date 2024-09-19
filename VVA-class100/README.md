
---
tags:
- autotrain
- tabular
- classification
- tabular-classification
datasets:
- autotrain-onmwz-zaj9u/autotrain-data
---

# Model Trained Using AutoTrain

- Problem type: Tabular classification

## Validation Metrics

- logloss: 2.272943046648277
- accuracy: 0.22105263157894736
- mlogloss: 2.272943046648277
- f1_macro: 0.15993219916585347
- f1_micro: 0.22105263157894736
- f1_weighted: 0.20550650321389216
- precision_macro: 0.15535396645989202
- precision_micro: 0.22105263157894736
- precision_weighted: 0.2044220893233298
- recall_macro: 0.17603999547363394
- recall_micro: 0.22105263157894736
- recall_weighted: 0.22105263157894736
- loss: 2.272943046648277

## Best Params

- learning_rate: 0.1726579479865136
- reg_lambda: 7.629907124737067
- reg_alpha: 6.272434706281163e-05
- subsample: 0.9479710667281049
- colsample_bytree: 0.7937184578102426
- max_depth: 1
- early_stopping_rounds: 173
- n_estimators: 15000
- eval_metric: mlogloss

## Usage

```python
import json
import joblib
import pandas as pd

model = joblib.load('model.joblib')
config = json.load(open('config.json'))

features = config['features']

# data = pd.read_csv("data.csv")
data = data[features]

predictions = model.predict(data)  # or model.predict_proba(data)

# predictions can be converted to original labels using label_encoders.pkl

```
