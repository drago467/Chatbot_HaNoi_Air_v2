
**URL:** https://acp.copernicus.org/articles/22/4101/2022/

---

Atmospheric Chemistry and Physics
ARTICLES & PREPRINTS 
SUBMISSION
POLICIES 
PEER REVIEW 
EDITORIAL BOARD
AWARDS 
ABOUT 
EGU PUBLICATIONS
 
Article  
Articles
Volume 22, issue 6
ACP, 22, 4101–4116, 2022
https://doi.org/10.5194/acp-22-4101-2022
© Author(s) 2022. This work is distributed under
the Creative Commons Attribution 4.0 License.
Article
Assets
Peer review
Metrics
Related articles
Research article
 | 
29 Mar 2022
Impacts of aerosol–photolysis interaction and aerosol–radiation feedback on surface-layer ozone in North China during multi-pollutant air pollution episodes
Hao Yang, Lei Chen, Hong Liao, Jia Zhu, Wenjie Wang, and Xin Li
Abstract

We examined the impacts of aerosol–radiation interactions, including the effects of aerosol–photolysis interaction (API) and aerosol–radiation feedback (ARF), on surface-layer ozone (O3) concentrations during four multi-pollutant air pollution episodes characterized by high O3 and PM2.5 levels during 28 July to 3 August 2014 (Episode1), 8–13 July 2015 (Episode2), 5–11 June 2016 (Episode3), and 28 June to 3 July 2017 (Episode4) in North China, by using the Weather Research and Forecasting with Chemistry (WRF-Chem) model embedded with an integrated process analysis scheme. Our results show that API and ARF reduced the daytime shortwave radiative fluxes at the surface by 92.4–102.9 W m−2 and increased daytime shortwave radiative fluxes in the atmosphere by 72.8–85.2 W m−2, as the values were averaged over the complex air pollution areas (CAPAs) in each of the four episodes. As a result, the stabilized atmosphere decreased the daytime planetary boundary layer height and 10 m wind speed by 129.0–249.0 m and 0.05–0.15 m s−1, respectively, in CAPAs in the four episodes. Aerosols were simulated to reduce the daytime near-surface photolysis rates of J[NO2] and J[O1D] by 1.8 × 10−3–2.0 × 10−3 and 5.7 × 10−6–6.4 × 10−6 s−1, respectively, in CAPAs in the four episodes. All of the four episodes show the same conclusion, which is that the reduction in O3 by API is larger than that by ARF. API (ARF) was simulated to change daytime surface-layer O3 concentrations by −8.5 ppb (parts per billion; −2.9 ppb), −10.3 ppb (−1.0 ppb), −9.1 ppb (−0.9 ppb), and −11.4 ppb (+0.7 ppb) in CAPAs of the four episodes, respectively. Process analysis indicated that the weakened O3 chemical production made the greatest contribution to API effect, while the reduced vertical mixing was the key process for ARF effect. Our conclusions suggest that future PM2.5 reductions may lead to O3 increases due to the weakened aerosol–radiation interactions, which should be considered in air quality planning.

How to cite. 

Yang, H., Chen, L., Liao, H., Zhu, J., Wang, W., and Li, X.: Impacts of aerosol–photolysis interaction and aerosol–radiation feedback on surface-layer ozone in North China during multi-pollutant air pollution episodes, Atmos. Chem. Phys., 22, 4101–4116, https://doi.org/10.5194/acp-22-4101-2022, 2022.

Received: 10 Feb 2021 – Discussion started: 02 Mar 2021 – Revised: 18 Feb 2022 – Accepted: 26 Feb 2022 – Published: 29 Mar 2022
1 Introduction

The characteristics of air pollution in China during recent years have changed from a single pollutant (e.g. PM2.5, i.e. particulate matter with an aerodynamic equivalent diameter of 2.5 µm or less), to multiple pollutants (e.g. PM2.5 and ozone and O3; Zhao et al., 2018; Zhu et al., 2019), and the synchronous occurrence of high PM2.5 and O3 concentrations has been frequently observed, especially during the warm seasons (Dai et al., 2021; Qin et al., 2021). Qin et al. (2021) reported that the co-occurrence of PM2.5 and O3 pollution days (days with PM2.5 concentration > 75 µg m−3 and maximum daily 8 h average ozone concentration > 80 ppb; parts per billion) exceeded 324 d in eastern China during 2015–2019. Understanding complex air pollution is essential for making plans to improve air quality in China.

