
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8361198/

---

Skip to main content

An official website of the United States government

Here's how you know
Search
Log in

Primary site navigation

Search PMC Full-Text Archive
Search in PMC
Journal List 
User Guide
As a library, NLM provides access to scientific literature. Inclusion in an NLM database does not imply endorsement of, or agreement with, the contents by NLM or the National Institutes of Health.
Learn more: PMC Disclaimer | PMC Copyright Notice
Sci Rep. 2021 Aug 12;11:16401. doi: 10.1038/s41598-021-95834-6
Hygroscopic properties of particulate matter and effects of their interactions with weather on visibility
Wan-Sik Won 1, Rosy Oh 2, Woojoo Lee 3, Sungkwan Ku 4, Pei-Chen Su 1,✉, Yong-Jin Yoon 1,5,✉
Author information
Article notes
Copyright and License information
PMCID: PMC8361198  PMID: 34385551
Abstract

The hygroscopic property of particulate matter (PM) influencing light scattering and absorption is vital for determining visibility and accurate sensing of PM using a low-cost sensor. In this study, we examined the hygroscopic properties of coarse PM (CPM) and fine PM (FPM; PM2.5) and the effects of their interactions with weather factors on visibility. A censored regression model was built to investigate the relationships between CPM and PM2.5 concentrations and weather observations. Based on the observed and modeled visibility, we computed the optical hygroscopic growth factor, 
𝑓
RH
, and the hygroscopic mass growth, 
𝐺
𝑀
VIS
, which were applied to PM2.5 field measurement using a low-cost PM sensor in two different regions. The results revealed that the CPM and PM2.5 concentrations negatively affect visibility according to the weather type, with substantial modulation of the interaction between the relative humidity (RH) and PM2.5. The modeled 
𝑓
RH
 agreed well with the observed 
𝑓
RH
 in the RH range of the haze and mist. Finally, the RH-adjusted PM2.5 concentrations based on the visibility-derived hygroscopic mass growth showed the accuracy of the low-cost PM sensor improved. These findings demonstrate that in addition to visibility prediction, relationships between PMs and meteorological variables influence light scattering PM sensing.

Subject terms: Environmental sciences, Engineering

Visibility represents the maximum distance from which an object can be recognized. It is controlled by the intensity of light absorption and scattering of gases and particulates in the atmosphere. Visibility degradation is mainly influenced by the amount and type of water droplets and aerosols suspended in the air1,2. This degradation affects people psychologically and physiologically, and causes inconvenience and poses danger when performing human activities such as aviation and shipping1,3. Sudden and prolonged visibility impairment poses risks to traffic areas, particularly aviation safety, by restricting surface movements and flight conditions during a flight’s takeoff or landing at airports4,5. In recent decades, due to increasing particulate matter (PM) concentrations from air pollutants in industrial areas and automobile exhaust in urban areas, visibility impairment, characterized by heavy haze or a haze-fog mixture, has increased continually6,7. These anthropogenic emissions interacting with meteorological variables complicate visibility prediction.

PM is mainly classified by size as PM10 and PM2.5, characterized by aerodynamic diameters of less than 10 and 2.5 µm, respectively. According to its definition, PM2.5 is a subset of PM10 particles. Thus, PM10–2.5, which has a particulate diameter between 2.5 and 10 µm, is termed as coarse PM (CPM) as opposed to the fine PM (FPM; PM2.5). The CPM originates primarily from nature (such as the ocean and land), whereas PM2.5 are generally secondary products of air pollution, in addition to the natural sources8–10. Prior to PM2.5 attracting significant attention because of its effects on human health and environment, PM10 was the most commonly monitored pollutant and was employed to study the pollution trends over past decades or to predict visibility11–14. Currently, the mitigation and monitoring of PM2.5 is the primary concern. Consequently, visibility studies also focus on the chemical composition and properties of PM2.515–17.

