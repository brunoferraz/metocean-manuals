# ICON Documentation

Source: https://docs.icon-model.org/land/land.html

---

Land &#8212; ICON documentation

-

[Skip to main content](#main-content)

Back to top

Ctrl+K

[
GitLab](https://gitlab.dkrz.de/icon/icon-model)

-

[
icon-model.org](https://icon-model.org)

# Land[#](#land)

Land models are used with atmospheric circulation models or coupled Earth System Models
in order to provide the lower boundary conditions to the atmosphere. As such, the exchange
of heat, moisture and momentum at the interface between the land surface and the atmospheric
boundary layer is strongly linked to the vertical turbulent diffusion parameterization in the atmospheric
physics. The surface fluxes are computed by solving the energy balance at the surface and by describing
the heat and water dynamics in the sub-surface soil. In setups including an ocean, river
discharge resulting from the surface runoff and sub-surface drainage is also coupled to the
ocean as freshwater flux from the land.

There are two atmospheric physics packages in ICON, [ICON-NWP](../atmosphere/atmosphere.html#ref-atmosphere-nwp-physics) and [ICON-AES](../atmosphere/atmosphere.html#ref-atmosphere-aes-physics).
Historically, [ICON-NWP](../atmosphere/atmosphere.html#ref-atmosphere-nwp-physics)
contained the “turbdiff/turbtran” turbulence parameterization with the [TERRA](#ref-land-terra) land model and [ICON-AES](../atmosphere/atmosphere.html#ref-atmosphere-aes-physics)
the “vdiff” turbulence parameterization with the [ICON-Land](#ref-icon-land) component implementing the [JSBACH](#ref-land-jsbach) land
model. Recently, the [QUINCY](#ref-land-quincy) land model has been implemented in [ICON-Land](#ref-icon-land) as an additional
configuration option. The following configurations are now possible:

-

[ICON-NWP](../atmosphere/atmosphere.html#ref-atmosphere-nwp-physics) with turbdiff/turbtran and [TERRA](#ref-land-terra)

-

[ICON-NWP](../atmosphere/atmosphere.html#ref-atmosphere-nwp-physics) with vdiff and [ICON-Land](#ref-icon-land)/[JSBACH](#ref-land-jsbach) (aka ICON XPP)

-

[ICON-AES](../atmosphere/atmosphere.html#ref-atmosphere-aes-physics) with vdiff and [ICON-Land](#ref-icon-land) (either [JSBACH](#ref-land-jsbach) or [QUINCY](#ref-land-quincy))

to be added: TMX turbulence package, biogeochemical cycles

Literature

See [Literature](../literature/literature.html#ref-land-literature) collection.

# Land Parameterizations[#](#land-parameterizations)

## TERRA[#](#terra)

The multi-layer soil-vegetation-atmosphere-transfer component TERRA can be classified as a second-generation land-surface model with the following characteristics:

-

Infiltration and a multi-layer model for hydrology (Richards equation). The transport of soil water is solved implicitely.

-

Surface and ground-water runoff

-

Multi-layer heat conduction equation (NWP: 7-layer + 1 climate layer; 1 cm - 14.58 m). The solution of the heat transport is solved implicitly.

-

Fractional freezing/melting

-

Evapotranspiration with bare soil evaporation after [Dickinson 1984](../literature/literature.html#term-Dickinson-1984) and [Schulz & Vogel 2020](../literature/literature.html#term-Schulz-Vogel-2020), and transpiration following [Jarvis 1976](../literature/literature.html#term-Jarvis-1976)

-

One-layer snow scheme

-

Skin-layer approach to mimic canopy effects ([Viterbo & Beljaars 1995](../literature/literature.html#term-Viterbo-Beljaars-1995), [Schulz & Vogel 2020](../literature/literature.html#term-Schulz-Vogel-2020))

From a numerical point of view TERRA is coupled explicity to the atmosphere.
TERRA requires a set of external physiographic parameters that hold the information such as e.g. soil type or land-use type.
To address the issue of spatial soil heterogeneity ICON employs tiles. Tiling is done in land-use space, and TERRA is called separately for each tile. Resulting fluxes from the separate tiles are averaged at a blending height of 10 m and passed to the turbulence scheme.

See also Section 3.8.9 of the [ICON Tutorial](../literature/literature.html#term-ICON-Tutorial).

## ICON-Land[#](#icon-land)

[
](../_images/ICON-Land.svg)
[
](../_images/ICON-Land.svg)

ICON-Land is a framework for the modeling of land processes in ICON and can be used as a
stand-alone land surface model as well as in the fully coupled ICON Earth System model or
in the ICON atmosphere-only model. It is specifically designed in a modular way for the
integration of concurrent and alternative process and surface descriptions in a flexible
and easy-to-use way. Currently, specific process implementations include the [JSBACH](#ref-land-jsbach) and
the [QUINCY](#ref-land-quincy) model configurations.

The ICON-Land framework has been designed to systematically separate the infrastructure
necessary to implement physical, biogeophysical and biogeochemical land processes from the
concrete process implementations which are accessed by abstract interfaces. A further goal
was the ability to support different experimental configurations of varying scope and
complexity to be used in different global, regional or single-site applications, coupled
online to an atmosphere model or driven offline by atmospheric observations.

ICON-Land is implemented in an object-oriented and modular way in Fortran2003/2008.
Hierarchical trees are used for the flexible description of surface characteristics (tiles).
Scientific code (processes) is clearly separated from the infrastructure. ICON-Land is a
self-contained package while using only a basic infrastructure for I/O, parallel domain
decomposition, time control, etc. from the ICON model via a relatively small number of
adapter routines.

## JSBACH[#](#jsbach)

JSBACH in ICON-Land (aka JSBACHv4) was initially a re-implementation of JSBACHv3 in the new
framework where JSBACHv3 [Reick et al. 2021](../literature/literature.html#term-Reick-et-al.-2021) has been the land component of the MPI-M ECHAM
and MPI-ESM models used in many modeling studies over the last decades. JSBACHv4 in ICON-Land
includes the fast physical and biogeophysical processes as well as biogeochemical processes
to simulate the natural land carbon cycle, disturbances and anthropogenic and natural land
cover change.

The surface energy balance and the soil thermal layers on land are coupled implicitly to the
vdiff vertical diffusion scheme. Plant productivity by photosynthesis, phenology (leaf area
index), roughness lengths for momentum and heat, and visible and near-infrared albedos are
computed on a flexible number of tiles representing sub-grid surface heterogeneity by plant
functional types. Heat and water dynamics in the soil are described to a depth of about 10 m
and are coupled to calculations of surface runoff and sub-surface drainage and the resulting
river discharge through a hydrologic discharge model ([Hagemann & Duemenil 1997](../literature/literature.html#term-Hagemann-Duemenil-1997), [Riddick et al. 2018](../literature/literature.html#term-Riddick-et-al.-2018)).
A five-layer snow model is applied and the soil dynamics include freezing water and phase changes
between liquid and frozen water ([Ekici et al. 2014](../literature/literature.html#term-Ekici-et-al.-2014), [de Vrese et al. 2021](../literature/literature.html#term-de-Vrese-et-al.-2021)).

## QUINCY[#](#quincy)

QUINCY (QUantifying Interactions between terrestrial Nutrient CYcles
and the climate system, [Thum et al. 2019](../literature/literature.html#term-Thum-et-al.-2019)) has been developed at the MPI for
Biogeochemistry as an alternative, more comprehensive representation of biogeochemical
processes for ICON-Land. QUINCY is integrated with ICON-Land through a set of defined
interfaces that affect the biological control of the land surface’s radiation balance,
momentum and heat transfer as well as its water balance. It follows a modular design
that allows to integrate fundamental, fast biospheric processes with increasing degree
of complexity from a prescribed phenology mode, a vegetation dynamics mode to a fully
coupled BGC vegetation-soil model. QUINCY also serves as test-bed for novel model
components, e.g. representations of soil biogeochemical processes ([Yu et al. 2020a](../literature/literature.html#term-Yu-et-al.-2020a),
[Yu et al. 2020b](../literature/literature.html#term-Yu-et-al.-2020b)).

QUINCY simulates the element cycling of carbon, nitrogen, and phosphorus in terrestrial
ecosystems, and includes novel representations of source/sink limited plant growth; the
acclimation of many ecophysiological processes; an explicit representation of vertical
soil processes to separate litter and soil organic matter dynamics; a range of new
diagnostics (leaf chlorophyll; isotope tracers) to allow for a more in-depth model
evaluation. Case-studies include the evaluation against standard biosphere benchmarks
[Thum et al. 2019](../literature/literature.html#term-Thum-et-al.-2019), in particular ecosystem manipulation experiments [Caldararu et al. 2020](../literature/literature.html#term-Caldararu-et-al.-2020)
as well as long-term monitoring data [Caldararu et al. 2021](../literature/literature.html#term-Caldararu-et-al.-2021).

# Dynamic Vegetation[#](#dynamic-vegetation)

to be added

# Carbon Cycle[#](#carbon-cycle)

to be added

On this page

so the DOM is not blocked -->