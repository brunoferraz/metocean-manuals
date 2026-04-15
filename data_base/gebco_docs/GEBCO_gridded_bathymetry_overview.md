# GEBCO Documentation

Source: https://www.gebco.net/data-products/gridded-bathymetry-data/

---

-

Gridded Bathymetry Data | GEBCO

[
Skip to main content
](#main-content)

# Gridded Bathymetry Data

## Global ocean & land terrain models

GEBCO’s current gridded bathymetric data set, the GEBCO_2025 Grid, is a global terrain model for ocean and land, providing elevation data, in meters, on a 15 arc-second interval grid. It is accompanied by a Type Identifier (TID) Grid that gives information on the types of source data that the GEBCO_2025 Grid is based.

This release includes a version of the grid with under-ice topography/bathymetry information for Greenland and Antarctica.
[Download global coverage grids](#global)
- [Download data for user-defined areas](#area)
- [Multi-resolution grid product](#multi)
- [Access the GEBCO grid via OPeNDAP](#opendap)

More [information](/data-products-gridded-bathymetry-data/gebco2025-grid) about the grid, its terms of use and attribution. [Provide feedback](https://www.gebco.net/data-products/gridded-bathymetry-data/feedback/), tell us how you are using the grid.

GEBCO releases a new global grid every year, generally in July. Find out more about the [grid generation process](/data-products/gridded-bathymetry-data/grid-development).

## Download global coverage grids

The GEBCO_2025 Grid and TID Grid can be download as global files in netCDF format or a set of 8 tiles (each with an area of 90° x 90°), giving global coverage, in Esri ASCII raster and data GeoTiff formats. The data filea are included in a zip file along with the data set documentation.

GEBCO_2025 Grid (ice surface elevation)[netCDF](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/ice_surface_elevation/netcdf/gebco_2025.zip?download=1) (4 Gbytes, 7.5 Gbytes uncompressed)[Data GeoTiff](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/ice_surface_elevation/geotiff/gebco_2025_geotiff.zip?download=1)[ ](https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024/geotiff/)(4 Gbytes, 8 Gbytes uncompressed)[Esri ASCII raster](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/ice_surface_elevation/esri_ascii_raster/gebco_2025_ascii.zip?download=1) (5 Gbytes, 20 Gbytes uncompressed)GEBCO_2025 Grid (sub-ice topo/bathy)[netCDF](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/sub_ice_topography_bathymetry/netcdf/gebco_2025_sub_ice_topo.zip?download=1)[ ](https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024_sub_ice_topo/zip/)(4 Gbytes, 7.5 Gbytes uncompressed)[Data GeoTiff](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/sub_ice_topography_bathymetry/geotiff/gebco_2025_sub_ice_topo_geotiff.zip?download=1)[ ](https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024_sub_ice_topo/geotiff/)(4 Gbytes, 8 Gbytes uncompressed)[Esri ASCII raster](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/sub_ice_topography_bathymetry/esri_ascii_raster/gebco_2025_sub_ice_topo_ascii.zip?download=1) (5 Gbytes, 20 Gbytes uncompressed)GEBCO_2025 TID Grid[netCDF](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/type_identifier_grid/netcdf/gebco_2025_tid.zip?download=1) (90 Mbytes, 4 Gbytes uncompressed)[Data GeoTiff](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/type_identifier_grid/geotiff/gebco_2025_tid_geotiff.zip?download=1) (96 Mbytes, 7 Gbytes uncompressed)[Esri ASCII raster](https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/type_identifier_grid/esri_ascii_raster/gebco_2025_tid_ascii.zip?download=1) (108 Mbytes, 9.5 Gbytes uncompressed)

Please note that the size of the uncompressed files.

## Download data for user-defined areas

Use our [application](https://download.gebco.net/) to select and download data in netCDF, Esri ASCII raster and data GeoTiff formats.

PLEASE NOTE: On the 16th March we have released a new GEBCO download application. Please provide any feedback at

[gdacc@seabed2030.org](mailto:gdacc@seab%65d2030.or%67)

[

Image:

](https://download.gebco.net)
## Multi-resolution grids

The global GEBCO grid is currently made available as a global 15 arc-second interval grid. However, in some regions, it is based on data at higher resolutions. To accommodate users who want access to higher resolution gridded bathymetry data, where it exists, a [test multi-resolution grid product](/data-products/gridded-bathymetry-data/multi-res) has been developed. This is now available through the new download application.

## Access the GEBCO grid via OPeNDAP

GEBCO’s gridded data sets are now available for [direct download](https://data.ceda.ac.uk/bodc/gebco/global/gebco_2025) from the Natural Environment Research Council's (NERC) Centre for Environmental Data Analysis (CEDA).

Through CEDA, GEBCO’s gridded data sets can also be accessed via [OPeNDAP](https://www.opendap.org/) – allowing direct access to the data sets through a number of applications.

To access the GEBCO_2025 Grid via OPeNDAP – navigate to the directory that contains the netCDF data file for the gridded data set that you are interested in, for example, the [ice surface elevation](https://data.ceda.ac.uk/bodc/gebco/global/gebco_2025/ice_surface_elevation/netcdf) version of the grid, and click on the ‘extract subset’ icon to access the OPeNDAP Dataset Access Form and data set URL. The image below illustrates this.

Image:

## Data set attribution for GEBCO_2025 Grid

If the data sets are used in a presentation or publication then we ask that you acknowledge the source. This should be of the form:

#### GEBCO Compilation Group (2025) GEBCO 2025 Grid (doi:10.5285/37c52e96-24ea-67ce-e063-7086abc05f29)

## Terms of use

The GEBCO Grid is placed in the public domain and may be used free of charge. Use of the GEBCO Grid indicates that the user accepts the [conditions of use and disclaimer information](https://www.gebco.net/data-products/gridded-bathymetry/terms-of-use).

## Data set errata and known issues

Although every care is taken during the development of the GEBCO bathymetric grids, errors can occasionally occur, and can be reported to the Seabed 2030 Global Centre (

[gdacc@seabed2030.org](mailto:gdac%63@s%65%61be%642030.o%72g)

). Known issues can be viewed on our [errata pages](/data-products/gridded-bathymetry-data/data-set-errata).

## Type Identifier (TID) Grid

The TID grid identifies the type of source data that the corresponding grid cells in the GEBCO Grid are based on. Further information about the TID codes can be found in the [accompanying documentation](/data-products-gridded-bathymetry-data/gebco2025-grid).

Find out more about the TID Grid from our StoryMap. [English](https://storymaps.arcgis.com/stories/115beb845eae4facb1047a5deb28f121), [Spanish](https://storymaps.arcgis.com/stories/ac6e968648224b019cf50dd9aedbd6dc) and [French](https://storymaps.arcgis.com/stories/51f9f91887bf466f8c416f7f48364970) language versions are available.

[

Image:

](https://storymaps.arcgis.com/stories/115beb845eae4facb1047a5deb28f121)[

Image:

](https://storymaps.arcgis.com/stories/ac6e968648224b019cf50dd9aedbd6dc)[

Image:

](https://storymaps.arcgis.com/stories/51f9f91887bf466f8c416f7f48364970)
## Note on vertical datum and GEBCO's grids

GEBCO's global elevation models are generated by the assimilation of heterogeneous data types assuming all of them to be referred to mean sea level. However, in some shallow water areas, the grids include data from sources having a vertical datum other than mean sea level. We are working to understand how best to fully assimilate these data.

## Provide feedback

To help us improve our products and services, use our form to [provide feedback](/data-products/gridded-bathymetry-data/feedback) on the GEBCO grid.

### Find out more

- [About the GEBCO_2025 Grid](/data-products-gridded-bathymetry-data/gebco2025-grid)
- [Data contributors](/about-us/acknowledgements/our-data-contributors)
- [Historical GEBCO data sets](https://www.gebco.net/data-products/historical-data-sets)
- [Improving GEBCO's grid in shallow water regions](https://www.gebco.net/data-products/gridded-bathymetry-data/shallow-water-bathymetry)
- [SRTM15_plus](https://topex.ucsd.edu/WWW_html/srtm15_plus.html)

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