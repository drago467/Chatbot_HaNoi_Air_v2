# Paper 1: Phung-Ngoc et al. 2023 - Intricate behavior of winter pollution in Hanoi

## Citation
- **Title**: Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period
- **Authors**: Bao-Anh Phung-Ngoc, Elsa Dieudonné, Hervé Delbarre, Karine Deboudt, Song-Tung Nguyen, Van-Hai Bui, Duc-Minh Vu, Huyen-Thu Nguyen-Thi
- **Journal**: Atmospheric Environment
- **Volume**: 300, 119669
- **Year**: 2023
- **DOI**: https://doi.org/10.1016/j.atmosenv.2023.119669
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings for Cold Surge Mechanisms

### 1. Cold Surge Onset - Long-range Transport Chain
- **Quote**: "During cold surge onsets, long-range transport from China causes an average increase of ~30% in PM2.5 concentrations."
- **Mechanism**: Northeast monsoon cycles create periodic changes in air masses pathways
- **Chain**: cold_surge_onset → air_mass_trajectory_change → regional_transport → pm25 (+30%)

### 2. Cold Surge Persistence - Local Stagnation Chain
- **Quote**: "The stagnation of local pollution during the cold surges persistence causes an average increase of ~40% in level of PM2.5."
- **Mechanism**: Stagnation conditions during persistence phase trap local emissions
- **Chain**: cold_surge_persistence → synoptic_stagnation → local_pollution_accumulation → pm25 (+40%)

### 3. Air Mass Trajectories
- **Quote**: "During regular winters, northeastern air masses predominated, which can bring pollution from eastern China and the industrial region surrounding Hanoi (Red River Delta)."
- **Mechanism**: HYSPLIT back-trajectory clustering shows NE air masses dominate
- **Source regions**: Eastern China, Red River Delta industrial region

### 4. Temporal Scope
- Winter period: October to March
- 10-15 cold surges per winter
- Study period: 2006-2020 (14 winters)

### 5. El Niño Effects
- El Niño perturbs air mass trajectories
- Brings more western air masses
- Causes temporary decrease of sulfate AOD, increase of smoke AOD

## Causal Chains Extracted

### Chain A: Cold Surge Onset → Regional Transport
1. cold_surge_onset → wind_direction_change (NE winds)
2. wind_direction_change → air_mass_trajectory_change (NE trajectories)
3. air_mass_trajectory_change → regional_transport (from E. China)
4. regional_transport → pm25 (+30%)

### Chain B: Cold Surge Persistence → Local Accumulation
1. cold_surge_persistence → synoptic_stagnation
2. synoptic_stagnation → reduced_dispersion
3. reduced_dispersion → local_pollution_accumulation
4. local_pollution_accumulation → pm25 (+40%)



---

# Paper 2: Aman et al. 2023 - Urban Haze and Cold Surge in Greater Bangkok

## Citation
- **Title**: A Study of Urban Haze and Its Association with Cold Surge and Sea Breeze for Greater Bangkok
- **Authors**: Nishit Aman, Kasemsan Manomaiphiboon, Natchanok Pala-En, Bikash Devkota, Muanfun Inerb, Eakkachai Kokkaew
- **Journal**: Int J Environ Res Public Health
- **Volume**: 20(4):3482
- **Year**: 2023
- **DOI**: 10.3390/ijerph20043482
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings for Cold Surge Mechanisms

### 1. Four Types of Haze Episodes Classification
- **Type I**: Cold surge alone → stagnant conditions → haze formation
- **Type II**: Sea breeze → local recirculation → pollutant accumulation
- **Type III**: Cold surge + Sea breeze synergetic effect (most persistent and polluted)
- **Type IV**: Neither cold surge nor sea breeze

### 2. Cold Surge Mechanism (Type I)
- **Quote**: "Type I is caused by the arrival of the cold surge in GBK, which leads to the development of stagnant conditions favorable for haze formation."
- **Mechanism**: Cold surge arrival → temperature decrease → stagnant conditions → reduced dispersion → haze formation
- **Conditions**: Coolest and driest weather conditions

### 3. Synergetic Effect (Type III)
- **Quote**: "Type III is the most persistent and most polluted haze type due to the synergetic effect of the cold surge and sea breeze"
- **Average duration**: 10.8 days (longest)
- **Mechanism**: Cold surge + sea breeze → combined stagnation and recirculation → highest PM2.5

### 4. Temporal Characteristics
- Winter period: December-February
- Episode duration: 1-14 days
- 38 haze episodes, 159 haze days identified (2017-2022)

