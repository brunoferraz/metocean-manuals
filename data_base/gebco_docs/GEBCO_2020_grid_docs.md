# GEBCO Documentation

Source: https://www.gebco.net/data-products/gridded-bathymetry-data/gebco-2020

---

-

GEBCO_2020 Grid | GEBCO

[
Skip to main content
](#main-content)

# GEBCO_2020 Grid

#### 1.0 Introduction

The GEBCO_2020 Grid was released in May 2020 and is the second global bathymetric product released by the General Bathymetric Chart of the Oceans (GEBCO) and has been developed through the Nippon Foundation-GEBCO [Seabed 2030 Project](https://seabed2030.org).

Please note that the lastest GEBCO grid release is available [here](https://www.gebco.net/data-products/gridded-bathymetry-data).

The GEBCO_2020 Grid provides global coverage of elevation data in meters on a 15 arc-second grid of 43200 rows x 86400 columns, giving 3,732,480,000 data points.

The data are available to download according to the Terms of Use provided in [Section 8](#section8) below, via several routes including: single-click download of the entire grid, selection of subsets and creation of output in alternative data formats [as detailed below.](#formats)

#### 2.0 Grid Development

The GEBCO_2020 Grid is a continuous, global terrain model for ocean and land with a spatial resolution of 15 arc seconds. The grid uses as a ‘base’ Version 2 of the SRTM15+ data set ([Tozer et al, 2019](#ref)). This data set is a fusion of land topography with measured and estimated seafloor topography. It is augmented with the gridded bathymetric data sets developed by the four Seabed 2030 Regional Centers. The Regional Centers have compiled gridded bathymetric data sets, largely based on multibeam data, for their areas of responsibility. These regional grids were then provided to the Global Center.

For areas outside of the polar regions (primarily south of 60°N and north of 50°S), these data sets are in the form of 'sparse grids', i.e. only grid cells that contain data were populated. For the polar regions, complete grids were provided due to the complexities of incorporating data held in polar coordinates.

The compilation of the GEBCO_2020 Grid from these regional data grids was carried out at the Global Center, with the aim of producing a seamless global terrain model.

In contrast to the development of the previous GEBCO grid, GEBCO_2019, the data sets provided as sparse grids by the Regional Centers were included on to the base grid without any blending, i.e. grid cells in the base grid were replaced with data from the sparse grids. This was with aim of avoiding creating edge effects, 'ridges and ripples', at the boundaries between the sparse grids and base grid during the blending process used previously. In addition, this allows a clear identification of the data source within the grid, with no cells being 'blended' values. Routines from Generic Mapping Tools ([GMT](http://gmt.soest.hawaii.edu/home)) system were used to do the merging of the data sets.

For the polar data sets, and the adjoining North Sea area, supplied in the form of complete grids these data sets were included using feather blending techniques from GlobalMapper software version 11.0, made available by [Blue Marble Geographic](https://www.bluemarblegeo.com/products/global-mapper.php).

The GEBCO_2020 Grid includes data sets from a number of international and national data repositories and regional mapping initiatives. For information on the data sets included in the GEBCO_2020 Grid, please see the list of [contributions included in this release of the grid](#compilations).

#### 3.0 Land Data

The land data in the GEBCO Grid are taken directly from SRTM15+ V2 for all areas outside the Polar regions.

South of 60°S, the land topography is determined largely from Bedmap2 (Fretwell et al, 2013).

For areas north of 60°N, land data are taken from the Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010) data set.

#### 4.0 GEBCO Type Identifier (TID) Grid

The GEBCO Grid is accompanied by a Type Identifier (TID) grid. This data set identifies the type of source data that the corresponding grid cells in the GEBCO Grid are based on. Further information about the format and coding of the TID grid is given below.

#### 4.1 GEBCO TID Grid coding

The table below details the coding of the GEBCO_2020 Type Identifier (TID) grid.

TID Definition 0 Land Direct measurements 10 Singlebeam - depth value collected by a single beam echo-sounder 11 Multibeam - depth value collected by a multibeam echo-sounder 12 Seismic - depth value collected by seismic methods 13 Isolated sounding - depth value that is not part of a regular survey or trackline 14 ENC sounding - depth value extracted from an Electronic Navigation Chart (ENC) 15 Lidar - depth derived from a bathymetric lidar sensor 16 Depth measured by optical light sensor 17 Combination of direct measurement methods Indirect measurements 40 Predicted based on satellite-derived gravity data - depth value is an interpolated value guided by satellite-derived gravity data 41 Interpolated based on a computer algorithm - depth value is an interpolated value based on a computer algorithm (e.g. Generic Mapping Tools) 42 Digital bathymetric contours from charts - depth value taken from a bathymetric contour data set 43 Digital bathymetric contours from ENCs - depth value taken from bathymetric contours from an Electronic Navigation Chart (ENC) 44 Bathymetric sounding - depth value at this location is constrained by bathymetric sounding(s) within a gridded data set where interpolation between sounding points is guided by satellite-derived gravity data 45 Predicted based on helicopter/flight-derived gravity data Unknown 70 Pre-generated grid - depth value is taken from a pre-generated grid that is based on mixed source data types, e.g. single beam, multibeam, interpolation etc. 71 Unknown source - depth value from an unknown source 72 Steering points - depth value used to constrain the grid in areas of poor data coverage
#### 5. GEBCO Grid, vertical and horizontal datum

The complete GEBCO_2020 data set provides global coverage, spanning 89° 59' 52.5''N, 179° 59' 52.5''W to 89°: 59' 52.5''S, 179° 59' 52.5''E on a 15 arc-second geographic latitude and longitude grid.It consists of 43200 rows x 86400 columns, giving 3,732,480,000 data points. The data values are pixel-centre registered i.e. they refer to elevations, in meters, at the centre of grid cells.

The GEBCO grid can be assumed to be relative to WGS84.

GEBCO's global elevation models are generated by the assimilation of heterogeneous data types, assuming all of them to be referred to Mean Sea Level. However, in some shallow water areas, the grids include data from sources having a vertical datum other than mean sea level.

#### 6. Data Dissemination

GEBCO's gridded data sets are made available in a number of different formats as described in the following sections.

Global gridded data are available in each format as a [‘one-click’ download](https://www.gebco.net/data-products/gridded-bathymetry-data) option.

User defined subsets can also be downloaded in the user selected format using the [download tool](https://download.gebco.net/).

### 6.1 CF-compliant NetCDF format

NetCDF (Network Common Data Form) is a self-describing, platform independent data format.The GEBCO_2020 NetCDF files are provided in NetCDF 4 format.

The GEBCO_2020 data files conform to the NetCDF Climate and Forecast (CF) Metadata Convention v1.6 ([http://cfconventions.org/](http://cfconventions.org)).

Within the NetCDF files, the GEBCO_2020 gridded data are stored as a two-dimensional array of 2-byte integer values of elevation in metres, with negative values for bathymetric depths and positive values for topographic heights. The GEBCO_2020 TID grid is provided in the NetCDF format, but data are stored as a two-dimensional array of single byte integers.
The global dataset is provided as a single 7.5 GB file
- The global TID grid is provided as a single 4 GB file
### 6.2 Esri ASCII raster format

This is an ASCII format developed for the export/exchange of Esri ARC/INFO rasters. The format consists of a header that gives the geographic extent and grid interval of the data set, followed by the actual grid cell data values.The GEBCO_2020 Grid and TID grids are made available as single-channel integer data values:

- The global data set is provided as a single compressed data file containing a set of 8 tiles (each with an area of 90° x 90°)
- The global TID grid is provided as a single compressed data file containing a set of 8 tiles (each with an area of 90° x 90°)

The data are available to access through the [download tool](https://download.gebco.net/).

### 6.3 Data GeoTIFF

The GeoTiff format contains geo-referencing (geographic extent and projection) information embedded within a Tiff file. The GEBCO_2020 Grid and TID grids are made available as single-channel integer data values for user-defined areas in GeoTiff format

- The global data set is provided as a single zip compressed data file containing a set of 8 tiles (each with an area of 90° x 90°)
- .The global TID grid is provided as a single zip compressed data file containing a set of 8 tiles (each with an area of 90° x 90°)The data are available to access through the [download tool](https://download.gebco.net/).
#### 7.0 Data set attribution

If the data sets are used in a presentation or publication then we ask that you acknowledge the source. This should be of the form:

GEBCO Compilation Group (2020) GEBCO 2020 Grid (doi:10.5285/a29c5465-b138-234d-e053-6c86abc040b9)

#### 8.0 Terms of use and disclaimer

### Scope

- These terms of use apply to The GEBCO Grid and other GEBCO-derived information products
- For brevity ‘The GEBCO Grid’ is used throughout and should be interpreted as meaning The GEBCO Grid and other GEBCO-derived information products
- Bathymetric Data refers to measurements made by various instruments of the ocean depth, associated ocean properties and the supporting metadata
- Information products are the result of applying algorithms, mathematical techniques, scientific theory and Intellectual Property to data to create useful, derived values.
- As the GEBCO Grid is created by interpolating, applying algorithms and mathematical techniques to bathymetric data, GEBCO considers the GEBCO Grid to be an information product
- GEBCO does not provide the underlying source bathymetric data when distributing the GEBCO Grid
### Terms of use

The GEBCO Grid is placed in the public domain and may be used free of charge.

Use of the GEBCO Grid indicates that the user accepts the conditions of use and disclaimer information given below.

### Users are free to:

- Copy, publish, distribute and transmit The GEBCO Grid
- Adapt The GEBCO Grid
- Commercially exploit The GEBCO Grid, by, for example, combining it with other information, or by including it in their own product or application
### Users must:

- Acknowledge the source of The GEBCO Grid. A suitable form of attribution is given in the documentation that accompanies The GEBCO Grid.
- Not use The GEBCO Grid in a way that suggests any official status or that GEBCO, or the IHO or IOC, endorses any particular application of The GEBCO Grid.
- Not mislead others or misrepresent The GEBCO Grid or its source.
### Disclaimer

- The GEBCO Grid should NOT be used for navigation or for any other purpose involving safety at sea.
- The GEBCO Grid is made available 'as is'. While every effort has been made to ensure reliability within the limits of present knowledge, the accuracy and completeness of The GEBCO Grid cannot be guaranteed. No responsibility can be accepted by GEBCO, IHO, IOC, or those involved in its creation or publication for any consequential loss, injury or damage arising from its use or for determining the fitness of The GEBCO Grid for any particular use.
- The GEBCO Grid is based on bathymetric data from many different sources of varying quality and coverage.
- As The GEBCO Grid is an information product created by interpolation of measured data, the resolution of The GEBCO Grid may be significantly different to that of the resolution of the underlying measured data.
#### 9.0 Reporting bugs in the GEBCO Grid

While every effort is made to produce an error free grid, some artefacts may still appear in the data set. Please see our [errata web page](https://www.gebco.net/data-products/gridded-bathymetry-data/data-set-errata) for information on known bugs in the dataset.

If you find any anomalies in the grid then please report them via email (

[gdacc@seabed2030.org](mailto:g%64a%63c@seabed2030.org)

), giving the problem location, and we will investigate.

#### 10. Data sets included in the GEBCO_2020 Grid

#### Compilations and gridded contributions

Contributing Project/Organization Regional Data Set (including reference/link where available) Alaska Fisheries Science Center of the US National Oceanic and Atmospheric Administration's National Marine Fisheries Service (NOAA Alaskan Fisheries)Bathymetry data from the Alaska bathymetry compilations for the Aleutian Islands, central Gulf of Alaska and Norton Sound. [https://www.afsc.noaa.gov/RACE/groundfish/Bathymetry/default.htm](https://www.afsc.noaa.gov/RACE/groundfish/Bathymetry/default.htm) Digitized chart soundings, Alaska:Proofed digitized historical chart soundings from “smooth sheets” covering Alaskan waters Proofed digitized historical chart soundings from “smooth sheets” covering Alaskan waters. Zimmermann, M., Prescott, M. M. & Haeussler, P. J. Bathymetry and Geomorphology of Shelikof Strait and the Western Gulf of Alaska. Geosciences 9, 409, doi:doi:10.3390/geosciences9100409 (2019).Prescott, M. M. & Zimmermann, M. Smooth sheet bathymetry of Norton Sound. Report No. Memo. NMFS-AFSC-298, 23 (U.S. Department of Commerce, 2015).Zimmermann, M. & Prescott, M. M. Smooth sheet bathymetry of Cook Inlet, Alaska. Report No. Memo. NMFS-AFSC-275, 32 (U.S. Department of Commerce, 2014).Zimmermann, M., Prescott, M. M. & Rooper, C. N. Smooth sheet bathymetry of the Aleutian Islands. Report No. Memo. NMFS-AFSC-250, 43 (U.S. Department of Commerce, 2013). British Antarctic Survey (BAS) Land elevation data and terrain models for areas in the Southern Ocean: South Georgia and South Sandwich Islands: From the South Georgia GIS [https://www.sggis.gov.gs/](https://www.sggis.gov.gs/) Marion Island: digitized from Very High Resolution (VHR) satellite imagery Balleney Island: digitized from Landsat imagery Bouvet and Peter Island: Norwegian Polar Institute (2014). Kartdata Bouvetøya 1:20 000 (B20 Kartdata); Norwegian Polar Institute (2014). Map data / kartdata Peter I Øy 1:50 000 (P50 Kartdata) British Oceanographic Data Centre (BODC) Gridded bathymetry data based on multibeam Data from RRS Charles Darwin cruise CD118 in the Northeast Atlantic off the UK. Bureau of Ocean Energy Management (BOEM)Northern Gulf of Mexico Deepwater Bathymetry Grid from 3D Seismic[https://www.boem.gov/Gulf-of-Mexico-Deepwater-Bathymetry/](https://www.boem.gov/Gulf-of-Mexico-Deepwater-Bathymetry/) Canadian Hydrographic ServiceNon-Navigational (NONNA-100) Bathymetric Data: represent all currently validated, digital bathymetric sources acquired by CHS, combined at a resolution of approximately 100 metres. Contains information licensed under the Open Government Licence – Canada.[https://open.canada.ca/data/en/dataset/d3881c4c-650d-4070-bf9b-1e00aabf0a1d](https://open.canada.ca/data/en/dataset/d3881c4c-650d-4070-bf9b-1e00aabf0a1d) Directorate of Navigation and Hydrography Brazil Digital Terrain Model of the Brazilian Continental Margin: Based on mixed data sources, provided by the Brazilian Navy at 1km resolution. Directorate of Navigation and Hydrography Brazil Bathymetric grid based on multibeam data. Data contributed by the Brazilian Navy in support of naming seafloor features (SCUFN 32), in the South Atlantic Ocean.Deakin University, AustraliaSeafloor mapping data, Victoria – 10m gridCollation of seafloor structure information (bathymetry and softness hardness) collected using multibeam sonar systems as part of the Victorian Marine Habitat Mapping Project and bathymetric light detection and ranging data (LiDAR) collected as part of the future coats program. The geographic is Victorian State waters.[http://dro.deakin.edu.au/view/DU:30043228](http://dro.deakin.edu.au/view/DU:30043228) Deep Reef Explorer ([www.deepreef.org](http://www.deepreef.org))High-resolution depth model for the Great Barrier Reef – 30Beaman, R J (2018). High-resolution depth model for the Great Barrier Reef - 30 m. Geoscience Australia, Canberra, Australia.[http://pid.geoscience.gov.au/dataset/115066](http://pid.geoscience.gov.au/dataset/115066)Deep Reef Explorer ([www.deepreef.org](http://www.deepreef.org))High-resolution depth model for the Northern Australia – 100m, V3Beaman, R J (2010). Project 3D-GBR: A high-resolution depth model for the Great Barrier Reef and Coral Sea. Marine and Tropical Sciences Research Facility (MTSRF) Project 2.5i.1a Final Report, MTSRF, Cairns, Australia, pp. 13 plus Appendix 1 (Internal Report).[https://www.deepreef.org/bathymetry/65-3dgbr-bathy.html](https://www.deepreef.org/bathymetry/65-3dgbr-bathy.html)EMODnetThe EMODnet Digital Bathymetry (DTM) 2018. A multilayer bathymetric product for Europe’s sea basins, based upon more than 9400 bathymetric survey data sets and Composite DTMs gathered from 49 data providers from 24 countries.EMODnet Bathymetry Consortium (2018): EMODnet Digital Bathymetry (DTM): [http://doi.org/10.12770/18ff0d48-b203-4a65-94a9-5fd8b0ec35f6](http://doi.org/10.12770/18ff0d48-b203-4a65-94a9-5fd8b0ec35f6)Geological Survey of IsraelBathymetric grids for the Black and Caspian SeasHall, J K (2002). Bathymetric compilations of the seas around Israel I: The Caspian and Black Seas. Geological Survey of Israel, Current Research, Vol. 13, December 2002.GeomarBathymetric grid for part of the Red Sea region and the South East Pacific region:[https://doi.org/10.1594/PANGAEA.860374](https://doi.org/10.1594/PANGAEA.860374) and [https://doi.org/10.1594/PANGAEA.785515](https://doi.org/10.1594/PANGAEA.785515)Geoscience AustraliaHigh-resolution depth model for Northern Australia - 30 m (2018)

[https://ecat.ga.gov.au/geonetwork/srv/eng/catalog.search#/metadata/121620](https://ecat.ga.gov.au/geonetwork/srv/eng/catalog.search#/metadata/121620)
Geoscience Australia 50m Multibeam Dataset of Australia 2012 Wilson, O, C Buchanan and M Spinoccia (2012). 50m Multibeam Dataset of Australia 2012 [https://ecat.ga.gov.au/geonetwork/srv/eng/catalog.search#/metadata/73842](https://ecat.ga.gov.au/geonetwork/srv/eng/catalog.search#/metadata/73842)Geoscience AustraliaAustralian Bathymetry and Topography Grid, June 2009ANZLIC unique identifier: ANZCW0703013116, Geoscience Australia.Whiteway, T, (2009). Australian Bathymetry and Topography Grid, June 2009. Scale 1:5000000. Geoscience Australia, Canberra. [http://dx.doi.org/10.4225/25/53D99B6581B9A](http://dx.doi.org/10.4225/25/53D99B6581B9A).Geoscience AustraliaMH370 - Phase One Data Release[http://marine.projects.ga.gov.au/mh370-phase-one-data-release.html](http://marine.projects.ga.gov.au/mh370-phase-one-data-release.html)Goodliffe, A.Woodlark Basin multibeam bathymetry grid – 200mGoodliffe, A. (2011). Woodlark Basin multibeam bathymetry grid. Interdisciplinary Earth Data Alliance (IEDA). doi:10.1594/IEDA/100015Global Multi-resolution Topography Data Synthesis (GMRT)GMRT versions 3.5 and 3.7 A multi-resolutional compilation of multibeam sonar data collected by scientists and institutions worldwide, that is edited, processed and gridded by the GMRT Team. This global multibeam compilation is merged into a continuously updated compilation of global elevation data. The GMRT multibeam compilation was provided to GEBCO at 15 arc sec resolution. The full list of contributing cruises, vessels and Chief Scientists is available [here](https://www.gmrt.org/contributors/cruises.php).[https://www.gmrt.org/](https://www.gmrt.org/)Global Sea Mineral Resources NV (GSR), DEME Group, BelgiumBathymetric grid, based on multibeam dataSupplied to GEBCO for a region of the North Pacific, 1800 km southwest of the Mexican Baja Peninsula.Hydrographic Service of the Royal Netherlands NavyGridded bathymetric data set for the Windward Island area of the Caribbean SeaThe dataset is based on mixed data sources. Hydrographic Service for the Navy, Ministry of the Defence of Argentina Bathymetric grids based on data acquired during cruises: ARG-MD_2007 (2007), HES-2008-COOPERACION (2008), HE-2016 (2016) and the recovery of the A.R.A SAN JUAN submarine (2017)Henstock, T.J. et alGridded bathymetric data set based on multibeam data from HMS Scott cruise HI1123Seafloor morphology of the Sumatran subduction zone: Surfacerupture during megathrust earthquakes? Geology, v34, pp485-488, 2006 International Bathymetric Chart of the Arctic Ocean (IBCAO)IBCAO V4 bathymetric gridIBCAO v4 bathymetric grid, 180°W-180°E; 64°N-90°N[doi:10.5285/a01d292f-b4a0-1ef7-e053-6c86abc0a4b2](https://www.gebco.net/10.5285/a01d292f-b4a0-1ef7-e053-6c86abc0a4b2)Access a

Document:

[ibcao_v4_data_sets.pdf](/sites/default/files/documents/ibcao_v4_data_sets.pdf)

included in the grid.International Bathymetric Chart of the Southern Ocean (IBCSO)IBCSO v1 bathymetric grid, 180°W-180°E; 60S-90°S:The grid for the Southern Ocean area is based on the IBCSO V1 data base as documented in the source id list: [https://www.scar.org/science/ibcso/resources/](https://www.scar.org/science/ibcso/resources/)Arndt, J E, H W Schenke, M Jakobsson, F Nitsche, G Buys, B Goleby, M Rebesco, F Bohoyo, J K Hong, J Black, R Greku, G Udintsev, F Barrios, W Reynoso-Peralta, T Morishita and R Wigley (2013). The International Bathymetric Chart of the Southern Ocean (IBCSO) Version 1.0 - A new bathymetric compilation covering circum-Antarctic waters. Geophysical Research Letters, [doi: 10.1002/grl.50413](https://doi.org/10.1002/grl.50413) Japan Coast Guard, Hydrographic and Oceanographic Department (JHOD); Japan Oceanographic Data Center (JODC) of the Japan Coast Guard Japan Coast Guard Grid for the North Western Pacific Ocean Provided at 30 arc-second intervals, the grid for this area was originally developed from the following source data: Multibeam data from the Japan Coast Guard, A pre-prepared 500m interval grid based on measured sounding data: J-EGG500 grid JODC-Expert Grid data for Geographic -500m [www.jodc.go.jp/data_set/jodc/jegg_intro.html](http://www.jodc.go.jp/data_set/jodc/jegg_intro.html) Land Information New Zealand (LINZ)Multibeam data used to compile New Zealand navigation chartsWater around New Zealand. Marine Geoscience Data System (MGDS), Hosted at Lamont-Doherty Earth Observatory of Columbia University.Gridded multibeam data Data from 6 cruises in the South and West Pacific Ocean region. National Institute of Water and Atmospheric Research Ltd (NIWA). WellingtonNew Zealand Bathymetry compilation - 250 mMitchell, J S, K A Mackay, H L Neil, E J Mackay, A Pallentin and P Notman (2012). Undersea New Zealand, 1:5,000,000. NIWA Chart, Miscellaneous Series No. 92[https://niwa.co.nz/our-science/oceans/bathymetry/download-the-data](https://niwa.co.nz/our-science/oceans/bathymetry/download-the-data) Olex AS, NorwayCrowd source bathymetry data provided by Olex These data are primarily single beam soundings collected by fishing vessels using the Olex acquisition system. The data are provided gridded at a resolution of 400x400 m.[www.olex.no](http://www.olex.no/index_e.html) Pacific Islands Benthic Habitat Mapping Center (PIBHMC)65 gridded datasets, based on multibeam and satellite-derived bathymetry data collected around the Pacific Islands: Commonwealth of Northern Mariana Islands (CNMI) and Guam; Northwest Hawaiian Islands; Pacific Remote Island Area; American Samoa[http://www.soest.hawaii.edu/pibhmc/cms/](http://www.soest.hawaii.edu/pibhmc/cms/) Scripps Institution of Oceanography SRTM15+ V2 Global Bathymetry and Topography at 15 ArcsecondsTozer, B, Sandwell, D. T., Smith, W. H. F., Olson, C., Beale, J. R., & Wessel, P. (2019). Global bathymetry and topography at 15 arc sec: SRTM15+. Earth and Space Science. 6. [https://doi.org/10.1029/2019EA000658](https://doi.org/10.1029/2019EA000658).[https://topex.ucsd.edu/WWW_html/srtm15_plus.html](https://topex.ucsd.edu/WWW_html/srtm15_plus.html) Service Hydrographique et Océanographique de la Marine (SHOM), FranceBathymetric data supplied in the form of gridsLargely from multibeam and Lidar bathymetric surveys and transect cruises in areas of the Pacific, Atlantic and Indian Oceans, from the data holdings and cruises of SHOM. [https://data.shom.fr/](https://data.shom.fr/)Service Hydrographique et Océanographique de la Marine (SHOM), FranceBathymetric DEM of the waters off Guyana, Atlantic Ocean[https://diffusion.shom.fr/pro/risques/bathymetrie/mnt-facade-guyane-homonim.html](https://diffusion.shom.fr/pro/risques/bathymetrie/mnt-facade-guyane-homonim.html)[https://data.shom.fr/](https://data.shom.fr/)Shell Ocean Discovery XPRIZEData acquired as part of the Shell Ocean Discovery XPRIZE competitionData were contributed in an area in the Mediterranean Sea and near Puerto Rico.South West Indian Ocean Bathymetry Compilation (SWIOBC)The Southwest Indian Ocean Bathymetric Compilation (swIOBC)Dorschel, B, L Jensen, J E Arndt, G-J Brummer, H de Haas, A Fielies, D Franke, W Jokat, R Krocker, D Kroon, J Pätzold, R R. Schneider, V Spieß, H Stollhofen, G Uenzelmann‐Neben, M Watkeys and E Wiles (2018). The Southwest Indian Ocean Bathymetric Compilation (SwIOBC). Geochemistry, Geophysics, Geosystems 19, no. 3 (March 2018): 968–76.[https://doi.org/10.1002/2017GC007274](https://doi.org/10.1002/2017GC007274)Taylor, Brian (2006)Multibeam bathymetry compilation of the Lau Back-Arc Basin – 100mTaylor, B. (2006). Multibeam bathymetry compilation of the Lau Back-Arc Basin. Interdisciplinary Earth Data Alliance (IEDA). [http://dx.doi.org/10.1594/IEDA/100063](http://dx.doi.org/10.1594/IEDA/100063)The quest for the Africa–Eurasia plate boundary west of the Strait of GibraltarBathymetric grid based on multibeam data North Atlantic Ocean, Gulf of Cadiz region — SWIM project Reference: "Earthquake and Tsunami hazards of active faults at the South West Iberian Margin: deep structure, high-resolution imaging and paleoseismic signature". Data set citation — The quest for the Africa-Eurasia plate boundary west of the Strait of Gibraltar: Zitellini, N., Gràcia, E., Matias, L., Terrinha, P., Abreu, M.A., DeAlteriis, G., Henriet, J.P., Dañobeitia, J.J., Masson, D.G., Mulder, T., Ramella, R., Somoza, L. and Diez, S. (2009). Earth and Planetary Science Letters, 280, (1-4), 13-50. (doi:10.1016/j.epsl.2008.12.005)University of New Hampshire and its Center for Coastal and Ocean Mapping/Joint Hydrographic Center (UNH/CCOM-JHC)United States Law of the Sea DataAtlantic Grid, version 2019. [https://ccom.unh.edu/theme/law-sea/law-of-the-sea-data/atlantic](https://ccom.unh.edu/theme/law-sea/law-of-the-sea-data/atlantic) Weinrebe et al.Multibeam compilation of the Central America Pacific Margin Weinrebe, W., et al. (2007). Multibeam bathymetry compilation of the Central America Pacific Margin. Interdisciplinary Earth Data Alliance (IEDA). doi:10.1594/IEDA/100069 Weinrebe and HasertDTMs of the South East Pacific Ocean created from a compilation of multibeam bathymetric data acquired during 18 cruises in 1995-2012 Weinrebe, R.W., Hasert, M. (2012). Bathymetric Charts of the South East Pacific with links to gridded datasets. PANGAEA, [https://doi.org/10.1594/PANGAEA.785515](https://doi.org/10.1594/PANGAEA.785515)US-Extended Continental Shelf (ECS) cruisesBathymetry data from the U.S. Extended Continental Shelf (ECS) Project [https://www.ngdc.noaa.gov/mgg/ecs/cruises.html](https://www.ngdc.noaa.gov/mgg/ecs/cruises.html)
#### Multibeam and Single Beam Survey Data

Source Description and Reference (where available) IHO DCDB Bathymetric soundings, single beam and multibeam, extracted from the data maintained by the International Hydrographic Organization (IHO) Data Center for Digital Bathymetry (DCDB) at the US National Centers for Environmental Information (NCEI).[https://www.ngdc.noaa.gov/iho/](https://www.ngdc.noaa.gov/iho/) Alfred Wegener Institute (AWI) Multibeam data in the Atlantic and Indian Ocean region. 17 cruises of multibeam data in the South and West Pacific. 59 cruises of multibeam data in the Southern Ocean region (South of 50°S) [https://www.awi.de/en/](https://www.awi.de/en/) All-Russia Research Institute of Geology and Mineral Resources of the World Ocean (VNIIOkeangeologia) 2 cruises of multibeam data in the Southern Ocean region (South of 50°S). Data originators: Polar Marine Geosurvey Expedition (PMGE). Australian Antarctic Data Centre (AADC) 2 cruises of multibeam data and 6 cruises of single beam data in the Southern Ocean region (South of 50S). Australian Hydrographic Office (AHO) 4 cruises of single beam data in the Southern Ocean region (South of 50°S). AusSeabed Multibeam data from around Australia [http://www.ausseabed.gov.au/](http://www.ausseabed.gov.au/) Australia's Marine National Facility (MNF) 5 cruises of multibeam data in the Southern Ocean region (South of 50°S). British Antarctic Survey (BAS) 93 cruises multibeam data and 1 cruise of single beam data in the Southern Ocean region (South of 50°S). [https://www.bas.ac.uk/](https://www.bas.ac.uk/) Centro de investigaciones Oceanograficas e Hidrograficas (CIOH), Colombia 1 cruise of multibeam data in the Southern Ocean region (South of 50°S Fugro 16 Cruises of Multibeam data in the Atlantic and Indian Ocean region. GEBCO Alumni Indian Ocean Bathymetric Compilation 102 Cruises of Multibeam data in the Atlantic and Indian Ocean region from multiple international sources. Geological Institute, Russian Academy of Sciences (GIN RAS) Gridded multibeam bathymetry data from RV Akademik Nikolaj Strakhov Cruise 22 in the Atlantic Ocean. Survey data from RV Akademik Nikolaj Strakhov Cruises 7 and 11-12 in the Atlantic ocean. Geoscience Australia 2 cruises of multibeam data and 8 cruises of single beam data in the Southern Ocean region (South of 50°S). HafenCity Universität Hamburg, Germany 2 cruises of multibeam data for the Atlantic Ocean collected aboard the RV Sonne in 2018. L'Institut Français de Recherche pour l'Exploitation de la Mer (IFREMER), France 3 cruises of multibeam data and 1 cruise of single beam data in the Southern Ocean region (South of 50°S). Instituto Geologico y Minero de Espana (IGME), Spain 9 cruises of multibeam data in the Southern Ocean region (South of 50°S). Istituto Nazionale di Oceanografia e di Geofisica Sperimentale (OGS), Italy 9 cruises of multibeam data in the Southern Ocean region (South of 50°S). Italian Hydrographic Institute (IHI) 1 cruise of single beam data in the Southern Ocean region (South of 50°S). Japan Agency for Marine-Earth Science and Technology (JAMSTEC) South and West Pacific Ocean region: 858 cruises of Multibeam data accessed through: Data and Sample Research System for Whole Cruise Information Southern Ocean region (South of 50°S): 7 cruises of multibeam data [http://www.godac.jamstec.go.jp/darwin/e](http://www.godac.jamstec.go.jp/darwin/e) Japanese Antarctic Research Expedition (JARE) 4 cruise of single beam data in the Southern Ocean region (South of 50°S) Japan Oceanographic Data Center (JODC) 4 cruise of multibeam data in the Southern Ocean region (South of 50°S) Korea Polar Research Institute (KOPRI) Southern Ocean region (South of 50°S): 19 cruises of multibeam data Lamont-Doherty Earth Observatory, Columbia University, Earth Institute (R/V Marcus G. Langeth expeditions) Southern Ocean region (South of 50°S): 11 cruises of single beam data.Marine Institute of Ireland Multibeam data form 3 cruises conducted aboard the Celtic Explorer in the Atlantic Ocean acquired as part of the AORA effort. Marine Geoscience Data System (MGDS), Lamont-Doherty Earth Observatory, Columbia University 9 cruises of multibeam data in the South and West Pacific Ocean. 138 cruises of multibeam data and over 600 cruises of single beam data in the Southern Ocean (South of 50°S). National Geospatial-Intelligence Agency (NGA) 27 cruises of single beam data and one file of isolated soundings for the Southern Ocean region (South of 50°S). National Institute of Polar Research (Japan) (NiPR) 4 cruises of multibeam data for the Southern Ocean region (South of 50°S). National Institute of Water and Atmospheric Research (New Zealand) 4 cruises of multibeam data for the Southern Ocean region (South of 50°S). Ocean Exploration Trust Gridded multibeam data from 8 cruises of the RV “Nautilus” (2019) in the South and West Pacific region [https://nautiluslive.org/expedition/2019](https://nautiluslive.org/expedition/2019) Multibeam data for 54 cruises in the North Pacific region [https://nautiluslive.org/expedition-map](https://nautiluslive.org/expedition-map) Polar Marine Geosurvey Expedition (PMGE) 1 cruise of multibeam and 27 cruises of single beam data for the Southern Ocean region (South of 50°S).Scripps Institution of Oceanography (SIO) 1 cruise of multibeam data for the Southern Ocean region (South of 50°S). Servicio Hidrografico y Oceanograficos de la Armada de Chile (SHOA) 1 cruise of single beam data for the Southern Ocean region (South of 50°S).State Oceanic Administration (China) (SOA) 5 cruises of single beam data for the Southern Ocean region (South of 50°S). Stockholm University 4 cruises of multibeam data for the Southern Ocean region (South of 50°S). Ukraine Antarctic Expedition (UAE) 13 cruises of single beam data for the Southern Ocean region (South of 50S). University of New Hampshire, Center for Coastal and Ocean Mapping/Joint Hydrographic Center Multibeam bathymetry from U.S. Law of the Sea cruise to map the foot of the slope and 2500-m isobath of the US Arctic Ocean margin carried Center for Coastal and Ocean Mapping/Joint Hydrographic Center, University of New Hampshire:[https://ccom.unh.edu/theme/law-sea/arctic-ocean](https://ccom.unh.edu/theme/law-sea/arctic-ocean)HLY1603, HLY1202, HLY1102, HLY0905, HLY0805, HLY0703, HLY0302, HLY0405, HLY0503.Bathymetry are in addition provided from the following expeditions with USCGC Healy through the Center for Coastal and Ocean Mapping/Joint Hydrographic Center, or retrieved from the IHO-DCDB: HLY0201, HLY0203, HLY0204, HLY0304, HLY0402, HLY0403, HLY0404, HLY0501, HLY0502, HLY0602, HLY0804, HLY0806, HLY0904, HLY1002 University of Tasmania (UTAS) 1 cruise of single beam data and 1 file of isolated sounding data for the Southern Ocean region (South of 50S). US Geological Survey 1 cruise of single beam data for the Southern Ocean region (South of 50°S).
#### Other contributions

Source Description and Reference (where available) Member States of the International Hydrographic Organization (IHO) Bathymetric soundings extracted from Electronic Navigation Charts (ENCs) provided by IHO Member States. Access further details about ENC contributions made to GEBCO. [www.gebco.net/data-products/gridded-bathymetry-datashallow_water_bathymetry](https://www.gebco.net/data-products/gridded-bathymetry-datashallow_water_bathymetry) List of countries/organisations that have contributed ENC data directly to GEBCO: Australian Hydrographic Service (RAN); AustraliaBundesamt fur Seeschifffahrt und Hydrographie, Germany;Directorate of Hydrography and Navigation, Peru;East Asia Hydrographic Commission;Finnish Hydrographic Office, Finland;Flemish Hydrography, Belgium;Hellenic Navy Hydrographic Service, Greece;Hydrographic service office of the Kingdom of Bahrain;Hydrographic Service, Maritime Administration of Latvia;Hydrographic Office of the Polish Navy, Poland;Hydrographic Office, South Africa;State Hydrographic Service of Ukraine;Royal Malaysian NavyServicio de Hidrografía, Oceanografía; Meteorología y Cartografiado Náutico, Venezuela;Instituto Oceanographico de la Armada, Ecuador;Instituto Idrografico Della Marina, Italy;Instituto Hidrografico, Portugal;Korea Hydrographic and Oceanographic Administration, Korea (Republic of);National Hydrographic Office, India;National Ocean Service, USA;Netherlands Hydrographic Office, The Netherlands;Norwegian Mapping Authority, Norway;Servicio Hidrográfico y Oceanográfico de la Armada, Chile;Swedish Maritime Administration, Sweden;Centro De Hidrografia Da Marinha, Brazil;Uruguayan Navy Oceanography, Hydrography and Meteorology Service;Argentina Davey, F.J., 2004Ross Sea Bathymetry (1:200,000) Bathymetric map, Version 1.0, Institute of Geological and Nuclear Sciences, geophysical Map 16, GNS Ltd, Lower Hutt, New Zealand Stagpoole, V.M. et al, 2004Bathymetry of the Ross Dependency and adjacent Southern ocean 1:5,000,000, Version 1.0. Institute of Geological and Nuclear Sciences, Lower Hutt, New Zealand, geophysical map 17. GNS Ltd, Lower Hutt, New Zealand
#### 11.0 References

Danielson, J.J., and Gesch, D.B., 2011, Global multi-resolution terrain elevation data 2010 (GMTED2010): U.S. Geological Survey Open-File Report 2011–1073, 26 p.

Fretwell, P, H D Pritchard D G Vaughan, J L Bamber, N E Barrand, R Bell, C. Bianchi, R G Bingham, D D Blankenship, G Casassa, G Catania, D Callens, H Conway, A J Cook, H F J Corr, D Damaske,V Damm, F Ferraccioli, R Forsberg, S Fujita, Y Gim, P Gogineni, J A Griggs, R C A Hindmarsh, P Holmlund, J W Holt, R W Jacobel, A Jenkins, W Jokat, T Jordan, E C King, J Kohler, W Krabill, M Riger-Kusk, K A Langley, G Leitchenkov, C Leusche, B P Luyendyk, K Matsuoka, J Mouginot,F O Nitsche, Y Nogi, O A Nost, S V Popov, E Rignot, D M Rippin, A Rivera, J Roberts, N Ros, M J Sieger, A M Smith, D Steinhage, M Studinger, B Sun, B K Tinto, B C Welch, D Wilson, D A Young, C Xiangbin and A Zirizzotti (2013). Bedmap2: improved ice bed, surface and thickness datasets for Antarctica, The Cryosphere, 7, 375-393, 2013, doi.org/10.5194/tc-7-375-2013.

GEBCO Bathymetric Compilation Group 2019 (2019). The GEBCO_2019 Grid - a continuous terrain model of the global oceans and land. British Oceanographic Data Centre, National Oceanography Centre, NERC, UK. doi:10/c33m. doi:10.5285/836f016a-33be-6ddc-e053-6c86abc0788e

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