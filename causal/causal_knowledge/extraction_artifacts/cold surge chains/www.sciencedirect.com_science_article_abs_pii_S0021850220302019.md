# The effects of meteorological conditions and long-range transport on PM2.5 levels in Hanoi revealed from multi-site measurement using compact sensors and machine learning approach - ScienceDirect

**URL:** https://www.sciencedirect.com/science/article/abs/pii/S0021850220302019

---

Skip to main content
Skip to article
Journals & Books
Help
Search
My account
Sign in
Access through your organization
Purchase PDF
Article preview
Abstract
Introduction
Section snippets
References (42)
Cited by (41)
Journal of Aerosol Science
Volume 152, February 2021, 105716
The effects of meteorological conditions and long-range transport on PM2.5 levels in Hanoi revealed from multi-site measurement using compact sensors and machine learning approach
Author links open overlay panel
Bich-Thuy Ly a
, Yutaka Matsumi b
, 
Tuan V. Vu c
, Kazuhiko Sekiguchi d, 
Thu-Thuy Nguyen e f
, 
Chau-Thuy Pham g
, 
Trung-Dung Nghiem a
, 
Ich-Hung Ngo a
, 
Yuta Kurotsuchi d
, 
Thu-Hien Nguyen a
, Tomoki Nakayama h
Show more
Add to Mendeley
Share
Cite
https://doi.org/10.1016/j.jaerosci.2020.105716
Get rights and content
Highlights
•
Observation of PM2.5 levels at three sites using sensors.
•
Moderate to good correlation factors among PM2.5 at sites showed regional effects.
•
Partial effects of meteorological and temporal factors on PM2.5 were determined by a machine learning approach.
•
Contribution of meteorological factors on haze revealed by weather normalized PM2.5
•
PM2.5 long-range transport investigated by CWT and partial trajectory correlation.
Abstract
Hanoi, the capital of Vietnam, frequently experiences heavy air pollution episodes in the winter, causing health concerns for the 7.5 million people living there. Spatial-temporal variations in PM2.5 levels can provide useful information about the sources and transportation of PM2.5. However, the published spatial-temporal data in the area are limited. In this research, PM2.5 concentrations at two sites in Hanoi and a site in Thai Nguyen (60 km north of Hanoi) were observed from October 2017 to April 2018, using newly available low-cost sensors. Hourly concentrations of PM2.5 at the three sites were similar on average (57.5, 54.9, and 53.6 μg m−3) and clearly co-varied, suggesting remarkable large-scale effects. The contribution of long-range transport and meteorological factors on PM2.5 levels were investigated with a machine learning technique based on a random forest (RF) algorithm and concentration weight trajectory (CWT). The results showed that the contribution of long-range transport from the north and northeast to local PM2.5 levels was significant. Moreover, weather normalized PM2.5 concentrations and partial plots of meteorological factors on the levels of PM2.5 showed that meteorological conditions play a significant role in the formation of winter haze events.
Graphical abstract
Download: Download high-res image (499KB)
Download: Download full-size image
Introduction
Particulate matter (PM), especially PM2.5, is a serious air pollution problem for the world as well as for Asia. In 2016, 2.2 million premature deaths in the Asia Pacific (the WHO Western Pacific) Region were attributed to air pollution (WHO, 2018). Several efforts have been made to reduce air pollution impacts in Asia.
The low-cost sensor is a tool that can supplement standard monitoring equipment, and it comes with several advantages. Sensors can be used to form a high-density network at reasonable cost. For example, the Aircasting project used AirBEAM instrument to map real-time PM2.5 (European Commission, 2015), or a research used both simulated datasets and a low-cost sensor network to map NO2 in Oslo, Norway (Schneider et al., 2017). Low-cost sensors can be useful for assessing personal exposure because their relatively small size, lightness, and low energy consumption that make them convenient for carriers. Cao and Thompson (2016) used portable, low-cost O3 sensors for personal exposure monitoring in Texas. Jerrett et al. (2017) used low-cost sensors of CO, NO, and NO2 for personal exposure monitoring in Spain. Steinle et al. (2015) used Dylos1700 to assess personal daily exposure to short-term PM2.5 concentrations. Low-cost sensors are also useful for mobile monitoring. The HazeWatch project attached several low-cost sensors to vehicles to measure air pollution in transportation in Sydney (Sivaraman et al., 2013). Hasenfratz et al. (2015) developed land-use regression models to create pollution maps using data collected from sensors fixed to the roofs of public transport vehicles in Zurich. In Vietnam, the application of low-cost sensors in determining of the concentration characteristics of PM2.5 in an urban site in Hanoi was carried out in the research of Ly et al. (2018).
In 2018, the Red River delta had a population of nearly 21.6 million people (GSO, 2018). Hanoi, the capital city of Vietnam, is located in the Red River delta and the city had a population of more than 7.5 million people in 2018 (GSO, 2018). Fewer than a dozen studies have investigated PM2.5 characteristics in Hanoi (Nguyen et al., 2018 and references therein), and fewer still have examined PM2.5 levels in areas other than Hanoi (Nguyen et al., 2018 and the references therein). Just one study has examined multi-site levels of PM2.5 in Hanoi and other provinces (Hien et al., 2005). This scarcity of research limits our understanding of PM2.5 transportation in the area. This study aims to partly fill this gap through the use of low-cost sensors.
An area's air pollutant levels are generally affected by local sources, meteorological conditions, and regional transportation. For particulate matter, secondary aerosol formation also contributes to the levels. The contributions of local sources to PM2.5 levels in Hanoi have been determined in previous works (Cohen et al., 2010a; Hai & Kim Oanh, 2013; Hien et al., 2004; Hopke et al., 2008; Kim Oanh et al., 2006). The effects of meteorological factors and regional transport on PM2.5 levels in Hanoi have been also investigated in previous research (Cohen et al., 2010a; Hai & Kim Oanh, 2013; Hien et al., 2011; Kim Oanh et al., 2006; Ly et al., 2019). The contribution of long-range transport of PM2.5 to Hanoi has been determined in the research of Hai and Kim Oanh (2013), Hien et al., 2004 and Cohen et al. (2010b) through the application of air mass backward trajectory. It has been found that air pollutant levels increased over the couple of days that followed a cold surge (Hien et al., 2011; Ly et al., 2018). Regression analysis showing the statistically significant effects of meteorological factors on PM2.5 levels were done by Ly et al. (2019) and Hien et al. (2002). The combined effects of different meteorological factors and regional transportation on PM2.5 levels hinder the determination of the effect of each meteorological factor and long-range transport alone on PM2.5 levels. While the effects of each contribution source and affected factor can be determined by dispersion models, the gap in emission inventory data in developing countries including Vietnam, hinders the application of such models. However, statistical methods offer another potential approach to determining the separate effects of individual sources and affected factors.
During the last three decades, several predictive models in the field of machine learning (ML) have been developed to complement statistical model for air quality trend analysis (Grange et al., 2018). Random forest (RF) is an ensemble decision-tree ML method. Decision trees use a binary recursive classifying algorithm that creates “pure” nodes by splitting observations into two homologous groups. The decision tree can grow very deep and can rarely be generalized to new data that was not used to train the model. RF controls for this disadvantage by aggregating several trees from the training data set with bagging methods. Bagging refers to randomly selected training data points that can be re-inserted into the selected data set. This allows RF to produce predictive models that have the capacity to generalize well while offering a similar standard of performance to the best ML techniques (Caruana & Niculescu-Mizil, 2006). Furthermore, RF models can be investigated with partial dependence plots that demonstrate the relationships among variables (Grange et al., 2018). There are several studies that apply decision-tree or RF models to predict the levels of air pollutants in different conditions, and or use them to identify the trend of air pollutants after removing the impact of weather (Carslaw & Taylor, 2009; Grange et al., 2018; Vu et al., 2019; Zhang et al., 2020).
A concentration weighted trajectory (CWT) is a trajectory statistical method, in which air mass backward trajectory modelling is used in combination with the atmospheric concentration at the receptor site (Squizzato & Masio, 2015 and references therein). In the CWT model, trajectories are weighted with their associated concentrations to determine the most probable source areas of long-range transports of the pollutants of interest. The average concentration-weighted residential time (passing time) at each grid is divided by the residential time of all trajectories to determine the “concentration weighted trajectory” of that grid (Hsu et al., 2003). The areas of high concentration weighted trajectory highlight the relative significance of potential sources (Hsu et al., 2003).
In this research, the RF model simulates the data set of PM2.5 in accordance with the meteorological and temporal parameters that were first determined. The effects of meteorological factors were investigated through partial plots and weather normalized PM2.5. The effects of long-range transport of PM2.5 was investigated by determining the partial effects of backward trajectory clusters on PM2.5 and CWT analysis. The combination of these methods to determine the separate effects of meteorological and long-range transport on air pollutants can be applied for other parameters as well as for other areas in the region.
This research aims to i) use sensor to determine the levels, and trends of PM2.5 at sites in Hanoi and Thai Nguyen; ii) evaluate the influence of meteorological factors on PM2.5 levels; iii) determine the effects of long-range transports on PM2.5 concentrations via CWT modeling and the partial dependence plot of trajectory clusters on PM2.5 concentrations; iv) determine the trend of PM2.5 without a weather effect by calculating the weather normalized concentrations.
Access through your organization

