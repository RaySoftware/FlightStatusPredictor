Flight Status Predictor

Welcome to Flight Status Predictor, an application that predicts if a flight may be cancelled, delayed, or on time. It does so using decision trees trained on 6 million tuples containing flight information.

Prerequisites

Python 3.10.12 or greater.
Jupyter Lab

## Instructions

### Install Models and Dictionaries
Run the final notebook provided. The notebook will create the following pickles:

Airline_unique.pickle
Dest_unique.pickle
DestCityName_unique.pickle
DestStateName_unique.pickle
flight_predictor_model.pickle (model)
Month_unique.pickle
Origin_unique.pickle
OriginCityName_unique.pickle
OriginStateName_unique.pickle

Save these on a "/pickles/" folder on the same level as the src directory.

### Install dependencies via

```
pip install sklearn
pip install pickle
pip install ttkbootstrap
```

### Run
```
python3 main.py
```