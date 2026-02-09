Ultraviolet Aerosol Index (UVAI) data

The daily UVAI data available was obtained for 2012–2016 (freely available for years 2004-present). Positive UVAI values indicate the presence of absorbing aerosols such as dust, and also black carbon often associated with biomass burning activities. Whereas, negative values indicate non-absorbing aerosols. The OMEAERUV dataset based on the Ozone Monitoring Instrument (OMI) imagery in 354nm– 388nm spectral range produces UVAI measurements based on the columnar data and are provided at a spatial resolution of approximately 0.25 degrees [51–52]. Unlike MODIS with a two-satellite constellation, OMI onboard the Aura satellite, operates with one daily overpass instead of twice daily. Because UVAI values range from negative to positive with low values indicative of non-absorbing aerosols or cloud cover, we removed all values less than 0.1, in order to better represent absorbing aerosol pollution values related to biomass burning.

Cloud cover data

Cloud cover data was freely obtained from NASA’s Clouds and the Earth’s Radiant Energy System (CERES) website. The SSF1deg dataset which contains MODIS cloud area fraction data was obtained for 12 years (2003–2014) at a daily temporal resolution and 1 degree spatial resolution, and freely available from 2000-present [53–54]. This dataset was used to provide ancillary information for the analysis and general cloud cover trends over Hanoi and the rest of the Continental Southeast Asia region.

Methods

Hanoi, Vietnam has experienced routinely degraded air quality over the past several decades due to urban expansion and development, as well as emissions from rice residue biomass burning especially during June and October [31]. While emissions from rice residue burning have been quantified, it’s unknown how much impact is measured through the satellite air pollution datasets. We integrated meteorological factors such as wind speed, direction, and precipitation combined with MODIS active fire data to explore BC trends and levels. We also assessed the potential of UVAI for monitoring absorbing aerosols from biomass burning, such as rice residue burning in Hanoi, which is a heavily cloud-covered region. Moreover, we compare average monthly MODIS cloud fractions over the region, as well as the average monthly number of clear sky observations of OMI UVAI per month.

We employed a timeseries of 3-hourly Merra-2 Reanalysis BC concentration data to explore pollution trends over both Hanoi City as well as the surrounding continental Southeast Asia. We explore the BC concentration and distribution of values throughout the time period using boxplots and timeseries plots, as well as exploring patterns of extreme values through time using the 90th and 95th percentiles of daily averaged data. We explore the same using 3-hourly data to further explore trends in diurnal variation of BC, and compare day and night values by averaging from 9am– 9PM (Day) and 9PM– 9AM (Night). We further investigate trends in BC concentrations during the rice residue burning months of June and October to determine if BC levels are elevated during these significant biomass burning events which emit a large amount of fine-particulate matter [31]. We also investigate pollutant transport and contribution to variability in BC levels from the surrounding region based on synoptic wind direction patterns and biomass burning based on MODIS active fire products averaged on a monthly scale throughout the surrounding continental Southeast Asia region.

To better understand the type of pollutants observed during different months, we compare UVAI values with BC values to infer if the source of pollution can be attributed to biomass burning or not as positive UVAI values can be representative of absorbing aerosols related to biomass burning [33].

Lastly, we adjust the BC data based on meteorological parameters such as rain, and compare the original BC with rain, which impacts BC levels significantly due to increased wet deposition. Previous work has adjusted, or detrended, different aerosol species based on meteorological variables and often found non-linear relationship between the pollutant and precipitation [55–57]. Rainfall-adjusted values have the most utility for monitoring changes in long-term pollutant trends as well as other long-term studies such as relating to climate, aerosols, and evapotranspiration [58–59]. A best-fit regression is conducted on the BC and rainfall data resulting in a non-linear power-function fit as,
Where ‘y’ is the daily BC concentration, ‘a’ is a constant and ‘x’ is daily rainfall. The equation can be linearized by taking the base 10 log of both sides of equation to obtain:

Then for each day of BC data we minimize the effects of rainfall by first calculating the residual:
Where ŷ is the predicted BC and yi is the observed BC for that day. We then subtracted the residual from our original BC data to get rainfall-adjusted BC concentration useful to compare variation between the biomass burning months and non-biomass burning months and general longer-term trends.

Results
Cloud conditions over Hanoi