Aerosols can influence O3 by changing the meteorology through absorbing and scattering solar radiation (defined as aerosol–radiation feedback (ARF) in this work; Albrecht, 1989; Haywood and Boucher, 2000; Lohmann and Feichter, 2005), which influences the air quality by altering the chemical reactions, transport, and deposition of the pollutant (Gao et al., 2018; Qu et al., 2021; Xing et al., 2017; Zhang et al., 2018). Many studies have examined the feedback between aerosols and meteorology (Gao et al., 2015; M. Gao et al., 2016; Qiu et al., 2017; Chen et al., 2019; Zhu et al., 2021). For example, Gao et al. (2015) used the Weather Research and Forecasting with Chemistry (WRF-Chem) model to investigate the feedbacks between aerosols and meteorological variables over the North China Plain in January 2013 and pointed out that aerosols caused a decrease in surface temperature by 0.8–2.8 ∘C but an increase of 0.1–0.5 ∘C around 925 hPa. By using the same WRF-Chem model, Qiu et al. (2017) reported that the surface downward shortwave radiation and planetary boundary layer height (PBLH) were reduced by 54.6 W m−2 and 111.4 m, respectively, due to the aerosol direct radiative effect during 21–27 February 2014 in the North China Plain. Such aerosol-induced changes in meteorological fields are expected to influence O3 concentrations during multi-pollutant episodes with high concentrations of air pollutants.

Aerosols can also influence O3 by altering photolysis rates (defined as aerosol–photolysis interaction (API) in this work; Dickerson et al., 1997; Liao et al., 1999; Li et al., 2011; Lou et al., 2014). Dickerson et al. (1997) reported that the presence of pure scattering aerosol increased ground level ozone in the eastern United States by 20 to 45 ppb , while the presence of strongly absorbing aerosol reduced ground level ozone by up to 24 ppb. Wang et al. (2019) found that aerosols reduced the net ozone production rate by 25 % by reducing the photolysis frequencies during a comprehensive field observation in Beijing in August 2012. Such aerosol-induced changes in the photolysis rates are expected to influence O3 concentrations during multi-pollutant episodes with high concentrations of air pollutants.

Few previous studies have quantified the effects of ARF and API on O3 concentrations. Xing et al. (2017) applied a two-way online coupled WRF-CMAQ (Community Multi-scale Air Quality) model and reported that the combination of API and ARF reduced the surface daily maximum 1 h O3 (MDA1 O3) by up to 39 µg m−3 over China during January 2013. Qu et al. (2021) found, by using the UK Earth System Model (UKESM1), that ARF reduced the annual average surface O3 by 3.84 ppb (14.9 %) in the North China Plain during 2014. Gao et al. (2020) analysed the impacts of API on O3 by using the WRF-Chem model and reported that API reduced surface O3 by 10.6 ppb (19.0 %), 8.6 ppb (19.4 %), and 8.2 ppb (17.7 %) in Beijing, Tianjin, and Shijiazhuang, respectively, during October 2018. However, these previous studies mostly examined either ARF or API and did not examine their total and respective roles in O3 pollution in China. Furthermore, these previous studies lacked process understanding about the impacts of ARF and API on O3 pollution under the co-occurrence of PM2.5 and O3 pollution events.

