
**URL:** https://www.mdpi.com/2072-4292/14/14/3333

---

You are currently on the new version of our website. Access the old version here.
Close
Journals
All Journals
Journal Finder
Proceedings Series
Propose a Journal
Topics
By Subjects
Biology & Life Sciences
Business & Economics
Chemistry & Materials
Computer Science & Mathematics
Engineering
Environmental & Earth Sciences
Medicine & Pharmacology
Physical Sciences
Public Health & Healthcare
Social Sciences, Arts & Humanities
Our Topics
All Topics
About Topics
Topics Awards
Subject Editors
Propose a Topic
Author Services
Information
Publishing
Open Access Policy
Editorial Process
Publication Ethics
Special Issues Guidelines
Article Processing Charge
Publishing Services
Guidelines
For Authors
For Reviewers
For Editors
For Librarians
Partnerships
Societies
Conferences
Institutional Open
Access Program
About
Company
About Us
Mission
Impact
History
Leadership
Office Locations
Awards
Careers
Products
Media
News
Blog
Contact
Support
Send Feedback
Search
Search
Sign in
Submit
Home
Journals
Remote Sensing
Volume 14, Issue 14
10.3390/rs14143333
Remote Sensing
Cite
Share
Download PDF
More formats
Abstract
Introduction
Data and Methods
Results and Discussion
Conclusions
Supplementary Materials
Author Contributions
Funding
Data Availability Statement
Acknowledgments
Conflicts of Interest
References
Article Metrics
Article

10 July 2022

Effect of Vertical Wind Shear on PM2.5 Changes over a Receptor Region in Central China
Xiaoyun Sun1
, 
Yue Zhou2,*
, 
Tianliang Zhao1
, 
Yongqing Bai2
, 
Tao Huo2,3
, 
Liang Leng2
, 
Huan He2,4
 and 
