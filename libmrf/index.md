# `mrf`

`mrf` is a Markov random field library written in portable C. 
It requires only an implementation of `malloc`, `free`, and a double precision floating point number.

## Install
You need a C99 compiler and a recent version of CMake (well, if you want to use CMake...otherwise, command line to your heart's content).
Though it contains `#include <stdlib.h>`, that's not actually necessary.
Only `malloc`, `free`, and a double precision floating point number are necessary.

## License etc.
mrf is licensed under the MIT license. Enjoy! Copyright David Rushing Dewhurst, 2024 - present.

## Source code distribution
Source is on [gitlab](https://gitlab.com/drdewhurst/libmrf).
Zip files are [here](./distros/).

## Documentation
[Here](./docs/).