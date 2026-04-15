# GEBCO Documentation

Source: https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2024-grid

---

-

The GEBCO_2024 Grid | GEBCO

[
Skip to main content
](#main-content)

# The GEBCO_2024 Grid

Image:

### Introduction

The GEBCO_2024 Grid is a global terrain model for ocean and land, providing elevation data, in meters, on a 15 arc-second interval grid of 43200 rows x 86400 columns, giving 3,732,480,000 data points. The data values are pixel-centre registered i.e. they refer to elevations, in meters, at the centre of grid cells.

The data are available to download according to the [Terms of Use](/data-products/gridded-bathymetry/terms-of-use).

The grid is accompanied by a Type Identifier (TID) Grid, giving information on the types of source data that the GEBCO_2024 Grid is based on.

The primary GEBCO_2024 grid contains land and ice surface elevation information. A version is also made available with under-ice topography/bathymetry information for Greenland and Antarctica.

The grid was published in July 2024 and is the sixth GEBCO grid developed through The Nippon Foundation-GEBCO [Seabed 2030 Project](https://seabed2030.org/). This is a collaborative project between the [Nippon Foundation](https://www.nippon-foundation.or.jp/en/) of Japan and [GEBCO](/about-us). The Seabed 2030 Project aims to bring together all available bathymetric data to produce the definitive map of the world ocean floor and make it available to all.

### Grid development

The GEBCO_2024 Grid is a continuous, global terrain model for ocean and land with a spatial resolution of 15 arc seconds. It uses as a ‘base’ version 2.6 of the [SRTM15+ data set](https://topex.ucsd.edu/WWW_html/srtm15_plus.html) between latitudes of 50° South and 60° North. This data set is a fusion of land topography with measured and estimated seafloor topography. This version of SRTM15+ is similar to version 2.1 [Tozer et al., 2019] but includes additional data sets. It uses predicted depths based on the V32 gravity model [Sandwell et al., 2019].

The SRTM15+ base grid has been augmented with the gridded bathymetric data sets developed by the four Seabed 2030 Regional Centers to produce the GEBCO_2024 Grid. The Regional Centers have compiled gridded bathymetric data sets, largely based on multibeam data, for their areas of responsibility. These regional grids were then provided to the Global Center. For areas outside of the polar regions (primarily south of 60°N and north of 50°S), these data sets are in the form of 'sparse grids', i.e. only grid cells that contain data were populated. For the polar regions, complete grids were provided due to the complexities of incorporating data held in polar coordinates.

The compilation of the GEBCO_2024 Grid from these regional data grids was carried out at the Global Centre, with the aim of producing a seamless global terrain model. For the 2020 and 2021 releases of the GEBCO grid, the data sets provided as sparse grids by the Regional Centers were included on to the base grid without any blending. This led to discontinuities at the boundary between the regional grids and the base grids in some areas, largely in regions where the base grid is not constrained by measured data, i.e. areas of large differences between the data sets.

For subsequent grid releases, the sparse regional grids have been included on to the base grid using a ‘remove-restore’ blending procedure (Smith and Sandwell, 1997; Becker, Sandwell and Smith, 2009 and Hell and Jakobsson, 2011). This is a two-stage process of computing the difference between the new data and the ‘base’ grid and then gridding the difference and adding the difference back to the existing ‘base’ grid. The aim is to achieve a smooth transition between the 'new' and 'base' data sets with the minimum of perturbation of the existing base data set. However, please note that there may be differences between the 2022 and 2021 grid in regions outside areas of measured data due to the grid merging process. For the polar data sets supplied in the form of complete grids these data sets were included using feather blending techniques from GlobalMapper software version 23.0.1 made available by Blue Marble Geographics. Some additional edits were made to the final grid to remove erroneous values identified in the previous grid and notified to the Global Centre.

The GEBCO_2024 Grid includes data sets from a number of international and national data repositories and regional mapping initiatives. Information on the data sets included in the grid is given in our [data contributors](/about-us/acknowledgements/our-data-contributors) list.

Please see the accompanying documentation for more information on the development of the grid.

Document:

[Documentation for the GEBCO_2024 Grid](/sites/default/files/documents/GEBCO_grid_2024.pdf)

### Ice-surface elevation and under-ice topography

The GEBCO_2024 grid is made available in two versions, containing:
land and ice surface elevation information
- under-ice topography information for Greenland and Antarctica

The information for ice-surface elevation and under-ice topography/bathymetry is taken from IceBridge BedMachine Greenland, Version 5 (Morlighem, M. et al. 2017) and data based on MEaSUREs BedMachine Antarctica, Version 2 (Morlighem, M. et al 2020).

### Land data

The land data in the GEBCO Grid are taken directly from SRTM15+ V2.6 data set for all areas outside the Polar regions – see the SRTM15_plus data set documentation for more information. South of 60°S, the land/ ice-surface elevation topography is largely determined from MEaSUREs BedMachine Antarctica, Version 2 (Morlighem, M. et al 2020). For areas north of 60°N, land data are largely taken from the Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010) data set (Danielson, J.J., and Gesch, D.B., 2011). For the Svalbard region, land data are taken from Terrengmodell Svalbard (S0 Terrengmodell), Norwegian Polar Institute (2014).

### GEBCO Type Identifier (TID) Grid

The GEBCO Grid is accompanied by a Type Identifier (TID) grid. This data set identifies the type of source data that the corresponding grid cells in the GEBCO Grid are based on. Further information about the format and coding of the TID grid is given below.

TIDDefinition0LandDirect measurements10Singlebeam - depth value collected by a single beam echo-sounder11Multibeam - depth value collected by a multibeam echo-sounder12Seismic - depth value collected by seismic methods13Isolated sounding - depth value that is not part of a regular survey or trackline14ENC sounding - depth value extracted from an Electronic Navigation Chart (ENC)15Lidar - depth derived from a bathymetric lidar sensor16Depth measured by optical light sensor17Combination of direct measurement methodsIndirect measurements40Predicted based on satellite-derived gravity data - depth value is an interpolated value guided by satellite-derived gravity data41Interpolated based on a computer algorithm - depth value is an interpolated value based on a computer algorithm (e.g. Generic Mapping Tools)42Digital bathymetric contours from charts - depth value taken from a bathymetric contour data set43Digital bathymetric contours from ENCs - depth value taken from bathymetric contours from an Electronic Navigation Chart (ENC)44Bathymetric sounding - depth value at this location is constrained by bathymetric sounding(s) within a gridded data set where interpolation between sounding points is guided by satellite-derived gravity data45Predicted based on helicopter/flight-derived gravity data46Depth estimated by calculating the draft of a grounded iceberg using satellite-derived freeboard measurement.Unknown70Pre-generated grid - depth value is taken from a pre-generated grid that is based on mixed source data types, e.g. single beam, multibeam, interpolation etc.71Unknown source - depth value from an unknown source72Steering points - depth value used to constrain the grid in areas of poor data coverage
### GEBCO Grid, vertical and horizontal datum

The complete GEBCO_2024 data set provides global coverage, spanning 89° 59' 52.5''N, 179° 59' 52.5''W to 89° 59' 52.5''S, 179° 59' 52.5''E on a 15 arc-second geographic latitude and longitude grid. It consists of 43200 rows x 86400 columns, giving 3,732,480,000 data points. The data values are pixel-centre registered i.e. they refer to elevations, in meters, at the centre of grid cells.

The GEBCO grid can be assumed to be relative to WGS84.

GEBCO's global elevation models are generated by the assimilation of heterogeneous data types, assuming all of them to be referred to Mean Sea Level. However, in some shallow water areas, the grids include data from sources having a vertical datum other than mean sea level.

### Data Dissemination

CF-compliant NetCDF format

The GEBCO_2024 NetCDF files are provided in NetCDF 4 format and conform to the NetCDF Climate and Forecast (CF) Metadata Convention v1.6 ([http://cfconventions.org/](http://cfconventions.org/)).

Within the NetCDF files, the GEBCO_2024 gridded data are stored as a two-dimensional array of 2-byte integer values of elevation in metres, with negative values for bathymetric depths and positive values for topographic heights. The GEBCO_2024 TID grid is provided in the NetCDF format, but data are stored as a two-dimensional array of single byte integers.

- The global dataset is provided as a single 7.5 GB file
- The global TID grid is provided as a single 4 GB file
### Data set attribution

If the data sets are used in a presentation or publication then we ask that you acknowledge the source. This should be of the form:

GEBCO Compilation Group (2024) GEBCO 2024 Grid (doi:10.5285/1c44ce99-0a0d-5f4f-e063-7086abc0ea0f)

### Terms of use and disclaimer

Scope

- These terms of use apply to The GEBCO Grid and other GEBCO-derived information products
- For brevity ‘The GEBCO Grid’ is used throughout and should be interpreted as meaning The GEBCO Grid and other GEBCO-derived information products
- Bathymetric Data refers to measurements made by various instruments of the ocean depth, associated ocean properties and the supporting metadata
- Information products are the result of applying algorithms, mathematical techniques, scientific theory and Intellectual Property to data to create useful, derived values
- As the GEBCO Grid is created by interpolating, applying algorithms and mathematical techniques to bathymetric data, GEBCO considers the GEBCO Grid to be an information product
- GEBCO does not provide the underlying source bathymetric data when distributing the GEBCO Grid

Terms of use

The GEBCO Grid is placed in the public domain and may be used free of charge.

Use of the GEBCO Grid indicates that the user accepts the conditions of use and disclaimer information given below.

Users are free to:

- Copy, publish, distribute and transmit The GEBCO Grid
- Adapt The GEBCO Grid
- Commercially exploit The GEBCO Grid, by, for example, combining it with other information, or by including it in their own product or application

Users must:

- Acknowledge the source of The GEBCO Grid. A suitable form of attribution is given in the documentation that accompanies The GEBCO Grid.
- Not use The GEBCO Grid in a way that suggests any official status or that GEBCO, or the IHO or IOC, endorses any particular application of The GEBCO Grid.
- Not mislead others or misrepresent The GEBCO Grid or its source.

Disclaimer

- The GEBCO Grid should NOT be used for navigation or for any other purpose involving safety at sea.
- The GEBCO Grid is made available 'as is'. While every effort has been made to ensure reliability within the limits of present knowledge, the accuracy and completeness of The GEBCO Grid cannot be guaranteed. No responsibility can be accepted by GEBCO, IHO, IOC, or those involved in its creation or publication for any consequential loss, injury or damage arising from its use or for determining the fitness of The GEBCO Grid for any particular use.
- The GEBCO Grid is based on bathymetric data from many different sources of varying quality and coverage.
- As The GEBCO Grid is an information product created by interpolation of measured data, the resolution of The GEBCO Grid may be significantly different to that of the resolution of the underlying measured data.
### Reporting bugs in the GEBCO Grid

While every effort is made to produce an error- free grid, some artefacts may still appear in the data set. Please see our [errata page](/data-products/gridded-bathymetry-data/data-set-errata) for information on known bugs in the dataset.

If you find any anomalies in the grid then please report them via email (

[gdacc@seabed2030.org](mailto:gda%63c@s%65abed203%30.o%72%67)

), giving the problem location, and we will investigate.

### References

Danielson, J.J., and Gesch, D.B., 2011, Global multi-resolution terrain elevation data 2010 (GMTED2010): U.S. Geological Survey Open-File Report 2011–1073, 26 p.

Hell, B and M Jakobsson (2011), Gridding heterogeneous bathymetric data sets with stacked continuous curvature splines in tension, Mar. Geophys. Res., 32(4), 493-501, doi:10.1007/s11001-011-9141-1.

Harper, Hugh & Sandwell, David. (2024). Global Predicted Bathymetry Using Neural Networks. Earth and Space Science. 11. 10.1029/2023EA003199.

Morlighem, M., C. Williams, E. Rignot, L. An, J. E. Arndt, J. Bamber, G. Catania, N. Chauché, J. A. Dowdeswell, B. Dorschel, I. Fenty, K. Hogan, I. Howat, A. Hubbard, M. Jakobsson, T. M. Jordan, K. K. Kjeldsen, R. Millan, L. Mayer, J. Mouginot, B. Noël, C. O'Cofaigh, S. J. Palmer, S. Rysgaard, H. Seroussi, M. J. Siegert, P. Slabon, F. Straneo, M. R. van den Broeke, W. Weinrebe, M. Wood, and K. Zinglersen. 2017. BedMachine v3: Complete bed topography and ocean bathymetry mapping of Greenland from multi-beam echo sounding combined with mass conservation, Geophysical Research Letters. 44. . [https://doi.org/10.1002/2017GL074954](https://doi.org/10.1002/2017GL074954)

Morlighem, M., E. Rignot, T. Binder, D. D. Blankenship, R. Drews, G. Eagles, O. Eisen, F. Ferraccioli, R. Forsberg, P. Fretwell, V. Goel, J. S. Greenbaum, H. Gudmundsson, J. Guo, V. Helm, C. Hofstede, I. Howat, A. Humbert, W. Jokat, N. B. Karlsson, W. Lee, K. Matsuoka, R. Millan, J. Mouginot, J. Paden, F. Pattyn, J. L. Roberts, S. Rosier, A. Ruppel, H. Seroussi, E. C. Smith, D. Steinhage, B. Sun, M. R. van den Broeke, T. van Ommen, M. van Wessem, and D. A. Young. 2020. Deep glacial troughs and stabilizing ridges unveiled beneath the margins of the Antarctic ice sheet, Nature Geoscience. 13. 132-137. [https://doi.org/10.1038/s41561-019-0510-8](https://doi.org/10.1038/s41561-019-0510-8)

Norwegian Polar Institute (2014). Terrengmodell Svalbard (S0 Terrengmodell) [Data set]. Norwegian Polar Institute. [https://doi.org/10.21334/npolar.2014.dce53a47](https://doi.org/10.21334/npolar.2014.dce53a47)

Sandwell, D.T., Harper, H., Tozer, B. and Smith, W.H., 2019. Gravity field recovery from geodetic altimeter missions. Advances in Space Research.

Smith, W H F and D T Sandwell (1997). Global seafloor topography from satellite altimetry and ship depth soundings, Science, v. 277, p. 1957-1962, 26 Sept.

Tozer, B, Sandwell, D. T., Smith, W. H. F., Olson, C., Beale, J. R., & Wessel, P. (2019). Global bathymetry and topography at 15 arc sec: SRTM15+. Earth and Space Science. 6. [https://doi.org/10.1029/2019EA000658](https://doi.org/10.1029/2019EA000658).

-
[Home](/)

-
[Data & Products](/data-products)

[Gridded Bathymetry Data](/data-products/gridded-bathymetry-data)

[Regional grid - Arctic Ocean (IBCAO)](/data-products/gridded-bathymetry-data/arctic-ocean)

-
[Regional grid - Southern Ocean (IBCSO)](/data-products/gridded-bathymetry-data/southern-ocean)

-
[Errata and known issues](/data-products/gridded-bathymetry-data/data-set-errata)

-
[GEBCO_2025 Grid](/data-products-gridded-bathymetry-data/gebco2025-grid)

-
[GEBCO_2024 Grid](/data-products-gridded-bathymetry-data/gebco2024-grid)

-
[GEBCO_2023 Grid](/data-products/gridded-bathymetry-data/gebco2023-grid)

-
[GEBCO_2022 Grid](/data-products/gridded-bathymetry-data/gebco-2022)

-
[GEBCO_2021 Grid](/data-products/gridded-bathymetry-data/gebco-2021)

-
[GEBCO_2020 Grid](/data-products/gridded-bathymetry-data/gebco-2020)

-
[GEBCO_2019 Grid](/data-products/gridded-bathymetry-data/gebco-2019)

-
[Undersea Feature Names](/data-products/undersea-feature-names)

-
[GEBCO Web Services](/data-products/gebco-web-services)

[Web Map Service](/data-products/gebco-web-services/web-map-service)

-
[Previous GEBCO WMS](/data-products/gebco-web-services/previous-wms)

-
[Printable Maps](/data-products/printable-maps)

-
[IHO-IOC GEBCO Cook Book](/data-products/gebco-cook-book)

-
[Historical GEBCO Charts](/data-products/historical-gebco-charts)

-
[Historical Data Sets](/data-products/historical-data-sets)

-
[Imagery](/data-products/imagery)

-
[History of GEBCO](/data-products/history-gebco)

-
[GEBCO Digital Atlas](/data-products/gebco-digital-atlas)

-
[Seabed 2030](https://seabed2030.org)

-
[Training](/training)

-
[News & Media](/news)

-
[About](/about-us)

[Overview](/about-us/overview)

-
[GEBCO Strategy](/about-us/gebco-strategy)

-
[Project History](/about-us/project-history)

-
[Seabed 2030](/about-us/seabed2030-project)

-
[Acknowledgements](/about-us/acknowledgements)

[Our Data Contributors](/about-us/acknowledgements/our-data-contributors)

-
[Working With Industry](/about-us/acknowledgements/working-with-industry)

-
[Contributing Data](/about-us/contributing-data)

-
[Presentations and Publications](/about-us/presentations-publications)

-
[Committees and Groups](/about-us/committees-groups)

[Guiding Committee](/about-us/committees-groups/guiding-committee)

-
[Regional Mapping](/about-us/committees-groups/scrum)

[Mapping projects](/about/committees-and-groups/scrum/mapping-projects)

-
[Undersea Features Names](/about-us/committees-groups/scufn)

-
[Technical Mapping](/about-us/committees-groups/tscom)

-
[Communication and Outreach](/about-us/committees-groups/scope)

-
[Meetings and Minutes](/about-us/meetings-minutes)

-
[GEBCO Symposium](/about-us/gebco-symposium)

-
[Frequently Asked Questions](/about-us/faq)

-
[Useful links](/about-us/links)

-
[Contact](/contact)