### 5. Secondary Aerosol Formation
- 34% of episodes potentially affected by secondary aerosols
- Higher relative humidity during sea breeze episodes promotes secondary aerosol formation

## Causal Chains Extracted

### Chain C: Cold Surge → Stagnation → Haze (Type I)
1. cold_surge_arrival → temperature_decrease
2. temperature_decrease → synoptic_stagnation
3. synoptic_stagnation → reduced_dispersion
4. reduced_dispersion → pm25_increase (haze)

### Chain D: Cold Surge + Sea Breeze Synergy (Type III)
1. cold_surge → synoptic_stagnation
2. sea_breeze → local_recirculation
3. synoptic_stagnation + local_recirculation → combined_accumulation
4. combined_accumulation → pm25 (most severe)



---

# Paper 3: Ly et al. 2018 - Characterizing PM2.5 in Hanoi with High Temporal Resolution Sensor

## Citation
- **Title**: Characterizing PM2.5 in Hanoi with New High Temporal Resolution Sensor
- **Authors**: Bich-Thuy Ly, Yutaka Matsumi, Tomoki Nakayama, Yosuke Sakamoto, Yoshizumi Kajii, Trung-Dung Nghiem
- **Journal**: Aerosol and Air Quality Research
- **Volume**: 18: 2487-2497
- **Year**: 2018
- **DOI**: 10.4209/aaqr.2017.10.0435
- **Tier**: Tier-1 (Peer-reviewed journal)

## Key Findings (from abstract and visible content)

### 1. Seasonal Variation
- PM2.5 high during dry season (December median = 62 µg/m³)
- PM2.5 low during rainy season (June-July median = 19 µg/m³)
- Levels in December and January about 3 times higher than July

### 2. Cold Surge Episodes
- **Quote from abstract**: "The PM2.5 peak, which often appeared at night after a cold surge, may be the result of secondary particle formation under stagnant conditions."
- Episodes with PM2.5 > 100 µg/m³ observed 13 times during dry season (Oct 2016 - March 2017)
- Episodes linked to East Asian winter monsoon

### 3. Mechanism
- Cold surge → stagnant conditions → secondary particle formation → PM2.5 peak at night
- Daily levels of PM2.5 and CO increased several days after most cold surge events

### 4. Air Mass Origins (from Table 1)
- Air from mainland China (dry season): 49.5% of time
- Air from East Sea (rainy season): 44.3%
- Air from Indochina (transition period): 20.4%

## Causal Chains Extracted

### Chain E: Cold Surge → Secondary Formation → PM2.5 Peak
1. cold_surge_onset → stagnant_conditions
2. stagnant_conditions → secondary_particle_formation
3. secondary_particle_formation → pm25_peak (nighttime)



---

# Paper 4: Hien et al. 2011 - Air Pollution Episodes and East Asian Winter Monsoons

## Citation
- **Title**: Air pollution episodes associated with East Asian winter monsoons
- **Authors**: P.D. Hien, P.D. Loc, N.V. Dao
- **Journal**: Science of The Total Environment
- **Volume**: 409, Issue 23, Pages 5063-5068
- **Year**: 2011
- **DOI**: 10.1016/j.scitotenv.2011.08.049
- **Tier**: Tier-1 (Peer-reviewed journal)
- **Cited by**: 71

## Key Findings for Cold Surge Mechanisms

### 1. Winter Pollution Episodes (WPEs) Pattern
- **Quote**: "A dozen multi-day pollution episodes occur from October to February in Hanoi, Vietnam due to prolonged anticyclonic conditions established after the northeast monsoon surges (cold surges)."
- Episodes account for most 24-h PM10 exceedances

### 2. Monsoon Cycle Mechanism
- **Quote**: "The 24-h pollutant concentrations are lowest during cold surges; concurrently rise thereafter reaching the highest levels toward the middle of a monsoon cycle, then decline ahead of the next cold surge."
- Two phases: dry phase and humid phase
- Air arrives through inland China (dry) then via East China Sea (humid)

### 3. Temperature Inversion Types
- **Nighttime Radiation Temperature Inversions (NRTIs)**: Dry phase
  - Evening pollution peak more pronounced than morning
  - Pollution ~2x higher at night than daytime
- **Subsidence Temperature Inversions (STIs)**: Humid phase
  - Broad morning and evening traffic peaks
  - Pollution equally high at night and daytime

### 4. Temporal Pattern
- Monsoon cycle: ~4 days average (similar to Beijing)
- 16 northeast monsoon cycles in winter 2003-04
- Period: October to February

### 5. Air Mass Trajectories
- Continental cold air from Asiatic high-pressure anticyclone (Lake Baikal, Siberia)
- Northerly to northeasterly monsoons
- Not blocked by Himalayas due to location east of Tibetan plateau

