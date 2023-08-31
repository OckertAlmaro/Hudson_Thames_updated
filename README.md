# Hudson_Thames_updated
Better and improved version for calculating bars

This is a prototype framework to calculate the time, volume, and tick bars for financial data.

## Installation
**1. Install Dependencies**

On your local laptop, open the terminal and install dependencies as shown below. Follow the instructions step by step.
- ```mkdir ~/repos```
- ```cd ~/repos```
- ```git clone https://<username>@bitbucket.org/must_research/knowit.git```


**2. Clone into KnowIt repository**

Ensure you have git installed and clone repository to desired location. Eg:

- ```mkdir ~/repos```
- ```cd ~/repos```
- ```git clone https://<username>@bitbucket.org/must_research/knowit.git```

**3. Create virtual environment**

Create new conda environment:

- ```cd ~/repos/knowit```
- ```conda env create -n knowit -f environment.yml```

Activate environment (knowit, should show in brackets in your terminal)

- ```conda activate knowit```

Install the appropriate [Cuda](https://pytorch.org/get-started/locally/) package if you plan on using your GPU for 
training networks.

(Optional) Update Conda when you are done installing everything:

- ```conda update -n base -c defaults conda```

**4. Personalize user paths**

Before running any scripts, please take the time to personalize the paths in env.env_user to your liking. 
It defines where everything is saved and logged.

## Preparing a model
**1. Train a model**

All operations are initialized with the main_proc.py script.
To train a model use the following command (assuming your environment is active and you are in the right directory):

- ```python main_proc.py train configs/tcn_ETTh1_baseline.yaml```

Here,  'configs/tcn_ETTh1_baseline.yaml' is a path to a config file that defines the specifics of the model to be trained.
You can create your own config file. See the comments in the example config file for details.
By default, knowit will train the model and log the per-iteration train loss and per-epoch validation loss as tensorboard parameters.

To view these curves: 
    Navigate to model out directory:
    
- ```cd projects/knowit/trained_models/model_name```

Locate the tensorboard log directory:

- ```cd tensorboard_logs/model_name```

Run the following command (with your environment activated):

- ```tensorboard --logdir logs```

You can now go to http://localhost:6006/ in your browser to view the logged parameters in realtime or after training.

**2. Rate a model**

By default, knowit will rate the performance of the model on the train, validation, and evaluation sets after training.
The results are captured in pickles and accompanying plots in the model out directory (default: projects/knowit/trained_models/model_name)
You can also initiate this rating functionality manually:

- ```python main_proc.py load configs/tcn_ETTh1_baseline.yaml```

## Preparing a custom dataset
To prepare a custom dataset use the following command (assuming your environment is active and you are in the right directory):

- ```python main_proc.py --d_tag my_new_dataset_tag prep_data ~/path_to_some_directory```

The last parameter is a path to a local directory containing your raw data with the following assumptions:

1. Provided directory must contain a number of pickle files

2. Each pickle file contains one pandas dataframe

3. Each dataframe is time indexed.

4. All dataframe must have the same headers.

5. No dataframe can contain an all-nan column. That frame will be skipped.

6. Drops duplicate time indices in each pickle and assumes duplicate time

7. indices across pickles are independent events.

8. Assumes identical frequencies.

Knowit will construct a file 'knowit/datasets/my_new_dataset_tag_data.pickle'.
This file can now be used by knowit to train models with the following command:

- ```python main_proc.py --d_tag my_new_dataset_tag train configs/a_new_config_file.yaml```

Just be sure to update the required parameters in the new config file, under the 'Dataset' and 'Custom data' sections.


## Interpreting a model

To interpret a model use the following command (assuming your environment is active and you are in the right directory):

- ```python main_proc.py --i_tag deepliftshap interpret configs/tcn_ETTh1_baseline.yaml```

There are also some optional parameters that can be set in explain_proc.py.

By default knowit will:

1. Interpret on the evaluation set.

2. Start interpreting at the first time step of the first sequence in the set.

3. Interpret on all target features.

4. Save the interpretation in the model analysis directory (default: projects/knowit/interpretations/model_name)
