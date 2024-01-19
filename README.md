# Label Studio Setup

This repository holds all of the information needed on how to setup label-studio. Data can be uploaded to the label-studio frontend by generating tasks via the import_data.py script. The 'config' folder holds txt files which contain lists of samples that should be uploaded. Config files can be created from scratch or generated by the 'generate_dataset_config.py' script which ouputs a list of all of the samples in a directory.

## Setting up your API key

First of all, set up your API key by creating a file called ".api_key.txt" and copy pasting the key which can be found in the label-studio frontend settings under "Account & Settings" -> "Access Key". Make sure there are no trailing new-line characters at the end of your key.

## Making sure the data is hosted on the nginx server

If you acquired new data and store it on the server, make sure to edit the "docker-compose.yml" file for the label-studio frontend and mount the directory holding the data in the volumes section. Just add a bulletpoint in the volumes section and follow the <code>\<source>:/srv/\<dataset-name>:r</code> template. Keep track of the <code>\<dataset-name></code> as you will need it when creating tasks / uploading data.

![Docker-compose with volumes mounted.](/media/docker-compose.png "Docker-compose file.")

## Generating a configuration file

To generate a configuration file which holds relative paths to all samples, one can use the 'generate_dataset_config.py' file.

```
python3 generate_dataset_config.py <dataset-name> <dataset-root>
```

The config file should be written to the config folder and called whatever was set as <code>\<dataset-name></code>. If certain samples in the list should be ignored one can just add a <code>#</code> in front of the sample.

## Upload data to label-studio

The final step now is to upload the data. To do so, first, it is important to differentiate what the labeling should look like. Currently there are two options. One is to label subsequences in longer sequences which should be cut up later. The other one is to annotate bounding boxes for objects one would like to track. For sequences, the corresponding integer is 0, for bounding boxes its 1. or the latter, depending on what exactly should be labeled, one can adjust the config file in <code>label_config/bounding_box_config.xml</code> such that it represents what should be labeled. Then, simply run the following command in order to upload the data:

```
python3 import_data.py -p <project-name> -t 0 -d <path-to-dataset-root> -c <path-to-dataset-config> -n <dataset-name>
```

The flag <code>-t</code> represents the aforementioned type of labeling project. 0: subsequences, 1: bounding boxes. Again, it is crucial that the <code>\<dataset-name></code> matches the one in the docker-compose file which states how the data is mounted on the hosting server.