The present study aims to quantify the respective/combined impacts of ARF and API on surface O3 concentrations by using the WRF-Chem model and to identify the prominent physical and/or chemical processes responsible for ARF and API effects by using an integrated process rate (IPR) analysis embedded in the WRF-Chem model. We carry out simulations and analyses on four multi-pollutant air pollution episodes (Episode1 is 28 July to 3 August 2014; Episode2 is 8–13 July 2015; Episode3 is 5–11 June 2016; Episode4 is 28 June to 3 July 2017) in North China with high O3 and PM2.5 levels (the daily mean PM2.5 and the maximum daily 8 h average O3 concentration are larger than 75 µg m−3 and 80 ppb, respectively). These episodes are selected because (1) these events with high concentrations of both PM2.5 and O3 are the major subjects of air pollution control, (2) high concentrations of both PM2.5 and O3 allow one to obtain the strongest signals of ARF and API, (3) the measurements of J[NO2] during 2014 and 2015 from the Peking University site (Wang et al., 2019) can help to constrain the simulated photolysis rates of NO2, and (4) selected events cover different years (2014 to 2017) during which the governmental Air Pollution Prevention and Control Action Plan was implemented (the changes in emissions and observed PM2.5 in the studied region during 2014–2017 are shown in Fig. S1 in the Supplement). We expect that the conclusions obtained from multiple episodes represent the general understanding of the impacts of ARF and API.

The model configuration, numerical experiments, observational data, and the integrated process rate analysis are described in Sect. 2. Section 3 shows the model evaluation. Results and discussions are presented in Sect. 4, and the conclusions are summarized in Sect. 5.

2 Methods
2.1 Model configuration

Version 3.7.1 of the online coupled Weather Research and Forecasting with Chemistry (WRF-Chem) model (Grell et al., 2005; Skamarock et al., 2008) is used in this study to explore the impacts of aerosol–radiation interactions on surface-layer O3 in North China. WRF-Chem can simulate gas-phase species and aerosols coupled with meteorological fields and has been widely used to investigate air pollution over North China (M. Gao et al., 2016; Gao et al., 2020; Wu et al., 2020). As shown in Fig. 1, we design two nested model domains with the number of grid points at 57 (west–east) × 41 (south–north) and 37 (west–east) × 43 (south–north) at 27 and 9 km horizontal resolutions, respectively. The parent domain centres at (39∘ N, 117∘ E). The model contains 29 vertical levels from the surface to 50 hPa, with 14 levels below 2 km for the full description of the vertical structure of planetary boundary layer (PBL).

Figure 1Map of the two WRF-Chem modelling domains, with the locations of meteorological (white dots) and environmental (red crosses) observation sites used for model evaluation.

Table 1Physical parameterization options used in the simulation.

Download Print Version | Download XLSX

The Carbon Bond Mechanism Z (CBM-Z) is selected as the gas-phase chemical mechanism (Zaveri and Peters, 1999), and the full eight-bin MOSAIC (Model for Simulating Aerosol Interactions and Chemistry) module with aqueous chemistry is used to simulate aerosol evolution (Zaveri et al., 2008). The photolysis rates are calculated by the Fast-J scheme (Wild et al., 2000). Other major physical parameterizations used in this study are listed in Table 1.

The initial and boundary meteorological conditions are provided by the National Centers for Environmental Prediction (NCEP) Final (FNL) analysis data, with a spatial resolution of 1∘ × 1∘. In order to limit the model bias of simulated meteorological fields, the four-dimensional data assimilation (FDDA) is used with the nudging coefficient of 3.0 × 10−4 for wind, temperature, and humidity (no analysis nudging is applied for the inner domain; Lo et al., 2008; Otte, 2008). Chemical initial and boundary conditions are obtained from the Model for Ozone and Related chemical Tracers, version 4 (MOZART-4), forecasts (Emmons et al., 2010).

