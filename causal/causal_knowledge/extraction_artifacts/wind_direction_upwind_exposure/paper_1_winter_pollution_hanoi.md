# Paper 1: Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period

## Thông tin nguồn
- **Title**: Intricate behavior of winter pollution in Hanoi over the 2006–2020 semi-climatic period
- **Authors**: Bao-Anh Phung-Ngoc, Elsa Dieudonné, Hervé Delbarre, Karine Deboudt, Song-Tung Nguyen, Van-Hai Bui, Duc-Minh Vu, Huyen-Thu Nguyen-Thi
- **Journal**: Atmospheric Environment
- **Year**: 2023
- **DOI**: https://doi.org/10.1016/j.atmosenv.2023.119669
- **Tier**: Tier 1 (Peer-reviewed, Atmospheric Environment)

## Key Findings về Wind Direction và PM2.5

### 1. Northeast Monsoon và Air Mass Transport
- **Mechanism**: Trong mùa đông (tháng 10 - tháng 3), chất lượng không khí ở miền Bắc Việt Nam bị ảnh hưởng mạnh bởi các chu kỳ gió mùa Đông Bắc, tạo ra những thay đổi định kỳ trong đường đi của khối không khí và điều kiện khí tượng.
- **Quote**: "During the winter period (October to March), air quality in northern Vietnam is strongly impacted by the northeast monsoon cycles, that create periodic changes in the air masses pathways and the meteorological conditions."

### 2. HYSPLIT Back-trajectory Analysis
- **Phương pháp**: Sử dụng HYSPLIT back-trajectories với clustering qua 14 mùa đông
- **Kết quả**: 
  - Trong các mùa đông bình thường, khối không khí từ hướng Đông Bắc chiếm ưu thế, có thể mang ô nhiễm từ miền Đông Trung Quốc và vùng công nghiệp xung quanh Hà Nội (Đồng bằng sông Hồng)
  - **Quote**: "During regular winters, northeastern air masses predominated, which can bring pollution from eastern China and the industrial region surrounding Hanoi (Red River Delta)."

### 3. Cold Surge Impact
- **Mechanism**: Long-range transport từ Trung Quốc trong giai đoạn onset của cold surges gây tăng trung bình khoảng 30% nồng độ PM2.5 tại Hà Nội
- **Quote**: "This classification allowed to estimate that long-range transport from China during the onset of cold surges caused an average increase of around 30% of the PM2.5 level in Hanoi."

### 4. El Niño Effect
- **Mechanism**: El Niño làm xáo trộn quỹ đạo khối không khí trong 3 mùa đông (2014/15, 2015/16, 2018/19), mang nhiều khối không khí từ hướng Tây hơn, gây giảm sulfate AOD và tăng smoke AOD
- **Quote**: "However, the existence of El Niño perturbed the air masses trajectories during three winters (2014/15, 2015/16 and 2018/19), bringing more western air masses and thus, causing a temporary decrease of the sulfate AOD and simultaneous increase of the smoke AOD over Hanoi."

### 5. Source Shift (2006-2020)
- **2006/07 - 2010/11**: Pollution plumes chủ yếu ở bán đảo Đông Dương, do biomass burning
- **2011/12 - 2019/20**: Pollution plumes chủ yếu ở miền Đông Trung Quốc và miền Bắc Việt Nam, do hoạt động công nghiệp sử dụng than

## Relationships có thể extract

1. **wind_direction_sector (NE) → upwind_emission_exposure**
   - Conditions: Winter monsoon, regular winters
   - Mechanism: NE air masses pass through industrial regions in eastern China and RRD

2. **cold_surge → pm25** (increase ~30%)
   - Mechanism: Long-range transport from China during cold surge onset

3. **upwind_emission_exposure → pm25**
   - Mechanism: Regional transport from industrial zones and TPPs in RRD

4. **el_nino → wind_direction_sector** (shift to westerly)
   - Effect: Reduces sulfate, increases smoke AOD


---

# Paper 2: Effects of local, regional meteorology and emission sources on mass and compositions of particulate matter in Hanoi

## Thông tin nguồn
- **Title**: Effects of local, regional meteorology and emission sources on mass and compositions of particulate matter in Hanoi
- **Authors**: Cao Dung Hai, Nguyen Thi Kim Oanh
- **Journal**: Atmospheric Environment
- **Year**: 2013
- **Volume**: 78, Pages 105-112
- **DOI**: https://doi.org/10.1016/j.atmosenv.2012.05.006
- **Tier**: Tier 1 (Peer-reviewed, Atmospheric Environment)

