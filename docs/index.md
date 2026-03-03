# Welcome!

Primary Gamma RADiation Landscapes (PG-RAD) is a Python package for research in source localization. It can simulate mobile gamma spectrometry data acquired from vehicle-borne detectors along a predefined path (e.g. a road).

## About

This software has been developed as part of dissertation work for the degree of master of Computational Science and Physics at Lund University, Sweden. The work has been done at the department of Medical Radiation Physics (MSF), Faculty of Medicine. The radiological emergency preparedness research group of MSF is assigned by the Swedish Radiation Safety Authority (SSM) to aid in preparation for effective mitigation of radiological or nuclear disasters on Swedish soil.

## Value proposition

PG-RAD is a toolbox that allows for simulation of detector response for a wide variety of source localization scenarios. The strength of the software lies in its simple and minimal configuration and user input, while its flexibility allows for reconstruction of specific scenarios with relative ease. PG-RAD is also general enough that novel methods such as UAV-borne detectors can be simulated and evaluated.

User input takes the form of an input file (YAML), describing the path, detector and source(s), and optional parameters. The output of the program is visualizations of the world (the path and sources), as well as the detector count rate as a function of distance travelled along the path.

Users can provide experimental / geographical coordinates representing real roads. Alternatively, users can let PG-RAD generate a procedural road, where the user can easily control what that road should look like. The user can specify a single point source, several point sources, as well as a field of radioactive material covering a large area.
```

See how to get started with PG-RAD with your own Python code [here](pg-rad-in-python).

## For developers
```
git clone https://github.com/pim-n/pg-rad
cd pg-rad
git checkout dev
```

or

```
git@github.com:pim-n/pg-rad.git
cd pg-rad
git checkout dev
```