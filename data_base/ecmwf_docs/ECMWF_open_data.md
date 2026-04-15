# ECMWF Documentation

Source: https://www.ecmwf.int/en/forecasts/datasets/open-data

---

-

Open data | ECMWF

[
](#main-content)

# Open data

[ECMWF Terms of Use](https://apps.ecmwf.int/datasets/licences/general/)

[Browse the data files](https://data.ecmwf.int/forecasts/)

Licence:
[description View licence](http://apps.ecmwf.int/datasets/licences/general)

A subset of ECMWF real-time forecast data from the IFS and AIFS models is made available to the public free of charge. Their use is governed by the [Creative Commons CC-BY-4.0 licence](https://creativecommons.org/licenses/by/4.0/deed.en) and the [ECMWF Terms of Use](https://apps.ecmwf.int/datasets/licences/general/). This means that the data may be redistributed and used commercially, subject to [appropriate attribution](https://apps.ecmwf.int/datasets/licences/general/).

Accessing this data, or arranging for any open data to be delivered directly to you, may be subject to [Service Charges](https://confluence.ecmwf.int/display/DAC/Service+Charges%3A+From+01+July+2024) and a Service Agreement. If you are interested in this, please see our [Service Agreement and Use Cases](https://www.ecmwf.int/en/forecasts/accessing-forecasts/licences-available) page.

For more information, please refer to the [User Documentation](https://confluence.ecmwf.int/display/DAC/ECMWF+open+data%3A+real-time+forecasts+from+IFS+and+AIFS) or visit the [ECMWF Support Portal.](https://confluence.ecmwf.int/site/support)

This page outlines the subset of free and open IFS and AIFS parameters available.

[Sign up](mailto:open-data-community-subscribe@lists.ecmwf.int?subject=subscribe) for an open data community mailing list, a joint project with EUMETSAT, Met Norway and German national meteorological service DWD to share new and updated open datasets, relevant resources, conferences and articles [>>>](mailto:open-data-community-subscribe@lists.ecmwf.int?subject=subscribe)

## Product description

These products are a subset of the full [Catalogue of ECMWF Real-time Products](/en/forecasts/datasets/catalogue-ecmwf-real-time-products) and are based on the medium-range ([high-resolution and ensemble](/en/forecasts/documentation-and-support/medium-range-forecasts)) and [seasonal](/en/forecasts/documentation-and-support/long-range) forecast models.

IFS data are released at the end of the [real-time dissemination schedule](https://confluence.ecmwf.int/display/DAC/Dissemination+schedule). AIFS data are released as soon the data are produced.

For further details about the available AIFS products, see the dataset descriptions for the [Deterministic AIFS](https://www.ecmwf.int/en/forecasts/datasets/set-ix) and [Ensemble AIFS](https://www.ecmwf.int/en/forecasts/datasets/set-x).

Products are available at 0.25 degrees resolution in GRIB2 format unless stated otherwise. Future updates to the Open Data catalog may include further resolution improvement, in line with developments in the ECMWF product catalogue. Since July 2023, the [ending of products in GRIB2 has changed to use CCSDS compression](https://confluence.ecmwf.int/display/FCST/Implementation+of+IFS+Cycle+48r1#ImplementationofIFSCycle48r1-Technicalcontent).

Important:

Higher-resolution products: Higher-resolution versions of the same products are available via the [Product Requirements Catalogue](https://products.ecmwf.int/requirements/) and are subject to a Real-time Dissemination Service Agreement. Please see the [Service Agreements and Use cases](https://www.ecmwf.int/en/forecasts/accessing-forecasts/licences-available) for more information.

-

System stability and access limits: To ensure the stability of our systems and to preserve resources for operational activities, access to the Open-Data Portal is currently limited to 500 simultaneous connections. This limit helps guarantee reliable service for operational users, especially during periods of high demand.

-

Rolling archive and data availability: ECMWF Open Data provides access to real-time forecast data on a rolling archive basis. Data are retained for the most recent 12 forecast runs, corresponding to approximately 2–3 days of forecasts based on the four daily IFS and AIFS cycles (00, 06, 12 and 18 UTC). If you are interested in accessing the full historical data archive, please see the [Service Agreements and Use cases](https://www.ecmwf.int/en/forecasts/accessing-forecasts/licences-available) for more information.

Alternative access methods and cloud platforms

For improved global accessibility and added redundancy, ECMWF Open Data subset is replicated and available on major public cloud platforms, including [Amazon Web Services (AWS)](https://registry.opendata.aws/ecmwf-forecasts/), [Microsoft Azure](https://ai4edataeuwest.blob.core.windows.net/ecmwf/) and [Google Cloud Platform (GCP)](https://console.cloud.google.com/marketplace/product/bigquery-public-data/open-data-ecmwf). These alternative access methods can be particularly useful for users who experience connectivity limitations, high demand periods, or performance constraints when accessing the Open-Data Portal directly. Users may either access the data directly via these public cloud storage services or use the [ecmwf-opendata](https://github.com/ecmwf/ecmwf-opendata) Python client, which allows selecting the data source (ecmwf, aws, azure or google) while providing a consistent interface across platforms. If you experience difficulties accessing the Open-Data Portal directly, retrieving the data from one of these cloud service providers is recommended. For more detailed technical documentation, file naming conventions, and download examples, please see the ECMWF Open Data technical [documentation](https://confluence.ecmwf.int/display/DAC/ECMWF+open+data%3A+real-time+forecasts+from+IFS+and+AIFS).

IFS Data

High-resolution products:

Steps:

- For times 00z &12z: 0 to 144 by 3, 150 to 360 by 6.

- For times 06z & 18z: 0 to 144 by 3.

Type of level data:

Surface (sfc), Surface Other level (sol) and Pressure Level (pl)

Pressure levels available (hPa): 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50

Only a single ID is used for Volumetric soil water and Soil Temperature with layer 1 having level=1, layer 2 having level=2 etc. Layers 1-4 are available.

Parameters: as described below

Short name
Long name
ID
Type of level

z
Geopotential (step 0)
129
sfc

sdor
Standard deviation of sub-gridscale orography (step 0)
160
sfc

slor
Slope of sub-gridscale orography (step 0)
163
sfc

10u
10 metre U wind component
165
sfc

10v
10 metre V wind component
166
sfc

100u
100 metre U wind component
228246
sfc

100v
100 metre V wind component
228247
sfc

10fg
Maximum 10 metre wind gust since previous post-processing - (appears as 10fg3 for steps 3 to 144)
49 / 228028
sfc

2t
2 metre temperature
167
sfc

2d
2 metre dewpoint temperature
168
sfc

msl
Mean sea level pressure
151
sfc

mp2
Mean zero-crossing wave period
140221
sfc

mwd
Mean wave direction
140230
sfc

mwp
Mean wave period
140232
sfc

pp1d
Peak wave period
140231
sfc

swh
Significant height of combined wind waves and swell
140229
sfc

ro
Runoff
205
sfc

tp
Total Precipitation
228
sfc

sp
Surface pressure
134
sfc

tcwv
Total column vertically-integrated water vapour
137
sfc

tcc
Total cloud cover
164
sfc

sd
Snow depth water equivalent
141
sfc

sf
Snowfall water equivalent
144
sfc

lsm
Land Sea Mask
172
sfc

vsw
Volumetric soil water (layers 1-4)
260199
sol

sot
Soil temperature (layers 1-4)
260360
sol

mucape
Most-unstable convective available potential energy
228235
sfc

asn
Snow albedo
32
sfc

mn2t3
Minimum temperature at 2 metres in the last 3 hours
228027
sfc

mx2t3
Maximum temperature at 2 metres in the last 3 hours
228026
sfc

mn2t6
Minimum temperature at 2 metres in the last 6 hours
122
sfc

mx2t6
Maximum temperature at 2 metres in the last 6 hours
121
sfc

tprate
Total precipitation rate
260048
sfc

ptype
Precipitation type
260015
sfc

ttr
Top net long-wave (thermal) radiation
179
sfc

rsn
Snow density (new from 11/02/2026!)
33
sfc

str
Surface net long-wave (thermal) radiation
177
sfc

ssr
Surface net short-wave (solar) radiation
176
sfc

ssrd
Surface net short-wave (solar) radiation downwards
169
sfc

strd
Surface net long-wave (thermal) radiation downwards
175
sfc

nsss
Time-integrated northward turbulent surface stress
181
sfc

ewss
Time-integrated eastward turbulent surface stress
180
sfc

t20d
Depth of 20C isotherm - currently unavailable (11/03/2024)

sfc

sav300
Average salinity in the upper 300m - currently unavailable (11/03/2024)

sfc

sve
Eastward sea water velocity
262140
sfc

svn
Northward sea water velocity
262139
sfc

sithick
Sea ice thickness
262000
sfc

zos
Sea surface height
262124
sfc

d
Divergence
155
pl

gh
Geopotential height
156
pl

q
Specific humidity
133
pl

r
Relative humidity
157
pl

t
Temperature
130
pl

u
U component of wind
131
pl

v
V component of wind
132
pl

w
Vertical velocity
135
pl

vo
Vorticity (relative)
138
pl

Tropical cyclone tracks - high-resolution products

Long name
Format
Type of level
Steps for times 00 &12
Steps for times 06 &18

Tropical Cyclone Trajectory (TC track including genesis)

BUFR
sfc
up to step 240
up to step 90

Ensemble products​

Steps:

- For times 00z &12z: 0 to 144 by 3, 150 to 360 by 6.

- For times 06z & 18z: 0 to 144 by 3.

Type of level data:

Surface (sfc), Surface Other level (sol) and Pressure Level (pl)

Pressure levels available (hPa): 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50

Only a single ID is used for Volumetric soil water and Soil Temperature with layer 1 having level=1, layer 2 having level=2 etc. Layers 1-4 are available.

Parameters: as described below

Short name
Long name
ID
Type of level

z
Geopotential (step 0)
129
sfc

sdor
Standard deviation of sub-gridscale orography (step 0)
160
sfc

slor
Slope of sub-gridscale orography (step 0)
163
sfc

10u
10 metre U wind component
165
sfc

10v
10 metre V wind component
166
sfc

100u
100 metre U wind component
228246
sfc

100v
100 metre V wind component
228247
sfc

10fg
Maximum 10 metre wind gust since previous post-processing - (appears as 10fg3 for steps 3 to 144)
49 / 228028
sfc

2t
2 metre temperature
167
sfc

2d
2 metre dewpoint temperature
168
sfc

msl
Mean sea level pressure
151
sfc

mp2
Mean zero-crossing wave period
140221
sfc

mwd
Mean wave direction
140230
sfc

mwp
Mean wave period
140232
sfc

pp1d
Peak wave period
140231
sfc

swh
Significant height of combined wind waves and swell
140229
sfc

ro
Runoff
205
sfc

tp
Total Precipitation
228
sfc

sp
Surface pressure
134
sfc

st
Soil temperature
228139
sfc

tcwv
Total column vertically-integrated water vapour
137
sfc

tcc
Total cloud cover
164
sfc

sd
Snow depth water equivalent
141
sfc

sf
Snowfall water equivalent
144
sfc

lsm
Land Sea Mask
172
sfc

vsw

Volumetric soil water (layers 1-4)
260199
sol

sot
Soil temperature (layers 1-4)
260360
sol

mucape
Most unstable convective available potential energy
228235
sfc

asn
Snow albedo
32
sfc

mn2t3
Minimum temperature at 2 metres in the last 3 hours
228027
sfc

mx2t3
Maximum temperature at 2 metres in the last 3 hours
228026
sfc

mn2t6
Minimum temperature at 2 metres in the last 6 hours
122
sfc

mx2t6
Maximum temperature at 2 metres in the last 6 hours
121
sfc

tprate
Total precipitation rate
260048
sfc

ptype
Precipitation type
260015
sfc

ttr
Top net long-wave (thermal) radiation
179
sfc

rsn
Snow density
33
sfc

str
Surface net long-wave (thermal) radiation
177
sfc

ssr
Surface net short-wave (solar) radiation
176
sfc

ssrd
Surface net short-wave (solar) radiation downwards
169
sfc

strd
Surface net long-wave (thermal) radiation downwards
175
sfc

nsss
Time-integrated northward turbulent surface stress
181
sfc

ewss
Time-integrated eastward turbulent surface stress
180
sfc

t20d
Depth of 20C isotherm - currently unavailable (11/03/2024)

sfc

sav300
Average salinity in the upper 300m - currently unavailable (11/03/2024)

sfc

sve
Eastward sea water velocity
262140
sfc

svn
Northward sea water velocity
262139
sfc

sithick
Sea ice thickness
262000
sfc

zos
Sea surface height
262124
sfc

d
Divergence
155
pl

gh
Geopotential height
156
pl

q
Specific humidity
133
pl

r
Relative humidity
157
pl

t
Temperature
130
pl

u
U component of wind
131
pl

v
V component of wind
132
pl

w
Vertical velocity
135
pl

vo
Vorticity (relative)
138
pl

Tropical cyclone tracks - ensemble products

The tropical cyclone trajectories are computed independently for each ensemble member; a given tropical cyclone may dissipate at different times in different members so the number of members predicting a given tropical cyclone may vary through the forecast.

Long name
Format
Type of level
Steps for times 00 &12
Steps for times 06 &18

Tropical Cyclone Trajectory (TC track including genesis)

BUFR
sfc
up to step 360
up to step 144

Ensemble means and standard deviations

​​Steps for times 00z &12z: 0 to 144 by 3, 150 to 360 by 6.

Short Name
Long Name
ID
Level

gh
Geopotential height
156
300, 500, 1000

t
Temperature
130
250, 500, 850

ws
Wind speed
10
250, 850

msl
Mean sea level pressure
151
Single

Probabilities, daily weather events

Ranges for times 00z &12z: 0-24 to 336-360 by 12​​

Short Name
Long Name
ID
Threshold
Type of level

tpg1
Total precipitation of at least 1 mm
131060
>1mm
sfc

tpg5
Total precipitation of at least 5 mm
131061
>5mm
sfc

tpg10
Total precipitation of at least 10 mm
131062
>10mm
sfc

tpg20
Total precipitation of at least 20 mm
131063
>20mm
sfc

tpg25
Total precipitation of at least 25 mm
131098
>25mm
sfc

tpg50
Total precipitation of at least 50 mm
131099
>50mm
sfc

tpg100
Total precipitation of at least 100 mm
131085
>100mm
sfc

10fgg10
10 metre wind gusts of at least 10 m/s
131100
>10m/s
sfc

10fgg15
10 metre wind gusts of at least 15 m/s
131070
>15m/s
sfc

10fgg25
10 metre wind gusts of at least 25 m/s
131072
>25m/s
sfc

Probabilities, instantaneous weather events - atmosphere

Steps for times 00z &12z: 12 to 360 by 12​

Level: 850 hPa

Short Name
Long Name
Type of level

ptsa_gt _1stdev
Probability of temperature standardized anomaly greater than 1 standard deviation
pl

ptsa_gt _1p5stdev
Probability of temperature standardized anomaly greater than 1.5 standard deviation
pl

ptsa_gt _2stdev
Probability of temperature standardized anomaly greater than 2 standard deviation
pl

ptsa_lt _1stdev
Probability of temperature standardized anomaly less than -1 standard deviation
pl

ptsa_lt _1p5stdev
Probability of temperature standardized anomaly less than -1.5 standard deviation
pl

ptsa_lt _2stdev
Probability of temperature standardized anomaly less than -2 standard deviation
pl

Probabilities, instantaneous weather events - wave

​Steps for times 00z &12z: 12 to 360 by 12

Short Name
Long Name
ID
Threshold
Type of level

swhg2
Significant wave height of at least 2 m
131074
>2 m
sfc

swhg4
Significant wave height of at least 4 m
131075
>4 m
sfc

swhg6
Significant wave height of at least 6 m
131076
>6 m
sfc

swhg8
Significant wave height of at least 8 m
131077
>8 m
sfc

Seasonal products - Not yet available (as of 01/03/2024)

Name
Long Name
ID
Type of Level
Steps for time 00

sst
Sea Surface Temperature
34
sfc

1 to 6 months

## AIFS data

- 4 forecast runs per day (00/06/12/18)

- 6 hourly steps to 360 (15 days)

AIFS Single - forecast

Short Name
Long Name
ID
Type of level

z
Geopotential
129
sfc

tcw
Total column water
136
sfc

msl
Mean sea level pressure
151
sfc

sdor
Standard deviation of sub-gridscale orography
160
sfc

slor
Slope of sub-gridscale orography
163
sfc

10u
10 metre U wind component
165
sfc

10v
10 metre V wind component
166
sfc

2t
2 metre temperature
167
sfc

2d
2 metre dewpoint temperature
168
sfc

ssrd
Surface short-wave (solar) radiation downwards
169
sfc

lsm
Land-sea mask
172
sfc

strd
Surface long-wave (thermal) radiation downwards
175
sfc

lcc
Low cloud cover
3073
sfc

mcc
Medium cloud cover
3074
sfc

hcc
High cloud cover
3075
sfc

rowe
Runoff water equivalent (surface plus subsurface)
231002
sfc

cp
Convective precipitation
228143
sfc

sf
Snowfall water equivalent
228144
sfc

tcc
Total cloud cover
228164
sfc

tp
Total precipitation
228228
sfc

100u
100 metre U wind component
228246
sfc

100v
100 metre V wind component
228247
sfc

skt
Skin temperature
235
sfc

sp
Surface pressure
134
sfc

z
Geopotential
129
pl

t
Temperature
130
pl

u
U component of the wind
131
pl

v
V component of the wind
132
pl

q
Specific humidity
133
pl

w
Vertical velocity
135
pl

vsw
Volumetric soil moisture
260199
sol

sot
Soil temperature
260360
sol

AIFS ENS - forecast

Short Name
Long Name
ID
Type of level

z
Geopotential
129
sfc

sp
Surface pressure
134
sfc

tcw
Total column water
136
sfc

msl
Mean sea level pressure
151
sfc

sdor
Standard deviation of sub-gridscale orography
160
sfc

slor
Slope of sub-gridscale orography
163
sfc

10u
10 metre U wind component
165
sfc

10v
10 metre V wind component
166
sfc

2t
2 metre temperature
167
sfc

2d
2 metre dewpoint temperature
168
sfc

ssrd
Surface short-wave (solar) radiation downwards
169
sfc

lsm
Land-sea mask
172
sfc

strd
Surface long-wave (thermal) radiation downwards
175
sfc

skt
Skin temperature
235
sfc

lcc
Low cloud cover
3073
sfc

mcc
Medium cloud cover
3074
sfc

hcc
High cloud cover
3075
sfc

rowe
Runoff water equivalent (surface plus subsurface)
231002
sfc

sf
Snowfall water equivalent
228144
sfc

tcc
Total cloud cover
228164
sfc

tp
Total precipitation
228228
sfc

100u
100 metre U wind component
228246
sfc

100v
100 metre V wind component
228247
sfc

z
Geopotential
129
pl

t
Temperature
130
pl

u
U component of wind
131
pl

v
V component of wind
132
pl

q
Specific humidity
133
pl

w
Vertical velocity
135
pl

sot
Soil temperature
260360
sol

Type:

Real-time

Range:

Medium (15 days)
Long (Months)

DOI:
[https://doi.org/10.21957/open-data](https://doi.org/10.21957/open-data)

Provided by: ECMWF

[◀ View Datasets search](/en/forecasts/datasets/search)

expand_less

expand_more