Check access to the full text by signing in through your organization.

Access through your organization
Section snippets
Description about monitoring sites
The monitoring was conducted at three sites, as presented in Table S1 and Fig. 1.
The first site (named HN–U) is located in HUST. The data of PM2.5 and other air pollutants at the site and information of HUST site were published elsewhere (Sakamoto et al., 2018; Ly et al., 2018). In brief, this site is located in the core area of Hanoi with high residential density. Two Panasonic PM2.5 sensors were co-measured outside the third floor of a four-story building. The site is located at least 100 m
Characteristics of observed PM2.5 levels at three sites
The hourly variations of PM2.5 at the three sites are presented in Fig. 2. The hourly medians of the urban (HN–U) and suburban sites (HN-PU) in Hanoi were 47.5 and 46.1 μg m−3 (average of 57.5 and 54.9 μg m−3). The hourly median of the site in Thai Nguyen (TN) was similar, at 46.9 μg m−3 (average of 53.6 μg m−3). The levels of PM2.5 at the sites in Hanoi were comparable to the data in the previous research of Ly et al., 2018. There were no published data about PM2.5 in Thai Nguyen. Even though
Conclusions
In this study, PM2.5 concentrations at two sites in Hanoi and a site in Thai Nguyen were observed from October 2017 to April 2018 using Panasonic sensors. The resulting data were then analyzed with a machine learning approach. The main conclusions are as follows:
1.
Data obtained by multisite measurement demonstrated a regional effect on PM2.5 levels in the area. The hourly average concentrations of PM2.5 at the three sites were similar (53.6, 57.5, 54.9 μg m−3). However, the number of haze
Declaration of competing interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
Acknowledgements
We would like to thank Life Solutions Company, Panasonic Corporation for providing the PM2.5 sensors. We would like to thank Wataru Okamoto and Takayuki Yamasaki in Nagoya University and Nguyen Minh Thang for their technical supports. We would like to thank Nguyen Anh Tuan for his English support. This work is funded by Vietnam National Foundation for Science and Technology Development (NAFOSTED) under grant number 105.99–2019.322 and received support from JSPS KAKENHI Grant number JP17H04483.
References (42)
T. Cao et al.
Personal monitoring of ozone exposure: A fully portable device for under 150 USD cost
Sens. Actuators B-Chem.
(2016)
G.R. Carmichael et al.
Seasonal variation of aerosol composition at cheju island, Korea
Atmospheric Environment
(1996)
D.C. Carslaw et al.
Openair — an R package for air quality data analysis
Environmental Modelling & Software
(2012)
D.C. Carslaw et al.
Analysis of air pollution data at a mixed source location using boosted regression trees
Atmospheric Environment
(2009)
D.D. Cohen et al.
Characterisation and source apportionment of fine particulate sources at Hanoi from 2001 to 2008
Atmospheric Environment
(2010)
D.D. Cohen et al.
Long range transport of fine particle windblown soils and coal fired power station emission into Hanoi between 2001 to 2008
Atmospheric Environment
(2010)
M.J. Gatari et al.
Assessment of inorganic content of PM2.5 particles sampled in a rural area north-east of Hanoi
Vietnam. Sci. Total Environ.
(2006)
D. Hasenfratz et al.
Deriving high-resolution urban air pollution maps using mobile sensor nodes
Pervasive and Mobile Computing
(2015)
P.D. Hien et al.
Influence of meteorological conditions on PM2.5 and PM2.5-10 concentrations during the monsoon season in Hanoi
Vietnam. Atmos. Environ.
(2002)
P.D. Hien et al.
PMF receptor modelling of fine and coarse PM10 in air masses governing monsoon conditions in Hanoi, northern Vietnam
Atmospheric Environment
(2004)
View more references
Cited by (41)
A comprehensive review on advancements in sensors for air pollution applications
2024, Science of the Total Environment
Show abstract
Particulate pollution and its toxicity to fish: An overview
2023, Comparative Biochemistry and Physiology Part C Toxicology and Pharmacology
Show abstract
Chemical composition and potential sources of PM2.5 in Hanoi
2023, Atmospheric Environment
Citation Excerpt :

