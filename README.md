# Tractors

A full-stack monorepo for a tractor supply machine-learning API.

## Requirements

* Python 3.13
* Docker

## How to Run

```docker build -t server .```

```docker run -d --name servercontainer -p 80:80 server```

Navigate to [localhost:80](http://127.0.0.1:80)

### Building the Machine Learning files

These are already built, but if you want to rebuild it, run the following command while the server is running:

```python -c "from app.learning import PartOrderPredictor; predictor = PartOrderPredictor(); predictor.train()"```
