# ICON Documentation

Source: https://docs.icon-model.org/buildrun/buildrun_quickstart.html

---

Quick Start &#8212; ICON documentation

-

[Skip to main content](#main-content)

Back to top

Ctrl+K

[
GitLab](https://gitlab.dkrz.de/icon/icon-model)

-

[
icon-model.org](https://icon-model.org)

# Quick Start[#](#quick-start)

## Obtaining the Code[#](#obtaining-the-code)

ICON is simultaneously developed in several repositories. There is the primary repository [icon](https://gitlab.dkrz.de/icon/icon) and several secondary ones: [icon-nwp](https://gitlab.dkrz.de/icon/icon-nwp), [icon-mpim](https://gitlab.dkrz.de/icon/icon-mpim), etc. If unsure, use the primary repository. If you don’t have access to any of those, choose the public [icon-model](https://gitlab.dkrz.de/icon/icon-model) repository.

Clone the ICON repository of choice and its submodules using the following command:

git clone --recursive https://gitlab.dkrz.de/icon/icon-model.git

Users with a DKRZ GitLab account are recommended to clone the repository via the SSH protocol:

git clone --recursive git@gitlab.dkrz.de:icon/icon-model.git

## Configuring and Building[#](#configuring-and-building)

The configuration step is typically executed by running the [configure](https://gitlab.dkrz.de/icon/icon-model/-/blob/icon-2025.10-2-public/configure) script with command-line arguments. These arguments specify the locations of libraries and tools needed for building. Note that the list of arguments required for successful configuration can be lengthy and complex, so it’s recommended to use a platform- or machine-specific configure wrapper, which automatically sets the necessary compiler and linker flags along with the recommended configuration options. You can find the configure wrappers in the respective subdirectories of the [config](https://gitlab.dkrz.de/icon/icon-model/-/blob/icon-2025.10-2-public/config) directory.

For example, to build ICON on [Levante&#64;DKRZ](https://docs.dkrz.de/doc/levante/index.html) with OpenMP enabled using the Intel compiler, run the following command:

./config/dkrz/levante.intel --enable-openmp

Alternatively, you can create a directory and perform an out-of-source build:

mkdir build && cd build
/path/to/icon/config/dkrz/levante.intel --enable-openmp

Using an out-of-source build, you can build ICON in multiple configurations using the same copy of the source code.

The building step is done by running make command with an optional argument specifying the number of jobs to run simultaneously. Usually, 8 is a good choice. For example:

make -j8

The result of the building — the executable file of ICON — is saved to the bin subdirectory of the build directory.

ICON on your system

If you want to build and run ICON on your personal computer, consider using the [generic configure wrapper](buildrun_building.html#ref-buildrun-configuration-wrappersgeneric).
For detailed information on [Configuration](buildrun_building.html#ref-buildrun-configuration) and [Building](buildrun_building.html#ref-buildrun-building) please refer to the respective section.

## Running ICON[#](#running-icon)

To run ICON, you need to create a runscript that sets the required environment variables and calls the executable. One way to get started with running ICON is to use the [mkexp](https://gitlab.dkrz.de/esmenv/mkexp) utility to generate a runscript and experimental configuration for the “bubble” test.

../utils/mkexp/mkexp bubble.config

The command above generates a runscript called ../experiments/bubble/scripts/bubble.run_start. To execute the experiment, navigate to the directory containing the script and submit it for the execution:

cd ../experiments/bubble/scripts
sbatch bubble.run_start

The output will be directed to the Work directory identified after the execution of mkexp.

Running ICON

For detailed information please refer to section [Running ICON](buildrun_running.html#ref-buildrun-running).

# FAQ[#](#faq)

-

[I run the configure script without any arguments and it fails. What should I do?](#faq1)

First, we recommend checking whether there is a suitable [Configure wrappers](buildrun_building.html#ref-buildrun-configuration-wrappers) in the [config](https://gitlab.dkrz.de/icon/icon-model/-/blob/icon-2025.10-2-public/config) directory that you could use instead of running the configure script directly. If that is not the case, you need at least to specify the LIBS variable telling the configure script which libraries to link the executables to. The content of the list depends on the configure options you specify (see [Table 1](buildrun_building.html#tab-icon-depgraph)), for example:

./configure --disable-mpi --disable-coupling LIBS='-lnetcdff -lnetcdf -llapack -lblas'

If the libraries reside in nonstandard directories, you might also need to specify the FCFLAGS, CPPFLAGS, and LDFLAGS variables to tell the script which directories need to be searched for header and library files (see section [Configuration](buildrun_building.html#ref-buildrun-configuration)) for more details).

-

[How can I reproduce the configuration of the model used in a Buildbot test?](#faq2)

Scripts run by Buildbot for configuration and building of the model reside in the config/buildbot directory. You can run them manually on the corresponding machine.

-

[I get an error message from the configure script starting with “configure: error: unable to find sources of…”. What does this mean?](#faq3)

Most probably, you forgot to initialize and/or update git submodules. You can do that by switching to the source root directory of ICON and running the following command:

git submodule update --init

-

[I have problems configuring/building ICON. What is the most efficient way to ask for help?](#faq4)

Whoever you ask for help will appreciate receiving the log files. You can generate a tarball with the log files by running the following commands from the root build directory of ICON:

make V=1 2>&1 | tee make.log
tar --transform 's:^:build-report/:' -czf build-report.tar.gz $(find . -name 'config.log' -o -name 'CMakeCache.txt') make.log

The result of the commands above will be file build-report.tar.gz, which should be attached to the very first email describing your problem. Please, do not forget to specify the repository and the branch that you experience the issue with, preferably in the form of a URL (e.g. [https://gitlab.dkrz.de/icon/icon-model/-/tree/icon-2025.10-2-public](https://gitlab.dkrz.de/icon/icon-model/-/tree/icon-2025.10-2-public)).

On this page

so the DOM is not blocked -->