Stagnant meteorological conditions limited wet removal and more biomass open burning occurring around the city during winters are some of the most important reasons for the high build-up of PM pollution in Hanoi (Kim Oanh, 2021; Hai and Kim Oanh, 2013). Regionally, the potential long-range transportation from Northern Vietnam and China associated with the Northeast Monsoon (Ly et al., 2021; Cohen et al., 2010a, 2010b) also contribute to the high pollution levels during winter. Increased concentrations of air pollutants during winter are found to increase the number of hospital visits due to acute respiratory and cardiovascular diseases (Trinh et al., 2019).

Show abstract
Regional division and influencing mechanisms for the collaborative control of PM2.5 and O3 in China: A joint application of multiple mathematic models and data mining technologies
2022, Journal of Cleaner Production
Show abstract
Influencing factors of PM2.5 and O3 from 2016 to 2020 based on DLNM and WRF-CMAQ
2021, Environmental Pollution
Show abstract
Clarifying Relationship between PM2.5 Concentrations and Spatiotemporal Predictors Using Multi-Way Partial Dependence Plots
2023, Remote Sensing
View all citing articles on Scopus
View full text
© 2020 Elsevier Ltd. All rights reserved.
Part of special issue
Special Section on Low Cost Sensors
Edited by Kerry Kelly
View special issue
(Content truncated due to size limit. Use line ranges to read remaining content)