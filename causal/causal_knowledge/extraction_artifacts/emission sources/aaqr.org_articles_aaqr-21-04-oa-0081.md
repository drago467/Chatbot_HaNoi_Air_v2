The RF model was applied to describe the relationship between hourly pollutant concentrations (PM2.5, CO) and the predictor variables as regression decision trees (Vu et al., 2019). These predictor variables included temporal variables (Unix Epoch time (ttrend), hour (0–23), weekday (Monday–Sunday), meteorological parameters (wind speed, wind direction, pressure, precipitation, temperature, relative humidity, and radiation), and air mass trajectory clusters. The effect of long-range transport was considered by inputting the air mass trajectory clusters in the model. However, those clusters demonstrated categorical information rather than a quantitative measurement of air mass trajectory.

In this study, a training data set (80% of total available data, which was randomly selected) constructed for the RF model, and then an unseen data set (20% left of all data points) would validate predicted results. Air mass trajectory clusters were determined by the HYSPLIT model using similar conditions as in the CWT model. The method to construct RF and calculate normalized weather concentrations is similar to the method used in Vu et al. (2019). Generally, the weather normalizing method also includes the impact of both seasonal and weather variations. In the method used in Vu et al. (2019), to improve the algorithm, meteorological variables of only the same hour in other days within two weeks before and after the investigated hour were selected (Vu et al., 2019).

 
3 RESULTS AND DISCUSSION
 
3.1 PM2.5 and CO Concentrations during Studied Periods in 2020

3.1.1 PM2.5 concentrations

Fig. 2(a) illustrates the daily mean PM2.5 concentrations in urban and traffic areas. During the study period, daily PM2.5 concentrations ranged widely from 10 to 130 µg m–3. The concentrations of PM2.5 recorded in 2020 varied in the same range as in 2019. The detailed statistics and confidential intervals (CI) in 2019 and 2020 by each period are provided in Table S2. In 2020, PM2.5 concentrations were 48 (95% CI: 45.7, 50.5) and 62 (95% CI: 59.3, 65) µg m–3 for urban and traffic sites in the pre-social distancing period. During soft and hard social distancing periods of 2020, PM2.5 concentrations declined by 18% and 13% in urban sites and by 15% and 14% in traffic sites in soft- and hard- distancing periods. The concentration declined further by 29% and 30% in the post-social distancing period, at urban and traffic sites, respectively. Because pollutant concentrations can be affected by meteorological conditions, discussion about trends without meteorological effects is presented in Section 3.3.1.

Fig. 2. (a) Daily concentrations of PM2.5 during pre-, soft, hard, post social distancing periods in 2020: Pink shade denotes the soft social distancing period. Orange shade denotes the hard social distancing one. (b) Diurnal variations of PM2.5 concentrations.



Fig. S1 (Supplementary Material) presents the correlation coefficients (r) of PM2.5 concentrations at nine stations in the studied periods are. High correlation, r > 0.80 for all sites, demonstrated the strong effects of regional sources on PM2.5 levels. No clear traffic rush-hour peaks were observed for PM2.5 even at roadside sites. However, the PM2.5 levels at traffic sites were consistently higher than in urban sites in 2020 during pre-, soft, hard, and post-social distancing periods, respectively (at 14.2, 13.3, 11.6, and 9.6 µg m–3) (Fig. 2(b)). This fact indicated an influence of traffic on PM2.5 levels at the roadside sites and strong impacts of weather on the dispersion, dilution, and elevation of fine particles at the urban scale. Explanation of these complex atmospheric processes of PM2.5 is out of the scope of this research.

 
3.1.2 CO concentrations

Fig. 3(a) shows large variations of daily CO concentrations. Its concentrations at urban stations fluctuated from approximately 400 to 1500 µg m–3, while those levels at roadside stations varied from approximately 500 to 2500 µg m–3, with the highest peaks happening in mid-March. The detailed statistics and CIs in 2019 and 2020 by each period are provided in Table S2. CO concentrations in this study are in agreement with the previous field measurements by Sakamoto et al. (2018) and Hien et al. (2002) who reported the annual levels of CO in Hanoi were around 1.3 ppm (~1.5 mg m–3). Concentrations of CO during soft and hard social distancing periods decreased by 41%, 29% at urban sites, and 28% during both periods at traffic sites.

Fig. 3. (a) Daily concentrations of CO during pre-, soft, hard, post social distancing periods in 2020. Pink shade denotes the soft social distancing period. Orange shade denotes the hard social distancing one. (b) Diurnal variations of CO concentrations.



The correlation coefficients (r) between CO levels from nine stations in the investigated periods were shown in Fig. S2(b). These r values were in the range of 0.34–0.80 which were lower than those for PM2.5, demonstrating that CO was more predominantly affected by local sources than PM2.5.

The observed CO concentrations at traffic sites were double those at urban sites in median (2.2, 1.8, 2.4 times in soft, hard, and after the social distancing, respectively) (Fig. 3(a)). In addition, the diurnal pattern (Fig. 3(b)) shows two distinct peaks coinciding with the traffic rush hours in Hanoi. At traffic peak hours, CO concentrations were approximately double those in the midnight and midday concentrations. It indicated a stringent relation of CO concentrations with road traffic emissions. In addition, the diurnal pattern (Fig. 3(b)) shows two distinct peaks coinciding with the traffic rush hours in Hanoi. The effects of traffic emissions on both CO trend and concentrations are much clearer than on PM2.5.

 
3.2 Impact of Meteorological Factors on PM2.5 Concentrations

The following section illustrates the impact of important meteorological factors (wind speed, wind direction) and long-range transport on PM2.5. The information on meteorological conditions during the study period is provided in detail in Section S1 (Supplementary Material).

 
3.2.1 Impact of wind speed and direction

Wind speed plays a key role in the dispersion of air pollutants as demonstrated in previous studies (Hien et al., 2002; Ly et al., 2018., 2020). Fig. 4(a) shows most episodes of high PM2.5 concentrations associated with the low wind speed (v < 2.05 m s–1). The windrose profile of PM2.5 concentrations in Fig. 4(b) also confirmed such association. Low wind speed may associate with circle wind, and the measured wind direction is more affected by nearby terrain. At the high level of wind speed (v > 5 m s–1), concentrations of PM2.5 were higher when the wind came from the eastern and southeastern directions (Fig. 4(b)), suggesting the impact of the sources of fine particles outside Hanoi city.

Fig. 4. Effects of wind speed on PM2.5 concentrations: (a) PM2.5 concentrations by wind speed; (b) Heat map of PM2.5 concentrations in relation to wind rose at traffic site.



 
3.2.2 Impact of air mass trajectories

Fig. 5 illustrates the 6-hour average concentrations of PM2.5 and backward air mass trajectory clusters in 2020. Those clusters include C1: originated from the northeast, passing ocean before reaching Vietnam (26.0%); C2: originated from north, northeast, passing land before reaching Vietnam (24.7%); C3: Originated from the southeast (25.7%); C4: Originated from the southwest (23.6%). Accordingly, Hien et al. (2004) demonstrated that the different contributions of long-range transport and secondary formation on PM2.5 concentrations associate with different trajectory clusters. In short, the contributed percentage of long-range transport on PM2.5 was in the order of C2 > (C1, C3) > C4. The contribution of secondary formation was highest with (C1, C3). Fig. 5(a) shows that all four clusters came to Hanoi quite evenly before the social distancing (pre-social distancing) period. During the soft social distancing period, the main air mass trajectory cluster was C3, from the southeast, then during the hard social distancing period, the C2 from north-northeast, land originated trajectory got the largest shared. Fig. 5(a) also shows the relationship of the backward trajectory with the highest PM2.5 events during those periods. The second event was related to the trajectory C3 from the southeast. The third major event of PM2.5 during the hard social distancing period relates to the first half of C2 from the mainland, north-northeast, and then C1 northeast from the sea. In the post-social distancing, the southeast (C4) trajectory cluster got the largest share in May. It corresponded with moderately low PM2.5 concentrations in May, notwithstanding its relation to a higher level of PM2.5 in April and the highest in March. The reason might be the biomass burning events during spring in the southeast area along the trajectory.

Fig. 5. Effects of backward air mass trajectories: (a) PM2.5 concentrations in relation to air mass trajectory clusters in 2020; (b) Air mass trajectory clusters in March-May 2020; (c) CWT in the pre-, during, and post social distancing periods.



The CWT map (Fig. 5(c)) also shows a wide area of potential sources from north, northeast, southeast, and a small portion from the west to Hanoi in the pre-social distancing. During the social distancing, the potential source areas were mainly from the northeast to the south. In the post-social distancing, potential sources were enlarged to the southwest than those during the social distancing.

 
3.3 Weather Normalized PM2.5 and CO Concentrations in Pre-, during, and Post-social Distancing

3.3.1 Weather normalized PM2.5 concentrations

As presented in Section 3.1.1, during the pre-social distancing, urban and traffic sites had average PM2.5 concentrations of 48 and 62 µg m–3, respectively. As Hanoi observed noticeable precipitation and strong wind at the beginning of March, PM2.5 concentrations remained low, the minimum approximately 20–30 µg m–3. Wind speed decreased shortly afterward, leading to a rise in PM2.5 concentrations with a daily peak of 123 µg m–3. Observed concentrations of PM2.5 dropped in the social distancing period and even further after that.

To understand the influence of meteorological factors, we conducted weather normalization to estimate the hourly weather normalized PM2.5 concentrations as shown in Fig. 6.

Fig. 6. Hourly concentration of weather normalized: (a) PM2.5, (b) CO. The blue text represents the number at traffic sites, the orange text represents the number at urban sites.



Table S3 and Fig. S2(a) provide the performance metrics of our RF models. After normalizing the effects of meteorological factors, the variability of PM2.5 decreased largely compared to the original observed data. The corresponding weather normalized concentrations were 48 and 64 µg m–3 in the pre-social distancing. The decreases under the period of soft social distancing were recalculated to be 8%, 7% for urban and traffic stations. Afterward, weather normalized concentrations during hard social distancing decreased by 10% and 9% at urban and transportation stations.

Those reductions after de-weathering were quite less than the observed concentrations of PM2.5 (14–18%), indicating the favored weather contributes significantly to the reductions of fine particles during soft and hard social distancing. Interestingly, in the post-social distancing, a further reduction of weather normalized PM2.5 concentrations were 17% and 21% at urban and traffic sites, respectively. Several reasons could be explained for those drops, especially the seasonality of primary, secondary, and long-range transport sources of aerosols. We note that summertime began in the post-social distancing period. Firstly, though the contribution of road traffic emission rose again in the post-social distancing period, other main primary sources of PM2.5 such as residential or agricultural emissions may continue to decrease. As discuss above biomass burning in the region (Thailand, Laos, Cambodia, Myanmar, Vietnam) occurs more frequently in spring (March–April) rather than in May when the social distancing ends (Bukowiecki et al., 2019; Sirimongkonlertkun, 2018). In another study, Vu et al. (2019) showed primary emissions of PM2.5 from the residential sector in Beijing decreased significantly during summertime during 2013-2017. The second reason could be the decrease in secondary aerosols.

Because of the higher mixing layer height in summer, secondary aerosols precursors such as SO2 and NOx were more elevated, hence reducing their concentrations. A lower concentration of secondary aerosols in summer could lead to a smaller amount of secondary aerosols formed. In addition, extremely hot temperatures and lower humidity in summer could reduce concentrations of secondary aerosols. Since the temperature in the period of the post-social distancing (at 28oC) was higher than in previous periods (22–24oC), the secondary particles (NH4NO3) have been volatilized partially, and the formation rate was slower as relative humidity was also low (< 80%) (Dawson et al., 2007; Stelson and Seinfeld, 1982). Although we included the temperature and relative humidity as input variables in our random forest model, however, chemistry in secondary particle formation and sinks in Hanoi are very complex. Therefore, it requires a chemical transport model to investigate that since the random forest model by itself can hardly explain these phenomena. The third reason for the reduction of PM2.5 in the post-social distancing period could be the less contribution of regional transport of PM2.5 in summer. The transboundary of PM2.5 to Hanoi in the winter and spring have been highlighted significantly in the research of Hien et al. (2011), Ly et al. (2021). In our model, several air mass clusters only represent the origins of air masses but did not account for the contribution of individual air masses to PM2.5 concentrations quantitatively (Shi et al., 2021). Similar trends of weather normalization PM2.5 reduction toward summer were also found in 2019 as shown in Table S2. The reductions of PM2.5 in Hanoi in summer have been demonstrated in previous research (Cohen et al., 2011, Ly et al., 2018).

Strong impacts of meteorology, long-range transport, and atmospheric chemistry that contribute to the level of PM2.5 during COVID-19’s lockdown period also be agreed upon by other studies. Those studies in the region also elucidated the unexpected pollution events that occurred during the lockdown time. Using a similar de-weather technique, Shi et al. (2021) observed an increase of PM2.5 in Bejing after the lockdown began. The unfavorable weather (high relative humidity, low wind speed, and boundary layer height) in Beijing-Hebei-Tianjin promotes the increase of heterogeneous aerosol chemistry (Chen et al., 2020). Long-range transport plays a crucial role in enhancing the fasting of the particular nitrate formation, the main factor contributing to the high atmospheric particle concentration in Shanghai (Chang et al., 2020). Otherwise, in Thailand, Dejchanchaiwong and Tekasakul (2021) explained the increase of PM2.5 under business areas in the lockdown period by identifying sources via calculating the ratio of organic carbon and elemental carbon (OC/EC) and backward trajectory simulation. The finding shows that the significant effects of local aerosol transport from open biomass burning in Thailand, Myanmar, Cambodia, Laos, and Vietnam affected the PM2.5 increase in Bangkok. Effectively controlling PM2.5 in any place in the region may require the co-effort from the neighborhood.

 
3.3.2 Weather normalized CO concentrations

(Content truncated due to size limit. Use line ranges to read remaining content)