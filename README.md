# Tractors

A full-stack monorepo for a tractor supply machine-learning API.

## Requirements

* Python 3.13
* Docker

## How to Run

First, unzip the machine learning file:

```tar -xzvf app/learning/models/model_supplier.tar.gz```

The, build and run the server with Docker:

```docker build -t server .```

```docker run -d --name servercontainer -p 80:80 server```

Navigate to [localhost:80](http://localhost:80)

### Building the Machine Learning files

These are already built, but if you want to rebuild it, run the following command while the server is running:

```python -c "from app.learning import PartOrderPredictor; predictor = PartOrderPredictor(); predictor.train()"```
