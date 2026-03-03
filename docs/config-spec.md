!!! note
    To get started quickly, you may copy and modify one of the example configs found [here](quickstart.md#example-configs).


The config file must be a [YAML](https://yaml.org/) file. YAML is a serialization language that works with key-value pairs, but in a syntax more readable than some other alternatives. In YAML, the indentation matters. I


The remainder of this chapter will explain the different required and optionals keys, what they represent, and allowed values. 

## Required keys

### Simulation options

The first step is to name the simulation, and define the speed of the vehicle (assumed constant) and acquisition time.

#### Landscape name

The name is a string, which may include spaces, numbers and special characters.

Examples:

```yaml
name: test_landscape
```
```yaml
name: Test Landscape 1
```

#### Acquisition time

The acquisition time of the detector in seconds.

Example:

```yaml
acquisition_time: 1
```

!!! note
    All units in the config file must be specified in SI units, e.g. meters and seconds, unless the key contains a unit itself (e.g. `activity_MBq` means activity in MegaBequerels).

#### Vehicle speed

The speed of the vehicle in m/s. Currently, the vehicle speed must be assumed constant. An example could be

```yaml
speed: 13.89 # this is approximately 50 km/h
```

!!! note
    The text after the `#` signifies a comment. PG-RAD will ignore this, but it can be helpful for yourself to write notes.


### Path

The `path` keyword is used to create a path for the detector to travel along. There are two ways to specify a path; from experimental data or by specifying a procedural path.

#### Path - Experimental data

Currently the only supported coordinate format is the RT90 (East, North) coordinate system. If you have experimental data in CSV format with columns for these coordinates, then you can load that path into PG-RAD as follows:

```yaml
path:
  file: path/to/experimental_data.csv
  east_col_name: East
  north_col_name: North
```

#### Path - Procedural path

Alternatively, you can let PG-RAD generate a path for you. A procedural path can be specified with at least two subkeys: `length` and `segments`. 

Currently supported segments are: `straight`, `turn_left` and `turn_right`, and are provided in a list under the `segments` subkey as follows:

```yaml
path:
  segments:
    - straight
    - turn_left
    - straight
```

The length must also be specified, using the `length` subkey. `length` can be specified in two ways: a list with the same length as the `segments` list

```yaml
path:
  segments:
    - straight
    - turn_left
    - straight
  length:
    - 500
    - 250
    - 500
```

which will assign that length (meters) to each segment. Alternatively, a single number can be passed:

```yaml
path:
  segments:
    - straight
    - turn_left
    - straight
  length: 1250
```

Setting the length for the total path will cause PG-RAD to *randomly assign* portions of the total length to each segment.

Finally, there is also an option to specify the turn angle in degrees:

```yaml
path:
  segments:
    - straight
    - turn_left: 90
    - straight
  length: 1250
```

Like with the lengths, if a turn segment has no angle specified, a random one (within pre-defined limits) will be taken.

!!! warning
    Letting PG-RAD randomly assign lengths and angles can cause (expected) issues. That is because of physics restrictions. If the combination of length, angle (radius) and velocity of the vehicle is such that the centrifugal force makes it impossible to take this turn, PG-RAD will raise an error. To fix it, you can 1) reduce the speed; 2) define a smaller angle for the turn; or 3) assign more length to the turn segment.

!!! info
    For more information about how procedural roads are generated, including the random sampling of lengths and angles, see X

### Sources

Currently, the only type of source supported is a point source. Point sources can be added under the `sources` key, where the **subkey is the name** of the source:

```yaml
sources:
  my_source: ...
```

the source name should not contain spaces or special characters other than `_` or `-`. There are three required subkeys under `sources.my_source`, which are: `activity_MBq`, `isotope` and `position`.

#### Source activity

The source activity is in MegaBequerels and must be a strictly positive number:

```yaml
sources:
  my_source:
    activity_MBq: 100
```

#### Source isotope

The isotope for the point source. This must be a string, following the naming convention of the symbol followed by the number of nucleons, e.g. `Cs137`:

```yaml
sources:
  my_source:
    activity_MBq: 100
    isotope: Cs137
```

!!! info
    Currently the following isotopes are supported: `Cs137`

#### Source position

There are two ways to specify the source position. Either with absolute (x,y,z) coordinates

```yaml
sources:
  my_source:
    activity_MBq: 100
    isotope: Cs137
    position: [0, 0, 0]
```

or relative to the path, using the subkeys `along_path`, `dist_from_path` and `side`

```yaml
sources:
  my_source:
    activity_MBq: 100
    isotope: Cs137
    position:
      along_path: 100
      dist_from_path: 50
      side: left
```

Note that side is relative to the direction of travel. The path will by default start at (x,y) = (0,0) and initial heading is parallel to the x-axis.

### Detector

The final required key is the `detector`. Currently, only isotropic detectors are supported. Nonetheless, you must specify it with `name`, `is_isotropic` and `efficiency`:

```yaml
detector:
  name: test
  is_isotropic: True
  efficiency: 0.02
```

Note there are some existing detectors available, where efficiency is not required and will be looked up by PG-RAD itself:

```yaml
detector:
  name: NaIR
  is_isotropic: True
```

## Optional keys

The following subkeys are optional and should be put under the `options` key.

```yaml
options:
  air_density_kg_per_m3: 1.243
  seed: 1234
```