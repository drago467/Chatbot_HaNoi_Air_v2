𝑅
)
2
	(2)

Where δEPM2:5 is the uncertainty for the PM2.5 emissions equation (1) and the uncertainty (δ) for each variable in equation (1). Proportion burned and crop area data from Vietnam government statistics do not have reported error. Thus, we conservatively assumed twenty percent error in these data.

We also compare our resulting emissions estimates with the Regional Emission inventory in ASia 2.1 (REAS), selecting only the combustion sources from the emissions inventory, available for PM2.5 for the latest year of 2008 (Kurokawa et al., 2013). The REAS is based on reported industrial activity data and existing survey data as well as other sources. This comparison will yield improved insight into the contribution of rice residue burning to all PM2.5 emissions.

5. Date of burning and pollutant transport

Due to consistent cloud cover and ephemeral agricultural fires in Vietnam, with only an average of about eighty fires detected during the residue burning season within the Red River Delta, other methods are needed to estimate burning (Fig. 2). We employ an indirect approach to estimate date of burning using time series of Sentinel-1A imagery as described in the previous section (Fig. 3). We used a total of 22 VH-polarized images starting on 3rd February 2016 and ending on 24th October 2016 with images for every 12 days excluding approximately June 28th due to no data. The phenology of rice fields has been highlighted in a number of recent studies, where minimum VH-polarized backscatter is observed during sowing because of inundation, and the maximum occurs at or near harvest attributed to removal of water prior to harvest and biomass removal, as well as double-bounce between rice plants and underlying surface and dielectric conditions of the canopy (Inoue et al., 2002, 2014; Choudhury and Chakraborty, 2006; Bouvet et al., 2009; Lopez-Sanchez et al., 2014; de Bernardis et al., 2015; Yuzugullu et al., 2015; Boschetti et al., 2017; Izumi and Demirci, 2017; Mansaray et al., 2017). We note that incident angle is constant throughout study area and is not a factor on backscatter variation.

Fig. 3.

Open in a new tab

Sentinel-1 VH backscatter averaged for each province. For each rice season, the date where backscatter values reach a maximum (i.e. June 2nd and October 12th) coincides with the rice harvest; then, the burning is assumed to occur within 3 days of harvest based on our field experience. Note: data was unavailable for June 28th (circled in red) due to image corruption. (For interpretation of the references to colour in this figure legend, the reader is referred to the Web version of this article.)

Within 4 km grid cells, we calculate the approximate harvest date based on the date of maximum backscatter within a window of each season based on local growing conditions (i.e. Feb–June for season 1, and Jun–Oct. for season 2). Based on our field experience, we found that rice residues were typically burned within 3 days of harvest (Lasko et al., 2017). Thus, we estimate the burn date by adding three days to the date of maximum backscatter. We then use these dates as the basis for air pollutant transport within the heavily populated study area, where air quality impacts would be strong due to the dense urban population (Hopke et al., 2008).

Back trajectories have been implemented by a number of studies attributing air quality to different biomass burning events in south/southeast Asia and abroad (Reiner et al., 2001; Eck et al., 2003; Kim et al., 2006; Badarinath et al., 2009; Sharma et al., 2010; Li et al., 2010; Sonkaew and Macatangay, 2015; Zhao et al., 2015). For the back-trajectory analysis we use the NOAA Hybrid Single Particle Lagrangian Integrated Trajectory (HYSPLIT) model (Draxler and Hess, 1998; Stein et al., 2015; Rolph et al., 2017) with hourly archived meteorological data from the US National Center for Environmental Prediction (NCEP) Global Data Assimilation System (GDAS). Back-trajectories were calculated during each estimated burn date and 1 day before and after, to account for variation in estimated burn date. The model parameters included: starting a new ground-level (5 m), 6 h back-trajectory every 3 h with start times selected during the day from 9AM to 6PM within the typical range of burn times and distances (Tipayarom and Oanh, 2007; Chen et al., 2017). We ran the HYSPLIT model for a total of 18 different dates.

6. Results
6.1. Rice area estimates

The rice area maps generated from each of the six datasets had mapped rice areas (in thousand ha) of 214.5 (VVVH10m), 220.3 (VVVH20m), 212.4 (VH10m), 218.8 (VH20m), 208.2 (VV10m), 214.9 (VV20m). Whereas the Vietnam Government data indicated 198.9 ha, showing similar results, with about 7.3% less than our most accurate VVVH10m data. Additional variation due to polarization and spatial resolution is described in Lasko et al., (2018). The rice map together with the field-based fuel-loading factors were used to estimate total rice residue using the factors shown in Table 2. The resulting rice residue map was the basis for emissions estimation in the Hanoi Capital Region of Vietnam. The total PM2.5 emissions for the HCR from rice residue burning are shown in Table 3 and Fig. 4b including the contribution to total estimated rice residue burning emissions for Vietnam with associated uncertainties in parentheses.

