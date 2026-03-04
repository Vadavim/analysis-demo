# analysis-demo
This repository is meant to demonstrate analysis of sample transaction and shipment data. There are two key components of the demonstration:

1. Jupyter notebooks with basic plotting and forecasting of time series dating using sktime.

2. A prototype of a dashboard using streamlit.

## Installation Instructions

To run the notebooks and streamlit server, you first need to install the python virtual environment. 

### Option 1: Installation through bash script
While in the repository, run:

```
bash install.sh
```
This will create a virtual environment located in `.env/`.
To enter the environment, run:

```
source source.sh
```
You should see (.env) next to your command line prompt if successful.

## Option 2: Manual installation
While in the root directory of the project, you can run:
```
  python3 -m venv .env
  source .env/bin/activate
  pip3 install -e .
```
(you may need to replace python3 and pip3 in the commands with python and pip depending on your python installation)

## Data Folder
The data required for this demonstration is not included. You will need to move them into the `data/` direction. The following files are expected: 

`data/SHIFT_SCHEDULE.csv`   
`data/WAREHOUSE_TRANSACTIONS.csv`   
`data/WAREHOUSE_SHIPMENTS.csv`  

## Running Streamlit
Within the virtual environment, in the root directory of the project, run:

```
streamlit run jsr/app.py
```
This will launch the dashboard in your browser locally.

## Running Jupyter Notebooks
To run a local jupyter notebook server while in the virtual environment, from the root of the project directory, run:

```
cd notebooks
jupyter lab
```

