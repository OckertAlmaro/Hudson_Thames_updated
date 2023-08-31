# Hudson_Thames_updated
Better and improved version for calculating bars

This is a prototype framework to calculate the time, volume, and tick bars for financial data.

## Installation
**1. Clone into Hudson_Thames repositor**

On your local laptop, open the terminal. Follow the instructions step by step.
- ```mkdir ~/repos```
- ```cd ~/repos```
- ```git clone https://github.com/OckertAlmaro/Hudson_Thames_updated.git```

**2. Install Dependancies**

Install dependencies as shown below.

- ```pip install pandas```
- ```pip install numpy```
- ```pip install datetime```
- ```pip install math```

## Running Hudson_Thames
**1. Load data**

Copy the text/csv file containing the financial data you wish to analyse into the same directory as the main python script (bars.py), that is in the directory ~repos/Hudson_Thames_updated/tickbars/

**2. Obtaining bars**

Relatively simple, you just need to run the bars.py script.

- ```cd ~/repos/Hudson_Thames/tickbar/```
- ```python bars.py```

To run the unit tests,
- ```cd ~/repos/Hudson_Thames/tickbar/tests/```
- ```python test_bar.py```
