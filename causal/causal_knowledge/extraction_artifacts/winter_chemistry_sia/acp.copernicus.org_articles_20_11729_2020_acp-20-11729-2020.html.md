
**URL:** https://acp.copernicus.org/articles/20/11729/2020/acp-20-11729-2020.html

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
Volume 20, issue 20
ACP, 20, 11729–11746, 2020
https://doi.org/10.5194/acp-20-11729-2020
© Author(s) 2020. This work is distributed under
the Creative Commons Attribution 4.0 License.
Article
Peer review
Metrics
Related articles
Research article
 | 
17 Oct 2020
Aerosol pH and chemical regimes of sulfate formation in aerosol water during winter haze in the North China Plain
Wei Tao, Hang Su, Guangjie Zheng, Jiandong Wang, Chao Wei, Lixia Liu, Nan Ma, Meng Li, Qiang Zhang, Ulrich Pöschl, and Yafang Cheng
Abstract

Understanding the mechanism of haze formation is crucial for the development of deliberate pollution control strategies. Multiphase chemical reactions in aerosol water have been suggested as an important source of particulate sulfate during severe haze (Cheng et al., 2016; Wang et al., 2016). While the key role of aerosol water has been commonly accepted, the relative importance of different oxidation pathways in the aqueous phase is still under debate mainly due to questions about aerosol pH. To investigate the spatiotemporal variability of aerosol pH and sulfate formation during winter in the North China Plain (NCP), we have developed a new aerosol water chemistry (AWAC) module for the WRF-Chem model (Weather Research and Forecasting model coupled with Chemistry). Using the WRF-Chem-AWAC model, we performed a comprehensive survey of the atmospheric conditions characteristic for wintertime in the NCP focusing on January 2013. We find that aerosol pH exhibited a strong vertical gradient and distinct diurnal cycle which was closely associated with the spatiotemporal variation in the abundance of acidic and alkaline fine particle components and their gaseous counterparts. Over Beijing, the average aerosol pH at the surface layer was ∼5.4 and remained nearly constant around ∼5 up to ∼2 km above ground level; further aloft, the acidity rapidly increased to pH ∼0 at ∼3 km. The pattern of aerosol acidity increasing with altitude persisted over the NCP, while the specific levels and gradients of pH varied between different regions. In the region north of ∼41∘ N, the mean pH values at the surface level were typically greater than 6, and the main pathway of sulfate formation in aerosol water was S(IV) oxidation by ozone. South of ∼41∘ N, the mean pH values at the surface level were typically in the range of 4.4 to 5.7, and different chemical regimes and reaction pathways of sulfate formation prevailed in four different regions depending on reactant concentrations and atmospheric conditions. The NO2 reaction pathway prevailed in the megacity region of Beijing and the large area of Hebei Province to the south and west of Beijing, as well as part of Shandong Province. The transition metal ion (TMI) pathway dominated in the inland region to the west and the coastal regions to the east of Beijing, and the H2O2 pathway dominated in the region extending further south (Shandong and Henan provinces). In all of these regions, the O3 and TMI pathways in aerosol water, as well as the gas-particle partitioning of H2SO4 vapor, became more important with increasing altitude. Sensitivity tests show that the rapid production of sulfate in the NCP can be maintained over a wide range of aerosol acidity (e.g., pH =4.2–5.7) with transitions from dominant TMI pathway regimes to dominant NO2∕O3 pathway regimes.

How to cite. 

Tao, W., Su, H., Zheng, G., Wang, J., Wei, C., Liu, L., Ma, N., Li, M., Zhang, Q., Pöschl, U., and Cheng, Y.: Aerosol pH and chemical regimes of sulfate formation in aerosol water during winter haze in the North China Plain, Atmos. Chem. Phys., 20, 11729–11746, https://doi.org/10.5194/acp-20-11729-2020, 2020.

Received: 25 Feb 2020 – Discussion started: 06 Apr 2020 – Revised: 07 Aug 2020 – Accepted: 26 Aug 2020 – Published: 17 Oct 2020
1 Introduction