Table 3.

PM2.5 emissions reported in metric tons for the Hanoi Capital Region (HCR) and Vietnam based on the different rice residue burning scenarios. Residue amounts are in terragrams. Note the emissions estimates are shown to 2 significant digits. Error rates are shown in parentheses for the emission estimates. The last column shows the total percentage of rice residue burning emissions.

Rice area dataset	Region	Rice residue amount produced (Tg)	PM2.5 using general EF/CF	100% pile burning PM2.5	100% non-pile burning PM2.5	Most-likely scenario (50/50) PM2.5	Percent of emissions for entire Vietnam
SAR map	HCR	3.762	3400	9400 (±7,800)	6600 (±4,700)	8000 (±6,200)	5%
Govt. stats	Red River Delta	9.771	11000	24000 (±20,000)	17000 (±15,000)	21000 (±18,000)	14%
Govt. stats	Mekong River Delta	31.58	46000	100000 (±88,000)	72000 (±63,000)	86000 (±76,000)	58%
Govt. stats	Entire Vietnam	62.61	80000	180000 (±150,000)	130000 (±110,000)	150000 (±130,000)	100%
Open in a new tab
Fig. 4.

Open in a new tab

a)PM2.5 emissions in tons for Vietnam comparing values that would result from non-Pile Burning (Non-PB), Pile burning (PB), and most-likely Current Situation (CS) which assumes 50% PB and 50% Non-PB based on a report from Vietnam Office of Statistics.4b)Most-likely (CS) PM2.5 emissions per 4 km gridcell based on the SAR rice map available for Hanoi. This scenario assumes 50% PB and 50% non-PB based on a Vietnam Office of Statistics, 2017 report.

6.2. Burning practice specific emissions factors

The PM2.5 EF’s for rice straw burning range from as low as 4.2 g kg−2 to 20.67 g kg−2, whereas the generalized agricultural emission factors used in various global and regional biomass burning studies are 3.9 g kg−2and 6.26 g kg−2. The pile burning EFs have an average EF of 16.8 g kg−2(±6.9), as compared to 8.8 g kg−2(±3.5) from non-pile burning often found in machine-harvested fields, suggesting pile burning emits almost double the PM2.5 than non-pile burning fire emissions. An even starker contrast is seen between the general agriculture emission factors (i.e. 6.26 g kg−2in Akagi et al., 2011 and 3.9 g kg−2in Andreae and Merlet, 2001). These results demonstrate a shortcoming and potential underestimation in global studies. While challenging, larger-scale biomass burning studies should employ crop and burning practice specific emission factors in order to best capture biomass burning emissions variation and to avoid significant potential underestimation in the emissions. For example, using the general agriculture emission factor in Akagi et al., (2011) for this study instead of the pile burning emission factor, would yield a 77% difference in the resulting emissions.

The combustion factors ranged from 66.7% to 98.7% with generally lower factors for pile burning. The average for non-pile burning is 89% (±8%), and 67% (±7%) for pile burning. We note that combustion factor measurements are difficult to measure in the laboratory, and thus, may not be completely representative of field conditions with inherent uncertainty. The combustion factor used in general agricultural studies and global studies is 80%, i.e., eighty-percent burned as reported in the IPCC report on greenhouse gas emissions (Aalde et al., 2006).

6.3. PM2.5 emission scenarios

The PM2.5 emissions estimates for non-pile burning, pile burning, and current status scenarios are shown for each region of Vietnam (Fig. 4a). The majority of emissions are from the Mekong River Delta (72 Gg PM2.5 and 100 Gg PM2.5) for non-pile burning and pile burning respectively. The lowest emissions are found in the Central Highlands which is characterized by slash and burn agriculture and coffee plantations (Le et al., 2014). In total, for Vietnam 180 Gg of PM2.5 would be emitted if rice residues were burned following the pile burning method with fields harvested by hand, whereas 130 Gg would be emitted if rice residues were non-pile burned, a scenario assuming all fields are mechanized and harvested using combine harvesters or similar equipment. The most-likely current emission scenario (50% pile burn, 50% non-pile burning) estimates 150 Gg PM2.5 emissions for the entirety of Vietnam. Overall, there is a 32% difference between pile burning and non-pile burning emission scenarios suggesting that the burning practice plays a very important role in total emissions. The specific emission scenarios with associated uncertainty are shown in Table 3.

We also compared our emission estimates to an existing all combustion-sources inventory (Kurokawa et al., 2013). The results show rice residue burning contributes to 14%, 18%, and 16% of all combustion sources in Vietnam respectively for non-pile burning, pile burning, and most-likely current status. This suggests that rice residue burning is one of the major emissions contributors in Vietnam, and is the second largest contributor after fuelwood burning. However, the REAS emission inventory does not account for other biomass burning such as forest or shrubland, therefore emissions are likely somewhat high.