## Key Findings về Wind Direction và PM2.5

### 1. Wind Speed và Direction Link với PM2.5
- **Quote**: "The daily PM2.5 levels were found to closely link to local wind speeds and directions (relative to local emission sources) and regional synoptic meteorology suggesting that both local sources and LRT contributed to the high PM levels at the site."
- **Mechanism**: PM2.5 hàng ngày liên quan chặt chẽ với tốc độ và hướng gió địa phương (tương đối với nguồn phát thải địa phương) và khí tượng synoptic khu vực

### 2. Stagnating Ridge và High PM
- **Quote**: "High 24 h PM levels were observed at low wind speeds when a stagnating ridge governed over Northern Vietnam."
- **Mechanism**: Nồng độ PM cao khi tốc độ gió thấp và có dải áp cao đứng yên bao phủ miền Bắc Việt Nam

### 3. PMF Source Apportionment
- Secondary mixed PM: 40%
- Diesel traffic: 10%
- Residential/commercial cooking: 16%
- Secondary sulfate rich: 16%
- Aged seasalt mixed: 11%
- Industry/incinerator: 6%
- Construction/soil: 1%

### 4. Long-Range Transport
- **Quote**: "Contributions from local emission sources and the potential long-range transport were analyzed using the PM compositions and the diurnal variations in relation to local source activities, location of local sources, winds and air mass HYSPLIT trajectories."
- **Method**: Sử dụng HYSPLIT trajectories để phân tích đóng góp từ LRT

## Relationships có thể extract

1. **wind_direction + wind_speed → pm25**
   - Conditions: Low wind speed, stagnating ridge over Northern Vietnam
   - Mechanism: Local sources + LRT contribution

2. **regional_synoptic_meteorology → pm25**
   - Mechanism: Stagnating ridge governance leads to high PM accumulation


---

# Paper 3: The effects of meteorological conditions and long-range transport on PM2.5 levels in Hanoi (Ly et al. 2021)

## Thông tin nguồn
- **Title**: The effects of meteorological conditions and long-range transport on PM2.5 levels in Hanoi revealed from multi-site measurement using compact sensors and machine learning approach
- **Authors**: Bich-Thuy Ly, Yutaka Matsumi, Tuan V. Vu, et al.
- **Journal**: Journal of Aerosol Science
- **Year**: 2021
- **Volume**: 152, 105716
- **DOI**: https://doi.org/10.1016/j.jaerosci.2020.105716
- **Tier**: Tier 1 (Peer-reviewed)

## Key Findings về Wind Direction và Long-Range Transport

### 1. Long-Range Transport from North and Northeast
- **Quote**: "The results showed that the contribution of long-range transport from the north and northeast to local PM2.5 levels was significant."
- **Method**: Random Forest (RF) algorithm và Concentration Weight Trajectory (CWT)

### 2. Cold Surge Impact
- **Quote**: "It has been found that air pollutant levels increased over the couple of days that followed a cold surge"
- **Reference**: Hien et al., 2011; Ly et al., 2018

### 3. Regional Effect
- **Quote**: "Hourly concentrations of PM2.5 at the three sites were similar on average (57.5, 54.9, and 53.6 μg m−3) and clearly co-varied, suggesting remarkable large-scale effects."

---

# Paper 4: Analysis of air pollution over Hanoi, Vietnam using multi-satellite and MERRA reanalysis datasets (Lasko et al. 2018)

## Thông tin nguồn
- **Title**: Analysis of air pollution over Hanoi, Vietnam using multi-satellite and MERRA reanalysis datasets
- **Authors**: Kristofer Lasko, Krishna Prasad Vadrevu, Thanh Thi Nhat Nguyen
- **Journal**: PLOS ONE
- **Year**: 2018
- **DOI**: https://doi.org/10.1371/journal.pone.0196629
- **Tier**: Tier 1 (Peer-reviewed, Open Access)

## Key Findings về Wind Direction và Transport