Persistent haze shrouding Beijing and its surrounding areas in the North China Plain during cold winters is one of the most urgent and challenging environmental problems in China (Sun et al., 2014; G. J. Zheng et al., 2015; Cheng et al., 2016; Su et al., 2020). The winter haze often has the following characteristic features, including stagnant meteorological conditions, high relative humidity, and high concentrations of PM2.5, as well as elevated contributions of secondary inorganics in PM2.5 (Zhang et al., 2014; Brimblecombe, 2012; G. J. Zheng et al., 2015; Sun et al., 2014). Although extremely sharp increases in PM2.5 concentration in Beijing (e.g., several hundred 
) have been attributed mainly to the transport processes rather than local chemical production, the large gap between modeled and observed PM2.5 reveals that there are still missing chemical formation pathways in the state-of-the-art atmospheric chemical transport models (G. J. Zheng et al., 2015; Cheng et al., 2016). Cheng et al. (2016) suggested and quantified that during severe haze, multiphase reactions in aerosol water can produce a remarkable amount of sulfate over a wide range of aerosol pH values which complements or even exceeds the contribution from gas-phase and cloud chemistry during the haze events. Laboratory studies of Wang et al. (2016) provide an experimental proof of the importance of the NO2 oxidation pathway in sulfate formation in aerosol water. However, depending on the aerosol pH and pollutant compositions, the major multiphase oxidation pathways may change from reactions of NO2 and O3 at pH greater than 4.5 to O2 (catalyzed by transition metal ion, TMI) and H2O2 at pH less than 4.5 (Cheng et al., 2016). Unlike the negative feedback between aerosol loadings and their photochemical production (Makar et al., 2015; Kong et al., 2015), the multiphase reactions induce a positive feedback mechanism, i.e., higher particle matter levels lead to more aerosol water, which accelerates sulfate production and further increases the aerosol concentration (G. J. Zheng et al., 2020; Su et al., 2020; Cheng et al., 2016).

Although the importance of reactions in aerosol water during severe haze has been widely accepted (Li et al., 2017a; Chen et al., 2016, 2019; G. J. Zheng et al., 2015; Cheng et al., 2016; Zhang et al., 2015; Wang et al., 2016; Shao et al., 2019; Xue et al., 2019; Gen et al., 2019; Wu et al., 2019), the exact formation pathway is still under debate. Besides the aforementioned reactions (i.e., reactions of NO2, O3, TMI, and H2O2), the heterogeneous production of hydroxymethanesulfonate (HMS) by SO2 and HCHO has also been proposed as contributing to the unexplained sulfate in models (Song et al., 2019; Moch et al., 2018). To a certain extent, this is not a surprise considering the strong dependence of the multiphase reaction rate on aerosol pH and pollutant compositions (including the most important oxidants for sulfate formation). Hourly predicted pH based on observations and thermodynamic model calculations showed a large variability from 2 to 8 in northern China (Shi et al., 2017; Ding et al., 2019). Previous observational and modeling studies also indicated that the temporal and spatial distribution of oxidants and catalysts, e.g., O3 (Dufour et al., 2010; Xu et al., 2008), NO2 (Zhang et al., 2012; Zhang et al., 2007), and TMI (Dong et al., 2016), was highly variable.

Thus, we hypothesize that multiple oxidation regimes for sulfate formation may indeed coexist in the North China Plain. The apparent contrasting results could be a consequence of regime transitions between different locations and periods. To test our hypothesis, we have developed a new aerosol water chemistry (AWAC) module and implemented an improved version of ISORROPIA II into the WRF-Chem model (Weather Research and Forecasting model coupled with Chemistry) to better account for the different sulfate formation pathways. With a comprehensive model survey, we focus on the variabilities of aerosol pH and regimes of sulfate formation in aerosol water with the aim of reconciling the continuing debates on the dominating sulfate formation pathways in the North China Plain. Detailed method description and model evaluation are provided in Sect. 2, followed by the results and discussion in Sect. 3. The last section summarizes the main conclusions and implications of this study.

2 Method
2.1 WRF-Chem-AWAC: new aerosol water chemistry module for WRF-Chem

To account for the formation of sulfate and nitrate in the liquid water of fine particles (including Aitken and accumulation modes and denoted as PM2.5), we have developed a new aerosol water chemistry (AWAC) module into WRF-Chem (version 3.8) (Grell et al., 2005). The coarse mode aerosols have been greatly simplified in the MADE/SORGAM framework, and the AWAC module is therefore not implemented for coarse mode aerosols. For sulfate (denoted as PM25_SO4) formation, we use explicit mechanisms involving 11 irreversible reactions for the oxidation of S(IV) by dissolved O3, H2O2, TMI (only Fe3+ and Mn2+ are considered), NO2, and CH3OOH (Table 1). The mass transfer of SO2 and gaseous oxidants between gas and liquid phases, as well as the dissociation equilibrium of sulfurous acid, is treated as an irreversible reaction and solved simultaneously with the redox reactions using KPP software (Damian et al., 2002; Sandu and Sander, 2006) and the Rosenbrock solver (Sandu et al., 1997; Shampine, 1982). The formula for the mass transfer rate coefficient, kT (in cm s−1), is adopted from Jacob and Brasseur (2017):

where Rd is the mean radius for fine particles (including aerosol water; in cm), Dg is the molecular diffusion coefficient (cm2 s−1), R is the gas constant (8.314 J mol−1 K−1), T is the air temperature (K), Mw is the molecular weight (kg mol−1), and α is the mass accommodation coefficient (unitless). Detailed descriptions are provided in the Supplement (Figs. S1–S5 and Tables S1–S5). Although using different solvers, the box model version of the aerosol water chemistry module could reproduce well the results in Cheng et al. (2016) (shown in Fig. S5 of Supplement).

