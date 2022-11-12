# `lppl-examples`

Here's a description of some examples of using `lppl`. You can find the source [here](https://gitlab.com/drdewhurst/lppl-examples/-/tree/master/).

## Requirements and installation

To build and run the examples, you need CMake 3.20.0 or newer, a C++20 compiler, and `lppl`. You can get `lppl` by [clicking this link](./distros/lppl-vlatest.zip).
To generate the plots, you need python 3.9 with pandas and matplotlib installed. Create a new conda environment and use the `requirements.txt` if in doubt.

+ Building the examples: `cd build && cmake .. && make`
+ Running the examples: `cd build && ./the_executable`
+ Plotting the examples: `cd src && my/python/install the_plot_script`

## Examples

+ `dynamic.cpp`: rolling your own time series filtering using queryers and importance sampling.
+ `linear-regression.cpp`: linear regression, fast and slow (with worse and better user-defined proposal distributions)
+ `sts.cpp`: *WIP* basic structural time series models in discrete time (for now -- continuous time later)
+ `symbolic-regression.cpp`: symbolic regression over a pure-functional DSL, featuring the simplest interpreter ever


## License etc.

`lppl-examples` is licensed under GPL v3. If you would like a license exception please contact us at [lppl@davidrushingdewhurst.com](mailto:lppl@davidrushingdewhurst.com). Copyright David Rushing Dewhurst, 2022 - present.