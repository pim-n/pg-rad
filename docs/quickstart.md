## Installation

See the [installation guide](installation.md).

## Test your installation

First, see if PG-RAD is available on your system by typing

```
pgrad --help
```

You should get output along the lines of

```
usage: pg-rad [-h] ...

Primary Gamma RADiation landscape tool

...
```

If you get something like `pgrad: command not found`, please consult the [installation guide](installation.md).

You can run a quick test scenario as follows:

```
pgrad --test
```

This should produce a plot of a scenario containing a single point source and a path.

## Running PG-RAD

In order to use the CLI for your own simulations, you need to provide a *config file*. To run with your config, run

```
pgrad --config path/to/my_config.yml
```

where `path/to/my_config.yml` points to your config file.

## Example configs

The easiest way is to take one of these example configs, and adjust them as needed. Alternatively, there is a detailed guide on how to write your own config file [here](config-spec.md).

=== "Example 1"

    The position can be defined relative to the path. `along_path` means at what distance traveled along the path the source is found. If the path is 200 meters long and `along_path` is `100` then the source is halfway along the path. `dist_from_path` is the distance in meters from the path. `side` is the side of the path the source is located. This is relative to the direction the path is traveled.

    ``` yaml
    name: Example 1
    speed: 13.89
    acquisition_time: 1

    path:
      file: path/to/exp_coords.csv
      east_col_name: East
      north_col_name: North

    sources:
      source1:
      activity_MBq: 1000
      isotope: CS137
      position:
        along_path: 100
        dist_from_path: 50
        side: left
    
    detector:
      name: dummy
      is_isotropic: True
    ```

=== "Example 2"

    The position can also just be defined with (x,y,z) coordinates.

    ``` yaml
    name: Example 2
    speed: 13.89
    acquisition_time: 1

    path:
      file: path/to/exp_coords.csv
      east_col_name: East
      north_col_name: North

    sources:
      source1:
        activity_MBq: 1000
        isotope: CS137
        position: [104.3, 32.5, 0]
      source2:
        activity_MBq: 100
        isotope: CS137
        position: [0, 0, 0]
        
    detector:
      name: dummy
      is_isotropic: True
    ```

=== "Example 3"

    This is an example of a procedural path with random apportionment of total length and random angles being assigned to turns. The parameter `alpha` is optional, and is related to randomness. A higher value leads to more uniform apportionment of lengths and a lower value to more random apportionment. More information about `alpha` can be found [here](pg-rad-config-spec.md).

    ``` yaml
    name: Example 3
    speed: 8.33
    acquisition_time: 1

    path:
      length: 1000
      segments:
        - straight
        - turn_left
        - straight
      alpha: 100

    sources:
      source1:
        activity_MBq: 1000
        isotope: CS137
        position: [0, 0, 0]
        
    detector:
      name: dummy
      is_isotropic: True
    ```

=== "Example 4"

    This is an example of a procedural path that is partially specified. Note that turn_left now is a key for the corresponding angle of 45 degrees. The length is still divided randomly

    ``` yaml
    name: Example 4
    speed: 8.33
    acquisition_time: 1

    path:
      length: 1000
      segments:
        - straight
        - turn_left: 45
        - straight

    sources:
      source1:
        activity_MBq: 1000
        isotope: CS137
        position: [0, 0, 0]
        
    detector:
      name: dummy
      is_isotropic: True
    ```

=== "Example 5"

    This is an example of a procedural path that is fully specified. See how length is now a list matching the length of the segments.

    ``` yaml
    name: Example 5
    speed: 8.33
    acquisition_time: 1

    path:
      length:
        - 400
        - 200
        - 400
      segments:
        - straight
        - turn_left: 45
        - straight

    sources:
      source1:
        activity_MBq: 1000
        isotope: CS137
        position: [0, 0, 0]
        
    detector:
      name: dummy
      is_isotropic: True
    ```