Owing to its abundant water-soluble particles, PM2.5 exhibits better hygroscopic properties for light scattering, thereby affecting visibility more than the CPM14,17,18. Water vapor impacts visibility because of the hygroscopic growth at elevated relative humidity (RH). The hygroscopic growth is the change of the diameter of a particle because of the uptake of water. It is represented as the particle size hygroscopic growth factor, 
𝐺
𝐹
RH
=
𝐷
RH
/
𝐷
𝑑
, defined as the ratio of the diameter of a particle (
𝐷
) at a given RH to that of dry particle (
𝐷
𝑑
)10,19,20. Similarly, the optical hygroscopic growth factor, 
𝑓
RH
=
𝜎
ext
RH
/
𝜎
ext
dry
, is defined as the ratio of the extinction coefficient (
𝜎
ext
) under wet conditions to that under dry conditions21–23. Hygroscopic PM scatters more light under humid weather conditions, resulting in lower visibility at high RH levels; therefore, predicting visibility under PM effects while considering their complicated interaction with meteorological factors is still challenging13,24. It is already well documented that visibility is predicted primarily by RH and the chemical composition of aerosols with empirical functions21,22. While chemical species are not typically monitored outside of special campaign periods, PM and weather variables such as RH are regularly reported by environmental or weather authorities. An international airport is a suitable weather station for regularly conducting meteorological observations like visibility25. Thus, it is notable that visibility can be estimated in real-time by an empirical function from RH and PM concentration than by chemical species data. Meanwhile, the light scattering characteristics of PM are also valuable not only for visibility studies but for manufacturing PM measuring instruments26–28. Recently, low-cost PM sensors have become more popular due to the convenience of real-time air quality monitoring29–31. Although they are easy to operate, the low-cost PM sensors have low accuracy because the estimations of PM concentrations made by the light-scattering sensors are affected by a variety of environmental parameters26,28,32,33. An important reason for the lower accuracies is that low-cost sensors lack the RH and temperature control functions; therefore, light scattering sensors overestimate the PM concentration affected by humidity26,34. Therefore, while understanding the hygroscopic properties of the CPM and PM2.5 and their relationship with weather is essential for predicting visibility, it can also contribute to enhancing sensor technology for more accurate measurements of PM concentrations.

In this study, the hygroscopic properties of CPM and PM2.5, and the effects on visibility due to their interactions with meteorological factors were investigated by modeling the relationship between CPM and PM2.5 concentration, and weather observations collected over four years from Incheon International Airport (ICN). A censored regression model was built to quantitatively predict the impact of CPM and PM2.5 on visibility under different meteorological conditions. We focus on determining the characteristics of CPM and PM2.5 that interact with meteorological factors and quantifying the relationship between PM concentration and visibility. Furthermore, we conducted PM2.5 field measurements in two different regions, namely Jeju, Korea and Singapore, to assess the effect of the RH on PM measurement by applying the RH-adjusted correction to the low-cost PM2.5 sensors based on the visibility-derived hygroscopic mass growth.

Results
PM–visibility weather dependence

The distributions of PM concentrations and visibility data for 4 years at the ICN are displayed in Fig. 1. The visibility data represent hourly observations at the airport, while the PM concentrations were obtained from the Unseo air pollution monitoring station near the ICN. The highest visibility of 10 km implies equal to or more than 10 km, according to the visibility standards reported at airports5,35. The exceptionally high CPM concentrations in Fig. 1, which indicate the Asian Dust in February 2018, highlight the elevated CPM transportation into the Seoul Metropolitan Area (SMA). The data in Table S-1 reveal average PM2.5 concentration at the ICN of 23 μg m−3 over the four years. This value largely exceeds that of the WHO annual standard and those put forth by other countries36,37 (statistics for each variable are presented in Table S-1). The ICN is impacted by visibility impairment associated with high PM concentrations annually, and particularly from December 24–25, 2017, during which half of the flights were delayed or canceled due to heavy haze and dense fog with high PM concentrations38.

Figure 1.

Open in a new tab

Scatter plots of visibility (km) and PM concentration (μg m−3) for CPM and PM2.5 at the ICN, 2015–2018. The different colors represent different weather types: haze, dust, mist, fog, and others (RA, DZ, SN, and None).

In Fig. 1, the plot of the relationships between the PM concentration and visibility under different weather types including haze (HZ), dust (DU), mist (BR), fog (FG), and others (RA (rain), DZ (drizzle), SN (snow), None) are represented by different colors (the criteria of each weather phenomena are presented in Table S-4). In the CPM plot, the boundary between dust and haze is distinct, whereas the PM2.5 plot exhibits an overlap. Although distinguishing between haze and mist in the CPM plot is difficult, the haze and mist distributions are easier to distinguish in the PM2.5 plot, and visibility in haze is higher than in mist for the PM2.5 plot. Consequently, the CPM concentration is remarkably high in dust, while haze is elevated in PM2.5. According to the weather type-based plot, visibility generally decreases with the PM concentration, except in the case of fog. Mist is at the boundary between haze and fog, and many cases in fog are characterized by low visibility, regardless of the PM concentration. The cases of fog exceeding 1 km involve scattered fog such as the fog patches and partial fog, for which the weather codes are BCFG and PRFG, respectively, according to the weather reporting manual39. The PM–visibility relationships under different meteorological conditions are further examined in the next section.

Correlation between PM and meteorological factors