## Causal Chains Extracted

### Chain F: Cold Surge → Anticyclonic Conditions → WPE
1. cold_surge → anticyclonic_conditions (prolonged)
2. anticyclonic_conditions → temperature_inversion (NRTI or STI)
3. temperature_inversion → reduced_vertical_mixing
4. reduced_vertical_mixing → pm10_accumulation (WPE)

### Chain G: Monsoon Cycle Evolution
1. cold_surge_onset → low_pollution (high winds, dispersion)
2. post_surge_period → anticyclonic_stagnation
3. anticyclonic_stagnation → pollution_rise
4. mid_cycle → peak_pollution
5. pre_next_surge → pollution_decline

### Chain H: Dry Phase vs Humid Phase
**Dry Phase (NRTI)**:
1. cold_air_via_inland_china → dry_conditions
2. dry_conditions → nighttime_radiation_inversion
3. nighttime_radiation_inversion → nighttime_pollution_peak

**Humid Phase (STI)**:
1. cold_air_via_east_china_sea → humid_conditions
2. humid_conditions → subsidence_inversion
3. subsidence_inversion → all_day_high_pollution



---

# Paper 5: Ngoc et al. 2021 - Key Factors Explaining Severe Air Pollution Episodes in Hanoi

## Citation
- **Title**: Key factors explaining severe air pollution episodes in Hanoi during 2019 winter season
- **Authors**: Bao Anh Phung Ngoc, Hervé Delbarre, Karine Deboudt, Elsa Dieudonné, Dien Nguyen Tran, Son Le Thanh, Jacques Pelon, François Ravetta
- **Journal**: Atmospheric Pollution Research
- **Volume**: 12(6), pp.101068
- **Year**: 2021
- **DOI**: 10.1016/j.apr.2021.101068
- **Tier**: Tier-1 (Peer-reviewed journal)
- **Cited by**: 24

## Key Findings (from visible abstract)

### 1. Campaign Details
- Two-month campaign: 11 January to 22 March 2019
- Impact of Northeast monsoon during winter period
- Doppler Lidar and elastic Lidar measurements used

### 2. Pollution Episodes
- Four heavily polluted events occurred during campaign
- Highest daily PM2.5: ~130 µg/m³
- Mean concentration: 45 ± 25 µg/m³

### 3. Sources of Pollution
- **Quote**: "These severe polluted events in Hanoi were mainly related to LRT coming from China besides local emission or LRT from other polluted regions of Vietnam."
- Long-range transport (LRT) from China is key factor
- Local emissions also contribute

### 4. Boundary Layer Height (BLH) Role
- **Quote**: "BLH proved to be one of the key factors controlling air pollution in Hanoi."
- Daily maximum BLH: 700m to 1200m during cloudy days
- BLH always below 1000m during hazy days
- Lower BLH → weakened vertical mixing → increased aerosol concentrations

### 5. Cold Surge Connection
- Cold surges in winter can affect PM2.5 concentrations in Hanoi
- 5 cold surges occurred during campaign period

## Causal Chains Extracted

### Chain I: Cold Surge → BLH → PM2.5
1. cold_surge → meteorological_conditions_change
2. meteorological_conditions_change → pblh_decrease (below 1000m)
3. pblh_decrease → reduced_vertical_mixing
4. reduced_vertical_mixing → pm25_increase

### Chain J: Long-Range Transport Chain
1. cold_surge_onset → northerly_wind_direction
2. northerly_wind_direction → long_range_transport (from China)
3. long_range_transport → regional_pollution_advection
4. regional_pollution_advection → pm25_increase



---

# Paper 6: Wang et al. 2017 - Large-scale Transport of PM2.5 During Winter Cold Surges in China

## Citation
- **Title**: Large-scale transport of PM2.5 in the lower troposphere during winter cold surges in China
- **Authors**: Jianjun Wang, Meigen Zhang, Xiaolin Bai, Hongjian Tan, Sabrina Li, Jiping Liu, Rui Zhang, Mark A. Wolters, Xiuyuan Qin, Miming Zhang, Hongmei Lin, Yuenan Li, Jonathan Li, Liqi Chen
- **Journal**: Scientific Reports
- **Volume**: 7, Article number: 13238
- **Year**: 2017
- **DOI**: 10.1038/s41598-017-13217-2
- **Tier**: Tier-1 (Peer-reviewed journal, Nature Publishing Group)
- **Cited by**: 72

## Key Findings

### 1. Transport Distance and Speed
- **Quote**: "PM2.5 driven by cold surges from the ground level could travel up to 2000 km from northern to southern China within two days."
- This is a NEW long-range transport mechanism (lower troposphere vs upper troposphere)