Country-level analysis of cloud cover fraction in continental southeast Asia revealed Vietnam as having the highest monthly average cloud cover (72.4%) followed by Cambodia (69.7%), Laos (67.7%), Thailand (67.6%), and Myanmar (59.9%) (Fig 1). Moreover, of these different countries, Vietnam also has the lowest monthly active fire detections with 647 hinting at potential under detections due to cloud cover. Monitoring of active fires from rice residue burning in the Red River Delta is especially difficult. For example, the month of highest cloud cover is during the rainy season of July or August for most of Thailand, Myanmar, Cambodia, and Southern Vietnam. In contrast, Hanoi and the Red River Delta experience highest cloud coverage during the June residue burning time, whereas there are fewer clouds during November and December. In comparing the two rice growing regions of Vietnam, the Red River Delta averages only 25 active fires during the June rice burning time, whereas the Mekong River Delta averages 556 fires during the peak residue burning month of March. This discrepancy can be largely attributed to the higher cloud cover over the Red River Delta during burning months, compounded by relatively smaller field and fire sizes with average field size of about 5000m2 in the Mekong River Delta compared to about 800m2 in Hanoi and the Red River Delta [30–31, 60–61].

	Download:
PPT
PowerPoint slide
PNG
larger image
TIFF
original image
Fig 1. Monthly cloud cover averaged by month (2003–2014) per 1 degree grid cell.

https://doi.org/10.1371/journal.pone.0196629.g001

Consistently high cloud coverage over the Red River Delta and Hanoi, has important implications for monitoring air pollution and air quality in these regions. For example, current satellite-based datasets provide daily observations of global air pollution, but cannot provide meaningful local observation if obstructed by cloud.

Wind and active fires

Transport of polluted air into Hanoi becomes apparent from monthly averaged wind direction and speed patterns shown in Fig 2 along with monthly average BC surface concentrations. General synoptic meteorology patterns indicate northerly winds flowing from South China into Northern Vietnam and Hanoi during October–March, whereas during Apr-Aug more south or southeasterly winds from Laos, Southern Vietnam, and the South China Sea. BC levels in the Southeast Asia region show a peak during March across Thailand and Myanmar attributed to agricultural and small-holder burning fires detected by MODIS (Fig 3) [33]. During March and April, high BC values over Laos and Northwest province of Vietnam are attributed especially to forest fires and slash and burn agriculture [30]. Relatively high BC levels throughout all months are consistently observed from Southern China largely originating from the mega-urban Chengdu and Chongqing cities with biomass burning also as a non-negligible emission source during these months [62–63].

	Download:
PPT
PowerPoint slide
PNG
larger image
TIFF
original image
Fig 2. Monthly average BC concentration, wind direction and speed.

https://doi.org/10.1371/journal.pone.0196629.g002

	Download:
PPT
PowerPoint slide
PNG
larger image
TIFF
original image
Fig 3. Average MODIS active fire trends in the surrounding region.

https://doi.org/10.1371/journal.pone.0196629.g003

Trends in the latest MODIS collection 6 active fire algorithm show peak burning in March and April as well as high levels of burning during Jan-Feb across much of Laos, Myanmar, Vietnam, Cambodia, and Northern Thailand due to forest and agricultural biomass burning (Fig 3). Relatively low active fires are detected across the region during June–November, a large portion of which is attributed to the rainy season (Table 1).

	Download:
PPT
PowerPoint slide
PNG
larger image
TIFF
original image
Table 1. Average monthly MODIS active fire counts within 1000km of Hanoi.

https://doi.org/10.1371/journal.pone.0196629.t001

BC concentrations during October reach as much as 45% higher than the following month of November with the largest difference in 2015. On average, BC levels are 19% higher in October than November. These two months are relatively comparable due to synoptic wind patterns, rainfall, and active fires, as well as being adjacent in time.

UVAI and number of clear observations

The UVAI is a satellite-derived pollution index sensitive to absorbing aerosols related to biomass burning. The average monthly total number of cloud-free observations for the UVAI (where UVAI > 0.1) are shown across Northern Vietnam in Fig 4. Over Hanoi, the highest number of observations occur during May and December which are generally drier months, still averaging only 5 or 6 clear observations. Whereas, very few observations are recorded especially during rainy months of June-August. The remaining months only experience between 1 and 5 clear observations on average (Fig 4). This lack of clear observations makes it very difficult to monitor the effects of air pollution with remote sensing. Moreover, because air pollution episodes often occur over rapid time-scales lasting for a few days [10,33], severe pollution events could be missed entirely, such as rice residue biomass burning events which occur in June and October.
