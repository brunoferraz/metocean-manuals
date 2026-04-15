# ICON Documentation

Source: https://docs.icon-model.org/atmosphere/atmosphere.html

---

Atmosphere &#8212; ICON documentation

-

[Skip to main content](#main-content)

Back to top

Ctrl+K

[
GitLab](https://gitlab.dkrz.de/icon/icon-model)

-

[
icon-model.org](https://icon-model.org)

# Atmosphere[#](#atmosphere)

The ICON atmosphere model predicts the spatio-temporal evolution
of the atmospheric state in terms of the prognostic variables
virtual potential temperature, 3D wind, total air density
and mass fractions of atmospheric water constituents and trace gases.
In addition, the model provides a comprehensive set of diagnostic quantities,
such as surface pressure, wind gusts or potential vorticity
just to name a few. An extensive, but still incomplete list of available
output variables is provided in Appendix A of the [ICON Tutorial](../literature/literature.html#term-ICON-Tutorial).

In mathematical terms, the ICON atmosphere model solves the fully compressible non-hydrostatic
Navier-Stokes equations on the sphere. The explicitly resolved scales of
motion are treated by the so called [Dynamical Core](#ref-atmosphere-dycore).
The latter is accompanyied by a set of physical parameterizations which account for the effect motions
that fall below a chosen mesh size.
ICON offers two different physics packages which are known as the AES Physics Package and the NWP Physics Package.

The [AES Physics Package](#ref-atmosphere-aes-physics) was originally derived from the physics package of the ECHAM model and subsequently further developed.
Applications range from general circulation model on long time scales to km-scale, storm-resolving climate simulations.
The [AES Physics Package](#ref-atmosphere-aes-physics) can be chosen by setting the namelist parameter [iforcing](#term-iforcing)=2.

The [NWP Physics Package](#ref-atmosphere-nwp-physics) parameterizations were chosen from different sources, most notably the [COSMO-Model](https://www.cosmo-model.org) and the [IFS model](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model).
Originally developed for numerical weather prediction, the [NWP Physics Package](#ref-atmosphere-nwp-physics) was extended for seamless application across scales.
The [NWP Physics Package](#ref-atmosphere-nwp-physics) can be activated by setting [iforcing](#term-iforcing)=3.

## Dynamical Core[#](#dynamical-core)

The dynamical core can be considered as the foundations of any numerical model.
It predicts the evolution in space and time of all
atmospheric motions which are resolvable on a given mesh.
To this end, the dynamical core solves the Euler equations which is a set
of partial differential equations describing adiabatic and inviscid flow.
There exist various approximative forms of the Euler equations in which
certain types of motion are filtered out that are difficult to handle numerically.
Well known examples are the hydrostatic form or the Boussinesq form,
both of them not supporting the propagation of acoustic waves.

The ICON dynamical core solves the fully compressible form of the Euler
equations, which does support acoustic waves.
Notable approximations to the exact Euler equations relate to the treatment
of the Earth as a spherical geoid and the shallow atmosphere approximation
(see e.g. [Thuburn & White 2013](../literature/literature.html#term-Thuburn-White-2013)).
The latter may be deactivated with the Namelist switch
[ldeepatmo](#term-ldeepatmo)=.TRUE., leading to the so called deep atmosphere form of the
governing equations ([Borchert et al. 2019](../literature/literature.html#term-Borchert-et-al.-2019)). Given a suitable set of physical
parameterizations, this allows for simulations on model domains
reaching all the way up to the lower thermosphere.

The governing set of equations is discretized on an Icosahedral-triangular C-grid
in horizontal directions, while in vertical direction a height-based terrain following
coordinate with Lorenz-type staggering of the prognostic variables is used.
The discrete numerical operators, such as the divergence,
gradient or laplace operator, are constructed using a mixture of finite
difference and finite volume discretizations of mostly second order-accuracy.
They are combined with a predictor-corrector type two-level time integration
scheme, leading to a discretization which is mass conserving, but not strictly
energy conserving.

For additional details on the dynamical core, the reader is referred to [Zaengl et al. 2015](../literature/literature.html#term-Zaengl-et-al.-2015)
and Chapter 3 of the [ICON Tutorial](../literature/literature.html#term-ICON-Tutorial).

## Tracer Transport[#](#tracer-transport)

The tracer transport module is an important building block of any weather
prediction or climate model.
It solves the tracer mass continuity equation,
in order to describe the redistribution of gaseous, liquid or solid
atmospheric constituents such as water vapour or rain water due to air
motion or gravitational settling (sedimentation).

In ICON, finite volume methods of second order accuracy in time and up to fourth order accuracy
in space are applied to construct mass conserving and mass consistent transport schemes.
If needed, these schemes can be combined with monotonicity or positivity preserving limiters.

More details on the tracer transport module can be found in the ICON reports
([Reinert 2020](../literature/literature.html#term-Reinert-2020), [Reinert & Zaengl 2021](../literature/literature.html#term-Reinert-Zaengl-2021)) and Section 3.6 of the [ICON Tutorial](../literature/literature.html#term-ICON-Tutorial).

## Physical Parameterizations[#](#physical-parameterizations)

### AES Physics Package[#](#aes-physics-package)

to be added

### NWP Physics Package[#](#nwp-physics-package)

Overview NWP physics package[#](#id1)

Parameterization

References

Namelist Parameter

Radiation

RRTM ([Mlawer et al. 1997](../literature/literature.html#term-Mlawer-et-al.-1997), [Barker et al. 2003](../literature/literature.html#term-Barker-et-al.-2003)), ecRad ([Hogan & Bozzo 2018](../literature/literature.html#term-Hogan-Bozzo-2018))

[inwp_radiation](#term-inwp_radiation)

Non-Orographic Gravity Wave Drag

[Orr et al. 2010](../literature/literature.html#term-Orr-et-al.-2010)

[inwp_gwd](#term-inwp_gwd)

Sub-grid scale Orographic Drag

[Lott & Miller 1997](../literature/literature.html#term-Lott-Miller-1997)

[inwp_sso](#term-inwp_sso)

Cloud Cover

-

[inwp_cldcover](#term-inwp_cldcover)

Microphysics

Single Moment ([Doms et al. 2011](../literature/literature.html#term-Doms-et-al.-2011)), Double Moment ([Seifert & Beheng 2006](../literature/literature.html#term-Seifert-Beheng-2006)), SBM ([Khain & Sednev 1996](../literature/literature.html#term-Khain-Sednev-1996), [Khain et al. 2004](../literature/literature.html#term-Khain-et-al.-2004))

[inwp_gscp](#term-inwp_gscp)

Convection

[Tiedtke 1989](../literature/literature.html#term-Tiedtke-1989), [Bechtold et al. 2008](../literature/literature.html#term-Bechtold-et-al.-2008)

[inwp_convection](#term-inwp_convection)

Turbulent Transfer

Prognostic TKE ([Raschendorfer 2001](../literature/literature.html#term-Raschendorfer-2001)), 3D Smagorinsky ([Smagorinsky 1963](../literature/literature.html#term-Smagorinsky-1963), [Lilly 1962](../literature/literature.html#term-Lilly-1962))

[inwp_turb](#term-inwp_turb)

Land

See [Land Parameterizations](../land/land.html#ref-land-schemes)

[inwp_surface](#term-inwp_surface)

More detailed descriptions of some of above options are available here:

[Radiation (ecRad)](ecrad/ecrad_overview.html#ref-atmosphere-ecrad)

[Reduced Radiation Grid](ecrad/ecrad_overview.html#ref-atmosphere-ecrad-redgrid)

[Aerosol Input Options](ecrad/ecrad_overview.html#ref-atmosphere-ecrad-aerosol)

[Cloud droplet number concentration (cdnc)](ecrad/ecrad_overview.html#ref-atmosphere-ecrad-cdnc)

[FSD Parameter](ecrad/ecrad_overview.html#ref-atmosphere-ecrad-fsd)

Microphysics

[Spectral Bin Microphysics (SBM)](sbm/sbm_overview.html#ref-sbm-overview)

[SBM implementation in ICON](sbm/sbm_overview.html#ref-sbm-implementation)

[Miscellaneous](miscellaneous/miscellaneous_nwp.html#ref-atm-nwpmisc)

[External SST/SIC](miscellaneous/miscellaneous_nwp.html#ref-sstsic-ext)

[2D Aerosol](miscellaneous/miscnwp_2daerosol.html#ref-miscnwp-2daero)

You can find a brief overview on the NWP physics package in chapter 3 of the [ICON Tutorial](../literature/literature.html#term-ICON-Tutorial).

Tuning ICON NWP Physics

A set of sensitive and important tuning parameters is provided in [this description](miscellaneous/tuning_nwp.html#ref-atmosphere-tuning).

### Glossary of Namelist Parameters[#](#glossary-of-namelist-parameters)

Operational NWP setting marked by

iforcing[#](#term-iforcing)

(&run_nml) Forcing of dynamics and transport by parameterized processes. 2: AES forcing, 3:

NWP forcing

ldeepatmo[#](#term-ldeepatmo)

(dynamics_nml) Switch for deep-atmosphere modification of non-hydrostatic atmosphere. Specific settings can be found in &upatmo_nml.

inwp_radiation[#](#term-inwp_radiation)

(&nwp_phy_nml) Radiation parameterization. 1: RRTM radiation, 4:

ecRad radiation

inwp_gwd[#](#term-inwp_gwd)

(&nwp_phy_nml) 1:

Orr et al. scheme

inwp_sso[#](#term-inwp_sso)

(&nwp_phy_nml) 1:

Lott-Miller scheme

inwp_cldcover[#](#term-inwp_cldcover)

(&nwp_phy_nml) 1:

Diagnostic PDF 5: All or nothing scheme (grid-scale clouds)

inwp_gscp[#](#term-inwp_gscp)

(&nwp_phy_nml) 1:

Single moment 2:

Single moment incl. graupel 4: Double moment 8: Spectral bin microphysics

inwp_convection[#](#term-inwp_convection)

(&nwp_phy_nml) 1:

Tiedtke-Bechtold

inwp_turb[#](#term-inwp_turb)

(&nwp_phy_nml) 1:

Prognostic TKE (COSMO) 5: 3D Smagorinsky diffusion

inwp_surface[#](#term-inwp_surface)

(&nwp_phy_nml) 1:

TERRA

On this page

so the DOM is not blocked -->