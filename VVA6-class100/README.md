
---
tags:
- autotrain
- tabular
- classification
- tabular-classification
datasets:
- VVA6-class100/autotrain-data
---

# Model Trained Using AutoTrain

- Problem type: Tabular classification

## Validation Metrics

- logloss: 2.263057582834152
- accuracy: 0.21403508771929824
- mlogloss: 2.263057582834152
- f1_macro: 0.13485997674881267
- f1_micro: 0.21403508771929824
- f1_weighted: 0.19487415178434858
- precision_macro: 0.13175645751759482
- precision_micro: 0.21403508771929824
- precision_weighted: 0.18920840565759028
- recall_macro: 0.15085162739624983
- recall_micro: 0.21403508771929824
- recall_weighted: 0.21403508771929824
- loss: 2.263057582834152

## Best Params

- learning_rate: 0.20256554278291938
- reg_lambda: 0.004161057969921168
- reg_alpha: 5.553816489232514
- subsample: 0.9871535957429787
- colsample_bytree: 0.9737688940097069
- max_depth: 1
- early_stopping_rounds: 443
- n_estimators: 20000
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