### 1. Wind Direction Patterns và BC Transport
- **Quote**: "Transport of polluted air into Hanoi becomes apparent from monthly averaged wind direction and speed patterns... General synoptic meteorology patterns indicate northerly winds flowing from South China into Northern Vietnam and Hanoi during October–March, whereas during Apr-Aug more south or southeasterly winds from Laos, Southern Vietnam, and the South China Sea."
- **Mechanism**: Gió mùa Đông Bắc (Oct-Mar) mang ô nhiễm từ Nam Trung Quốc; Gió Đông Nam (Apr-Aug) mang ô nhiễm từ Lào và Nam Việt Nam

### 2. Biomass Burning Transport
- **Quote**: "During March and April, high BC values over Laos and Northwest province of Vietnam are attributed especially to forest fires and slash and burn agriculture."
- **Mechanism**: Đốt sinh khối từ Lào và Tây Bắc Việt Nam ảnh hưởng chất lượng không khí Hà Nội vào tháng 3-4

### 3. Southern China Industrial Transport
- **Quote**: "Relatively high BC levels throughout all months are consistently observed from Southern China largely originating from the mega-urban Chengdu and Chongqing cities"
- **Quote**: "During the peak BC months of December and January, wind patterns indicated pollutant transport from southern China megacity areas."

### 4. Seasonal Wind Direction Summary
| Season | Wind Direction | Source Region | Pollutant Type |
|--------|---------------|---------------|----------------|
| Oct-Mar | Northerly (NE monsoon) | South China | Industrial, urban |
| Mar-Apr | Variable | Laos, NW Vietnam | Biomass burning |
| Apr-Aug | South/Southeast | Laos, South Vietnam, South China Sea | Mixed |

### 5. Back-trajectory Findings
- **Quote**: "Trajectory patterns suggested relatively more polluted air parcels moving into Hanoi City originate from the North, while more originate from the South during..."


---

# Paper 5: Seasonal Characteristics of Atmospheric PM2.5 in an Urban Area of Vietnam and the Influence of Regional Fire Activities (Bui et al. 2022)

## Thông tin nguồn
- **Title**: Seasonal Characteristics of Atmospheric PM2.5 in an Urban Area of Vietnam and the Influence of Regional Fire Activities
- **Authors**: Quang Trung Bui, Duc Luong Nguyen, Thi Hieu Bui
- **Journal**: Atmosphere (MDPI)
- **Year**: 2022
- **Volume**: 13(11), 1911
- **DOI**: https://doi.org/10.3390/atmos13111911
- **Tier**: Tier 1 (Peer-reviewed)

## Key Findings về Wind Direction và PM2.5

### 1. Seasonal Wind Direction và PM2.5
- **Quote**: "With the predominance of north and northeast winds during the winter period, the long-range transport of air pollutants which emitted from the highly industrialized areas and the intensive fire regions in the southern part of China and Southeast Asia region were likely other important sources for the highly elevated concentrations of PM2.5 and its chemical species in the study area."

### 2. Back-trajectory Analysis
- **Quote**: "air masses mainly originating from the north and northeast directions travelled through the Pearl River Delta region in the southern part of China (a highly industrialized area) before arriving at the measurement site during the winter period."
- **Summer**: Air masses từ south, southwest, southeast - qua continental (Việt Nam, Lào, Thái Lan) và maritime (Biển Đông)
- **Winter**: Air masses từ north và northeast - qua Pearl River Delta (vùng công nghiệp hóa cao)

### 3. Fire Activities và Long-Range Transport
- **Quote**: "The MODIS fire maps showed that fire sources occurring in the southern part of China and the Southeast Asia region (Vietnam, Laos, Thailand, and Myanmar) during the winter period were much more intensive than those during the summer period."
- **Quote**: "As air masses traveled across the highly industrialized and intensive fire regions during the winter period, they might have carried a large amount of air pollutants, released from those regional sources, to the study area"

### 4. Wind Direction và Chemical Species
- **Summer**: Southeast wind dominant → highest concentrations of Cl−, NO3−, Na+, K+, Ca2+, EC
- **Winter**: North/Northeast winds dominant → high concentrations of Cl−, NH4+, Ca2+ (north wind); K+ diverse sources (southeast, north, northeast, east)

### 5. Wind Speed Impact
- **Quote**: "the moderate to strong negative correlations between wind speed and PM2.5 as well as most of PM2.5 chemical species were generally observed for both the summer and winter periods"
- **Quote**: "the lower values of wind speed and boundary layer height during the winter period were favorable for the trapping of air pollutants in the ground"