Many large-scale biomass burning studies rely on generalized agriculture emission factors due to currently limited availability of crop, region, or burning-practice specific data (Andreae and Merlet, 2001; Akagi et al., 2011). To estimate emissions for the entirety of Vietnam, we used the 2015 rice area from Vietnam office of statistics and the general agriculture emission factor from Akagi et al., (2011) with general agriculture combustion factor from IPCC (Aalde et al., 2006). The resulting rice residue burning PM2.5 emissions for Vietnam using these factors would be: 80 Gg which is only 44% of pile burning and 62% of non-pile burning. This large difference demonstrates burning practice specific and crop-specific factors are important to improve existing global and regional emission inventories.

6.3.1. Emissions transport

Based on the time-series SAR imagery for 2016, seasonal date of maximum backscatter per grid cell, and 3 day estimate between harvest and burn, we mapped the estimated burn date for each season (Fig. 5). The estimated burn dates were May 24th, June 5th, and June 17th for season one. For season two, the dates of burn were October 3rd, October 15th, and October 27th. These dates are constrained by the 12-day overpass for Sentinel-1 and burn date uncertainty. We subsequently ran the HYSPLIT back-trajectories over Hanoi City, Vietnam on these dates of burning as well as 1 day before and after to account for some variation.

Fig. 5.

Open in a new tab

Estimated dates of burning based on Sentinel-1 SAR maximum backscatter value for each 4 km gridcell for Spring and Autumn residue burning seasons.

Results from the HYSPLIT back-trajectory maps are shown in Fig. 6 and were conducted for the spring and autumn rice burning seasons. Trajectories generally originate from all directions outside of Hanoi City, suggesting potential rice residue burning impacts. Results stratified by season show that for autumn most trajectories originate from the North while for spring most originate from the South, likely due to synoptic weather patterns. A breakdown for the top 3 wind directions in the spring are: 31% South, 17% southeast, and 17% east; whereas for autumn: 26% North, 24% southeast, and 15% east. The biggest difference was 26% of trajectories originated north of Hanoi in Autumn, but only 6% during Spring as illustrated in the map. Thus, depending on the season, the emissions from different regions and directions will be more impactful in Hanoi City, highlighting the importance of accurate spatial maps of emissions. Overall, the air quality in Hanoi City could be linked with rice residue burning events, but the level of impact will be dependent on seasonal variability and timing and locations of burning. This suggests a need for further research on atmospheric chemical and concentration modelling in Hanoi.

Fig. 6.

Open in a new tab

NOAA HYSPLIT back-trajectories stratified by the two different burning seasons of Spring (May/June) and Autumn (Oct). Trajectory patterns suggested relatively more polluted air parcels moving into Hanoi City originate from the North, while more originate from the South during Spring.

7. Perspectives and conclusions

Our study conducted improved estimates of emissions for rice residue burning, and for the first time, accounted for burning practice in the resulting assessment. The results illustrate that when burning practice specific emission factors are employed, a large difference is seen in the emission estimates. Moreover, our study highlights that previous large-scale studies using general emission factors could be significantly underestimating emissions. Our latest estimates for the entirety of Vietnam for year 2015 show that the PM2.5 emissions likely fall somewhere between 130 Gg (100% non-pile burning) and 180 Gg (100% pile burned). Therefore, our rice residue burning estimates on PM2.5 will add significantly to the overall PM2.5 emissions, such as in the REAS emission inventory (Kurokawa et al., 2013). Our findings also show that rice residue burning contributes to 14% (non-pile burning), 18% (pile burning), and 16% (current status) of total combustion PM2.5 emissions in Vietnam in comparison with the REAS. These findings are important for improving upon existing emissions inventories and source apportionment.

These results have an important implication in terms of policy measures and for estimating future emissions. Both our field visit and the literature showed an increasing use of mechanized farming (Oanh et al., 2011; Lasko et al., 2017; Vietnam GSO, 2017). As harvesting practices transition from manual to machine-harvesting with non-pile burning, and assuming a constant rate of burning, the emissions could naturally decrease to the non-pile burning level. In addition, it’s possible to further mitigate emissions by improving crop residue management practices such as incorporating residues into the field and avoiding GHG emissions from residue burning. Whereas, the pile burning emissions estimates for Vietnam would be representative of historical emissions amounts prior to mechanization of agriculture.

The HYSPLIT trajectory model demonstrates common spatial patterns of rice residue burning emissions transport. With this knowledge, focusing emissions mitigation efforts in areas impacted by rice residue burning could be most beneficial. Some efforts to alleviate emissions impact have included: rice straw mushroom cultivation, enforcement of rice residue burning laws, and education on alternative uses such as for fertilizer, cattle feed, etc.

(Content truncated due to size limit. Use line ranges to read remaining content)