### 2. Cold Surge Mechanism
- **Quote**: "The most prominent surface feature of the winter monsoon is cold surges induced by strong northwesterly winds along the eastern flank of the Siberian high, leading in turn to rapid temperature falls in southern China."
- Siberian high → northwesterly winds → cold surge → PM2.5 transport

### 3. Case Study (February 2015)
- Two cold surges: Feb 3-6 and Feb 6-9, 2015
- PM2.5 in Xiamen increased to 80 µg/m³ (double the winter average)
- Transport path: Beijing → Shanghai → Xiamen

### 4. Wind Speed Role
- **Quote**: "Wind speed was found to be a major facilitator in transporting PM2.5 from Beijing to Xiamen"
- Maximum ground wind speeds over 20 m/s during cold surges
- High wind speed enables transport before deposition

### 5. Temporal Pattern
- Air pollution more severe in winter in north China
- Seasonal variations in energy usage, trade wind movements, industrial emissions

## Causal Chains Extracted

### Chain K: Cold Surge → Long-range Transport (Lower Troposphere)
1. siberian_high → northwesterly_winds (strong)
2. northwesterly_winds → cold_surge_onset
3. cold_surge_onset → high_wind_speed (>20 m/s)
4. high_wind_speed → pm25_transport (up to 2000 km in 2 days)
5. pm25_transport → pm25_increase_at_receptor

### Chain L: Cold Surge Transport vs Stagnation
**During Cold Surge (Transport Phase)**:
- High wind speed → rapid PM2.5 transport southward
- PM2.5 can travel 2000 km in 2 days

**After Cold Surge (Stagnation Phase)**:
- Wind speed decreases → stagnation
- Local accumulation dominates



---

# Paper 7: Ly et al. 2021 - Effects of Meteorological Conditions and Long-Range Transport on PM2.5 in Hanoi

## Citation
- **Title**: The effects of meteorological conditions and long-range transport on PM2.5 levels in Hanoi revealed from multi-site measurement using compact sensors and machine learning approach
- **Authors**: Bich-Thuy Ly, Yutaka Matsumi, Tuan V. Vu, Kazuhiko Sekiguchi, Thu-Thuy Nguyen, Chau-Thuy Pham, Trung-Dung Nghiem, Ich-Hung Ngo, Yuta Kurotsuchi, Thu-Hien Nguyen, Tomoki Nakayama
- **Journal**: Journal of Aerosol Science
- **Volume**: 152, 105716
- **Year**: 2021
- **DOI**: 10.1016/j.jaerosci.2020.105716
- **Tier**: Tier-1 (Peer-reviewed journal)
- **Cited by**: 41

## Key Findings

### 1. Regional Effects
- **Quote**: "Hourly concentrations of PM2.5 at the three sites were similar on average (57.5, 54.9, and 53.6 μg m−3) and clearly co-varied, suggesting remarkable large-scale effects."
- Multi-site measurement confirms regional-scale pollution patterns

### 2. Long-Range Transport
- **Quote**: "The contribution of long-range transport from the north and northeast to local PM2.5 levels was significant."
- CWT (Concentration Weighted Trajectory) analysis used
- Air mass backward trajectory modeling confirms transport pathways

### 3. Cold Surge Effects
- **Quote**: "It has been found that air pollutant levels increased over the couple of days that followed a cold surge (Hien et al., 2011; Ly et al., 2018)."
- Post-cold surge period shows elevated PM2.5

### 4. Meteorological Factors
- **Quote**: "Meteorological conditions play a significant role in the formation of winter haze events."
- Weather normalized PM2.5 used to separate meteorological effects
- Random forest (RF) algorithm applied for analysis

### 5. Winter Haze Formation
- **Quote**: "Stagnant meteorological conditions limited wet removal and more biomass open burning occurring around the city during winters are some of the most important reasons for the high build-up of PM pollution in Hanoi."
- Northeast Monsoon brings pollutants from Northern Vietnam and China

## Causal Chains Extracted

### Chain M: Regional Transport Pattern
1. northeast_monsoon → northerly_airflow
2. northerly_airflow → long_range_transport (from north/northeast)
3. long_range_transport → regional_pm25_increase
4. regional_pm25_increase → co-variation_across_sites (Hanoi + Thai Nguyen)

### Chain N: Post-Cold Surge Accumulation
1. cold_surge_passage → post_surge_conditions
2. post_surge_conditions → stagnant_meteorology
3. stagnant_meteorology → limited_wet_removal
4. limited_wet_removal → pm25_accumulation (couple of days after surge)