Anthropogenic emissions in these four episodes are taken from the Multi-resolution Emission Inventory for China (MEIC; http://www.meicmodel.org/, last access: 24 March 2022; M. Li et al., 2017). These emission inventories provide emissions of sulfur dioxide (SO2), nitrogen oxides (NOx), carbon monoxide (CO), non-methane volatile organic compounds (NMVOCs), carbon dioxide (CO2), ammonia (NH3), black carbon (BC), organic carbon (OC), PM10 (particulate matter with an aerodynamic diameter of 10 µm and less), and PM2.5. Emissions are aggregated from four sectors, including power generation, industry, residential, and transportation, with 0.25∘ × 0.25∘ spatial resolution. Biogenic emissions are calculated online by the Model of Emissions of Gases and Aerosols from Nature (MEGAN; Guenther et al., 2006).

2.2 Numerical experiments

To quantify the impacts of API and ARF on O3, the following three experiments have been conducted: (1) BASE – the base simulation coupled with the interactions between aerosol and radiation, which includes both impacts of API and ARF; (2) NOAPI – the same as the BASE case but the impact of API is turned off (aerosol optical properties are set to zero in the photolysis module), following Wu et al. (2020); and (3) NOALL – both the impacts of API and ARF are turned off (removing the mass of aerosol species when calculating aerosol optical properties in the optical module), following Qiu et al. (2017). The differences between BASE and NOAPI (i.e. BASE minus NOAPI) represent the impacts of API. The contributions from ARF can be obtained by comparing NOAPI and NOALL (i.e. NOAPI minus NOALL). The combined effects of API and ARF on O3 concentrations can be quantitatively evaluated by the differences between BASE and NOALL (i.e. BASE minus NOALL).

All the experiments in Episode1, Episode2, Episode3, and Episode4 are conducted from 26 July to 3 August 2014, 6–13 July 2015, 3–11 June 2016, and 26 June to 3 July 2017, respectively, with the first 40 h as the model spin-up in each case. Simulation results from the BASE cases of the four episodes are used to evaluate the model performance.

2.3 Observational data

Simulation results are compared with meteorological and chemical measurements. The surface-layer meteorological data (2 m temperature (T2), 2 m relative humidity (RH2), and 10 m wind speed (WS10)) with the temporal resolution of 3 h at 10 stations (Table S1 in the Supplement) are obtained from NOAA's National Climatic Data Center (https://www.ncei.noaa.gov/maps/hourly/, last access: 24 March 2022). The radiosonde data of temperature at 08:00 and 20:00 LST in Beijing (39.93∘ N, 116.28∘ E) are provided by the University of Wyoming (http://weather.uwyo.edu/, last access: 24 March 2022). Observed hourly concentrations of PM2.5 and O3 at 32 sites (Table S2) in North China are collected from the China National Environmental Monitoring Center (CNEMC). The photolysis rate of nitrogen dioxide (J[NO2]) measured at the Peking University site (39.99∘ N, 116.31∘ E) is also used to evaluate the model performance. More details about the measurement technique of J[NO2] can be found in Wang et al. (2019). The aerosol optical depth (AOD) at the Beijing site (39.98∘ N, 116.38∘ E) is provided by AERONET (level 2.0; http://aeronet.gsfc.nasa.gov/, last access: 24 March 2022). The AODs at 675 and 440 nm are used to derive the AOD at 550 nm to compare with the simulated ones.

Figure 2Time series of observed (black) and simulated (red) hourly surface (a) PM2.5 and (b) O3 concentrations averaged over the 32 observation sites in Beijing, Tianjin, and Baoding during 28 July to 3 August 2014 (Episode1; a1 and b1), 8–13 July 2015 (Episode2; a2 and b2), 5–11 June 2016 (Episode3; a3 and b3), and 28 June to 3 July 2017 (Episode4; a4 and b4). The error bars represent the standard deviations. The calculated index of agreement (IOA), mean bias (MB), normalized mean bias (NMB), and root mean square error (RMSE) are also shown.

Download

2.4 Integrated process rate analysis

Integrated process rate (IPR) analysis has been widely used to quantify the contributions of different processes to O3 variations (Goncalves et al., 2009; J. Gao et al., 2016; Gao et al., 2018; Tang et al., 2017). In this study, four physical/chemical processes are considered, including vertical mixing (VMIX), net chemical production (CHEM), horizontal advection (ADVH), and vertical advection (ADVZ). VMIX is initiated by turbulent process and closely related to PBL development, which influences O3 vertical gradients. CHEM represents the net O3 chemical production (chemical production minus chemical consumption). ADVH and ADVZ represent transport by winds (J. Gao et al., 2016). In this study, we define ADV as the sum of ADVH and ADVZ.

3 Model evaluation

(Content truncated due to size limit. Use line ranges to read remaining content)