The relationships between all variables are shown in Fig. 2, with the RH exhibiting the highest correlation with visibility (VIS), − 0.59, followed by the PM2.5, − 0.50, while the wind speed (WS) shows weak positive correlations of 0.15. Although the CPM displays very weak correlations of − 0.08, its correlation of − 0.21 and − 0.33 in haze and dust, respectively, at the ICN cannot be ignored (Fig. S-2). The temperature (TMP) and VIS display essentially no correlation, with values of − 0.01 at the ICN. As the most important variable, high RH significantly reduces visibility and contributes to hydrometeors formation such as fog2. Even in fine aerosols, the extinction coefficient values of high hygroscopicity particles increase through moisture absorption, further supporting RH as a major factor responsible for decreased visibility21,22. This validates the conclusion that PM2.5 commonly displays strong correlation with visibility15,17,24. According to the Mie-scattering theory, the scattering efficiency associated with the light wavelength is frequently high for particles less than 2.5 µm in diameter40–42. Among particles with high extinction efficiency values, sulfates and nitrates characterized by high hygroscopicity also fall in the less than 2.5 µm category24,43. According to previous studies, the PM10 contributes to visibility deterioration11–13, which can be attributed mostly to the PM2.5. Therefore, better prediction of the distribution and concentration of the fine PM is necessary to clearly understand how PMs and weather factors affect visibility.

Figure 2.

Open in a new tab

Matrix of plots and correlation coefficients between variables for the ICN over four years (2015–2018). The upper panel above the diagonal in each matrix shows correlation coefficients between two variables; the lower panel below the diagonal gives their scatter plots. The histograms of each variable are shown in the diagonal line. For WX (weather), the upper and lower panels (the two are the same) give boxplots of each variable categorized by eight WX levels: None, HZ (haze), DU (dust), BR (mist), FG (fog), DZ (drizzle), RA (rain), and SN (snow) in order. Units are as follows; CPM (μg m−3), PM2.5 (μg m−3), TMP (℃), RH (%), WS (kt*), and VIS (km) respectively. *1 kt = 0.5144 m s−1.

Regarding the PM, the CPM and PM2.5 show very weak negative correlations with the TMP, while the RH and WS display opposite correlations, respectively. For example, the correlation between the RH and CPM is negative, while that between the RH and PM2.5 is positive. In the RH–CPM and RH–PM2.5 plots, the RH shows higher correlation with the PM2.5 than with the CPM (0.20 and –0.10, respectively). In the WS–PM2.5 plot, the lower the wind speed, the higher the concentration (− 0.20). Conversely, in the WS–CPM plot, high concentrations are observed in the case of winds exceeding 10 kt. This is explained by the negative correlations in the RH–WS plot (− 0.27), demonstrating that low wind speed and high humidity values are related to high PM2.5 concentrations. Since these conditions are common under stable atmospheric conditions, several studies have revealed their association with PM2.5 stagnation18,45,46. In the WX–CPM box plot, the CPM commonly displays high concentrations in dust, while in the WX–PM2.5 box plot, the highest PM2.5 concentrations occur in haze and dust. The dust-pollution is mainly influenced by the Asian Dust in spring, and the high PM2.5 concentration in dust indicates that in addition to the CPM, fine PM are transported into the region47.

Impacts of PM and meteorological factors on visibility

The visibility prediction model determined the effects on visibility considering the PM2.5 and CPM variables for each weather factor (Table S-7). The contribution of each PM concentration on visibility degradation depends on the coefficient of TMP, RH, and WS. For example, the coefficients of the interactions between the PM2.5 and meteorological variables, TMP, RH, and WS (− 0.231, 0.676, and 0.086, respectively) show that visibility decrease at any PM2.5 concentration is associated with high TMP, low RH, and low WS. Conversely, the effect of any CPM concentration (0.020, 0.193, and − 0.023, respectively) is related to low TMP, low RH, and high WS. The coefficient of the PM2.5–TMP interactions (− 0.231) and that of the PM2.5–RH interactions (+ 0.676) demonstrate involvement in visibility degradation. When comparing the visibility estimation coefficient for each variable, the effect of the 
𝑍
RH
, with its coefficient of –2.88 km is the highest (refer to Table S-6g). Thus, when the RH increases, the effect of the PM is reduced, while that of the RH is maintained. Conversely, at low RH, the PM mainly control the visibility impairment. For example, assuming standardized values of 0 for the TMP, RH, and WS, for haze at the ICN, the coefficient for the PM2.5 (
𝛽
𝑍
𝑃
𝑀
2.5
) changes to − 0.784 and that for the CPM (
𝛽
𝑍
CPM
) to − 0.637. Evidently, the values for the PM2.5 and CPM are not significantly different, but since days with high PM concentrations are often dry (
𝑍
RH
<
0
), at 
𝑍
RH
=
-
1.0
 (RH 44%) with 
𝑍
TMP
=
0
 and 
𝑍
WS
=
0
, the effect of PM2.5 is − 1.46 km, while the CPM effect is − 0.83 km. Contrarily, for fog, since the humidity is very high (
𝑍
RH
≫