Table 1Rate expressions and rate constants for the S(IV) oxidation reactions in the aerosol water.

* The rate coefficient k6 (in M−1 s−1) is expressed as follows: 
,
where 
 M−1 s−1, 
 M−1 s−1, 
 M−1 s−1, 
 M−1 s−1.

Download Print Version | Download XLSX

Following B. Zheng et al. (2015) and Chen et al. (2016), a parameterization scheme is adopted to simulate the aqueous-phase production of nitrate (denoted as PM25_NO3):

where Aa is the surface area concentration of fine particles (cm2 cm−3) and γ is the uptake coefficient (unitless) for NO2. The uptake coefficient γ has a lower limit (
) and a higher limit (
) when the relative humidity (RH) is lower than 50 % and higher than 90 %, respectively. Note that the γ has been scaled 15 times lower than that used in B. Zheng et al. (2015) to better match the observed PM25_NO3 with R=0.74 and NMB =3 % (normalized mean bias; see more details in Sect. 3.1). When the RH ranges between 50 % and 90 %, the value for γ is then linearly interpolated between the two limits.

To simulate aerosol water content (AWC) and pH as input parameters of the AWAC module, we have replaced the original ISORROPIA model in WRF-Chem with an improved version of ISORROPIA II (Fountoukis and Nenes, 2007; Song et al., 2018). The source code of the improved ISORROPIA II is available at http://wiki.seas.harvard.edu/geos-chem/index.php/ISORROPIA_II (last access: 6 October 2020). ISORROPIA predicts the thermodynamic equilibrium (including pH) for an internal-mixed system of multiple inorganic components at a specific temperature and humidity. Following Ding et al. (2019), we assume that the phase state for aerosol is metastable at RH >30 %; otherwise the phase state is stable. If the predicted AWC is less than an infinitesimal value (the threshold value of 10−8 µg m−3 is used; see Figs. S6 and S7 of Supplement for relevant uncertainties), pH is set to a missing value, and heterogeneous reactions in aerosol water are not calculated. Otherwise the heterogeneous oxidation module is called assuming a fixed number and/or size distribution and thermodynamic status (including AWC and pH) within one time step of the master chemistry module in WRF-Chem program.

The RACM mechanism (Stockwell et al., 1997, 1990) is used to calculate the gas-phase photochemistry and provides the concentrations of gaseous precursors (e.g., SO2, NO2, etc.) and oxidants (e.g., O3, H2O2, etc.). The MADE/SORGAM scheme (Ackermann et al., 1998; Schell et al., 2001) with the improved ISORROPIA II model is used to simulate the aerosol dynamics (including nucleation, coagulation, and condensation) and thermodynamics and provide the aerosol's size distribution and number concentration, as well as AWC and pH values. The integrated process rate (IPR) technique (Tao et al., 2017, 2015) is used to record the formation rates of sulfuric and nitric acid vapor through photochemical oxidation in the gas phase.

For the TMI oxidation pathway, we assume that Fe3+ and Mn2+ will not be consumed in the TMI pathway due to the catalytic nature of 
. The concentrations of Fe3+ and Mn2+ (in mol L−1) in aerosol water can be calculated by Eq. (3):

where PM25_FE and PM25_MN are the fine particle components of Fe and Mn minerals, respectively, C denotes the concentrations in moles per liter of air, FS
 and FS
 represent the maximum fractional solubility of Fe3+ and Mn2+, respectively (regardless of the acidity of aerosol water), and AWC is the aerosol liquid water content in liters per liter of air.

2.2 WRF-Chem model configuration and scenarios

The modeling framework is constructed on a single domain of 100 (west–east) ×70 (south–north) ×30 (vertical layers) grid cells with a horizontal resolution of 20 km (including the Gobi Desert; see Fig. S8 of Supplement). The overview of the chemical and physical options used in this study is summarized in Table S6 of Supplement. The Madronich F-TUV photolysis scheme (Madronich, 1987) is used to calculate the photolysis rates. The initial and boundary conditions for meteorology and chemistry are derived from 
 National Center for Environmental Prediction Final (NCEP FNL) data and global-scale MOZART outputs, respectively. Observation nudging (Liu et al., 2005) is used to nudge the modeled temperature, wind fields, and humidity towards the observations (including surface and upper layers). The multi-resolution Emission Inventory for China (MEIC) of the year 2013 (Lei et al., 2011; Zhang et al., 2009; Li et al., 2014, 2017b) is used for anthropogenic emissions. The Megan scheme (Guenther et al., 2006) is used for biogenic volatile organic compound emissions. The hourly biomass burning emissions data are provided by the fire inventory from the National Center for Atmospheric Research (NCAR) (FINN; Wiedinmyer et al., 2011). We use the GOCART dust scheme (Ginoux et al., 2001; Zhao et al., 2010, 2013), which is coupled with the MADE/SORGAM aerosol scheme.

(Content truncated due to size limit. Use line ranges to read remaining content)