Jing Sun2
1
Collaborative Innovation Center on Forecast and Evaluation of Meteorological Disasters, Key Laboratory for Aerosol-Cloud-Precipitation of China Meteorological Administration, Nanjing University of Information Science and Technology, Nanjing 210044, China
2
Institute of Heavy Rain, China Meteorological Administration, Wuhan 430205, China
3
Changsha Meteorological Bureau, Changsha 410205, China
4
Jingmen Meteorological Bureau, Jingmen 448000, China
Show more
Remote Sens.
2022, 14(14), 3333;
https://doi.org/10.3390/rs14143333
This article belongs to the Section Atmospheric Remote Sensing
Version Notes
Order Reprints
Review Reports
Abstract
Vertical wind shear (VWS) significantly impacts the vertical mixing of air pollutants and leads to changes in near-surface air pollutants. We focused on Changsha (CS) and Jingmen (JM), the upstream and downstream urban sites of a receptor region in central China, to explore the impact of VWS on surface PM2.5 changes using 5-year wintertime observations and simulations from 2016–2020. The surface PM2.5 concentration was lower in CS with higher anthropogenic PM2.5 emissions than in JM, and the correlation between wind speed and PM2.5 was negative for clean conditions and positive for polluted conditions in both two sites. The difference in the correlation pattern of surface PM2.5 and VWS between CS and JM might be due to the different influences of regional PM2.5 transport and boundary layer dynamics. In downstream CS, the weak wind and VWS in the height of 1–2 km stabilized the ABL under polluted conditions, and strong northerly wind accompanied by enhanced VWS above 2 km favored the long-range transport of air pollutants. In upstream JM, local circulation and long-range PM2.5 transport co-determined the positive correlation between VWS and PM2.5 concentrations. Prevailed northerly wind disrupted the local circulation and enhanced the surface PM2.5 concentrations under polluted conditions, which tend to be an indicator of regional transport of air pollutants. The potential contribution source maps calculated from WRF-FLEXPART simulations also confirmed the more significant contribution of regional PM2.5 transport to the PM2.5 pollution in upstream region JM. By comparing the vertical profiles of meteorological parameters for typical transport- and local-type pollution days, the northerly wind prevailed throughout the ABL with stronger wind speed and VWS in transport-type pollution days, favoring the vertical mixing of transported air pollutants, in sharp contrast to the weak wind conditions in local-type pollution days. This study provided the evidence that PM2.5 pollution in the Twain-Hu Basin was affected by long-distance transport with different features at upstream and downstream sites, improving the understanding of the air pollutant source–receptor relationship in air quality changes with regional transport of air pollutants.
Keywords: regional transport; radar wind profiler; vertical wind shear
Graphical Abstract
1. Introduction
Air pollution with high PM2.5 concentrations in the ambient atmosphere has been a crucial problem in environmental science [1,2], with adverse influences on climate change and human health [3,4]. The PM2.5 variations, causes, and impacts have been intensively studied over recent decades [5].
PM2.5 changes are co-determined by anthropogenic emissions and meteorological conditions [6,7]. In response to the severe air pollution, the Chinese government issued the Action Plan on Prevention and Control of Air Pollution in 2013, imposing emission control on industry production, vehicles, and energy consumption [5,8,9]. The meteorological conditions significantly influence the formation and evolution of air pollution and offset the emission reduction efforts in some years [10,11,12]. Local accumulation, chemical transformation, and long-range transport are key factors of air pollution [13,14]. The stagnant meteorological conditions, such as low atmospheric boundary layer (ABL) height, strong temperature inversion, weak near-surface wind, and high relative humidity, are unfavorable for the dispersion of air pollutants [14,15]. The formation of secondary aerosols and aerosol–ABL interactions play vital roles in the explosion of air pollution under stagnant weather conditions and weakening monsoons [16,17,18,19,20]. In addition, the regional transport of air pollutants is a remarkable contributor to regional air pollution events [10,21,22]. However, it is difficult to figure out the associations between vertical wind structures in ABL and PM2.5 concentrations due to the lack of credible observations in local wind profiles.
Radar wind profilers (RWPs), generally Doppler radar, have been widely applied to monitor the vertical structures of meteorology with high temporal–spatial resolutions, especially in ABL [23,24,25]. Ground-based RWP can remotely monitor vertical and horizontal winds as well as mix processes to identify the meteorological conditions in the lower troposphere and explore the dynamic features of ABL [26,27,28]. Furthermore, synchronous observations and model simulations are the most common methods to analyze ABL structures, revealing the vital role of vertical wind changes in modulating air pollution [29,30]. To date, a large number of field campaigns involving the wind profiles observed using RWP have been conducted, especially over megacities, and the archived dataset has received increasing attention [28,31,32,33].
Air pollution in the Twain-Hu Basin (THB), featuring the lower plain in Hubei and Hunan provinces over central China, has become a heavy pollution center in recent years [34,35,36]. THB is located in the downwind areas of heavy air pollution in north and east China, serving as a key receptor region in the regional transport of air pollutants from upstream regions driven by East Asian monsoonal winds [34,37]. Heavy air pollution with a unique “non-stagnation” ABL in THB is aggravated by regional PM2.5 transport [38,39], and the effect of meteorology on PM2.5 pollution can accelerate and offset the effects of emission reductions oppositely in the northern and southern THB, respectively [40]. However, there is few research on the impact of vertical wind shear (VWS) on PM2.5 pollution over the receptor region in central China. Based on high-resolution radar observation, and surface environmental and meteorological observations in winters from 2016–2020, our study aimed to investigate the impacts of VWS on surface PM2.5 concentrations in two representative urban sites, Changsha (CS) and Jingmen (JM), in the southern and northern THB, respectively, and to reveal the implication of regional PM2.5 transport for environmental changes.
2. Data and Methods
2.1. Data
2.1.1. Ground-Based Meteorological and Environmental Data
The observational data of hourly PM2.5 concentrations in CS and JM (marked by pink dots in Figure 1b) for boreal winters (December, January, and February) from 2016–2020 were collected from the national air quality monitoring network [41], which was under strict quality control based on China’s national standard of air quality observation. To avoid the uncertainties induced by heterogeneous aerosol distribution among different sites in the same city, hourly PM2.5 concentrations for CS and JM were averaged with no more than 50% missing data over 10 and 4 environmental observation sites, respectively. The contemporaneous hourly meteorological data were sourced from the weather monitoring network of the China Meteorological Administration [42], including wind speed and wind direction.
Figure 1. The locations of the (a) Twain-Hu basin and (b) monitoring sites in Jingmen and Changsha overlaid with topography (color contour, m a.s.l.). The pink dots, blue pentacles, and black pluse are the locations of PM2.5, radar wind profiler (RWP), and radiosonde (SOND) sites, respectively.
2.1.2. RWP and Radiosonde Measurements
The RWP data were collected in CS and JM (marked by blue pentacles in Figure 1b), including the profiles of horizontal wind speed and direction. The raw data have undergone strict quality control before further analysis [31,43]. Hourly averaged wind profiles were computed from the original 6 min RWP data to match hourly PM2.5 concentrations, with no more than 40% missing data. On account of the high missing rate of RWP data above 1000m, the subsequent analysis of vertical wind was only conducted under 1000 m in JM to ensure the continuity and sample capability of vertical wind data (Figure S1).
The radiosonde sounding data measured in CS were used to characterize the thermodynamic structure relevant to air pollution. The sounding balloons are launched twice per day at 08:00 and 20:00 local standard time (LST, UTC+8). The detailed information on RWPs and radiosonde measurements are presented in Table 1.
Table 1. Detailed information on RWPs and radiosonde measurements in CS and JM.
2.2. Methods
For all measurements mentioned in this study, only the non-precipitation hours were selected to eliminate the effect of wet deposition on air pollutants. The precipitation hours are defined with precipitation amounts >0.1 mm [44]. Hourly PM2.5 concentration was normalized with monthly average [45], and the normalized PM2.5 concentration was grouped into three subsets with the same sample number [32]. The lower (bottom 1/3) and upper (top 1/3) terciles of the normalized hourly PM2.5 refer to clean and polluted conditions, respectively, to ensure that comparison can be performed with the same sample number between clean and polluted conditions [32].