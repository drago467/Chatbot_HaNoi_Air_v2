 are halved (TMI0.5 scenario), a similar pHsurf and PS(VI),surf is predicted as in the TMI0 scenario. When both FS
 and FS
 are doubled (TMI2 scenario), PS(VI),surf increases by ∼300 % and pHsurf decreases to 4.6. Our results indicate that sulfate production is rather sensitive to the availability of TMI species. Unfortunately, the concentrations, as well as sources, of TMI species in aerosol water during haze episodes remain not well constrained or understood. The simulated mean concentrations of Fe3+ and Mn2+ in PM2.5 at the Beijing TSU site are 3.2 and 3.6 ng m−3, respectively, and they are smaller than the observed concentrations of soluble Fe and Mn (1.5–16 and 10–41 ng m−3, respectively) in PM2.5 at a Xi'an site (Wang et al., 2016). Note that 
 ions also have an anthropogenic source and were estimated to account for 10 %–30 % of ions in Beijing (Shao et al., 2019). Furthermore, the soluble Fe∕Mn speciation (including Fe3+–Fe2+ and Mn2+–Mn3+–Mn4+ cycling) depends on dust mineralogy, particle acidity, and heterogeneous redox reactions (Takahashi et al., 2011; Schroth et al., 2009), and it is very difficult to be explicitly treated. The activity coefficients for 
 ions under the high ionic strength environment might also differ (Cheng et al., 2016). The treatment of the TMI pathway should be further improved in future studies.

Different phase state assumptions predict slightly different pHsurf but distinct sulfate production. Compared with CTRL scenario, assuming a fixed metastable phase state (MSTB scenario) predicts a slightly lower pHsurf (5.0) and 40 % higher PS(VI),surf, and the contribution of the TMI pathway increases. Assuming a fixed stable phase state predicts a slightly higher pH (5.3) and 25 % lower PS(VI),surf (maybe mainly due to the changes in predicted aerosol water content), and the contribution of the NO2 pathway increases. Previous box model studies reported a similar finding regarding the minor impacts of phase state assumption on pH (Song et al., 2018).

4 Conclusions

The focus of the current study is to investigate the spatiotemporal variabilities of aerosol pH and regime transitions of sulfate formation at a regional scale. For this purpose, an aerosol water chemistry (AWAC) module for sulfate and nitrate formation in aerosol water was developed and implemented using the results (including aerosol water and pH) of the revised ISORROPIA II model as input data. With this improved version of Weather Research Forecasting Model with Chemistry (WRF-Chem), we simulated the severe and successive haze pollution spreading over the North China Plain during January 2013. Control experiments could reproduce well the observed inorganic components of fine particles (including sulfate, nitrate, ammonium, chloride, sodium, and crustal minerals), as well as SO2, NO2, O3, and relative humidity, compared to the observations at the Beijing Tsinghua University site. Impacts of the uncertainties in parameters and assumptions have also been discussed.

The vertical profile and diurnal cycle pattern for aerosol pH were closely associated with the spatiotemporal variation in the abundance of acidic and alkaline fine particle components and their gaseous counterparts. The competition between the ammonia, crustal particles, and acidic components (such as sulfate and nitrate) could play an important role in determining pH in different vertical layers. The monthly mean pH at the surface layer exhibited a large spatial variability over the North China Plain. Mean pH was greater than 6 for the areas with higher latitudes north of 41∘ N (mainly influenced by the abundant crustal particles) and was mostly between 4.4 and 5.7 (10 % and 90 % quantiles, respectively) for vast areas south of ∼41∘ N (with NHx as the driving factor) over the North China Plain. The trend that aerosol acidity was enhanced with increasing altitude was consistent for all latitudes (35–43∘ N) investigated, while the vertical gradients of pH varied between different locations. The diurnal cycle pattern existed only for the domain-wide cells in the lower boundary layer, in which nighttime pH was higher.

In the AWAC module, six sulfate formation pathways in aerosol water are implemented and compared, namely aqueous-phase oxidation by dissolved O3, NO2, H2O2, TMI (in the presence of O2) and CH3OOH, as well as gas-particle partitioning of H2SO4 vapor (GPP). The relative contributions of different sulfate formation pathways in aerosol water depended on both pH and the concentrations of each oxidant/catalyst. At the surface layer, O3, NO2, TMI, and H2O2 pathways were the most important in different locations over the North China Plain, and four regions with three distinct regimes have been found. With the increasing height, O3, TMI, and GPP pathways became more important, while contributions from NO2 and H2O2 pathways decreased rapidly. At higher altitudes above ∼3 km above ground level, aqueous-phase oxidation in aerosol water became negligible.

The diurnal cycle pattern at the surface layer and altitudinal decrease of pH is consistent for all the sensitivity tests with varying adjusted emission parameters and phase state assumptions except when NH3 emissions are completely removed. The pH is sensitive to the alkalization effect of NH3 and crustal particles; furthermore, the rapid production of sulfate could be maintained over a wide pH range (e.g., 4.2–5.7) with the varying emissions for NH3 and crustal particles (transition from the dominant TMI pathway to the dominant NO2∕O3 pathway). The sulfate production is rather sensitive to the concentrations of TMI species, and doubling the TMI species sources almost triples the sulfate production. Changes in chloride emissions and phase state assumptions both have a relatively minor effect on pH, but sulfate formation could be changed as the predicted aerosol water changes. Our studies suggest that sources of crustal particles, NH3, and TMI species are very important factors for the aqueous-phase chemistry during haze episodes and should be better constrained in future studies. Moreover, the use of a more detailed aqueous-phase mechanism involving the TMI species cycling and radical chain propagation is suggested. Uncertainties relevant to the algorithms to solve the aerosol thermodynamics, including the treatment of non-ideality, size effects, phase state, mixing state, the interactions between inorganic compounds and organic compounds, and phase separation, should also be addressed in future studies.

Data availability

The source code for the aerosol water chemistry module and the data used in this paper are available upon request from the corresponding authors Hang Su (h.su@mpic.de) or Yafang Cheng (yafang.cheng@mpic.de).

Supplement

The supplement related to this article is available online at: https://doi.org/10.5194/acp-20-11729-2020-supplement.

Author contributions

HS and YC designed and led the study. WT developed the AWAC module and implemented the revised ISORROPIA II into WRF-Chem. WT performed model simulations. WT, HS, and YC analyzed data and interpreted the results. GZ supported the data analyses. JW, CW, and LL supported the modeling work. ML and QZ provided the MEIC for the year 2013. All coauthors have discussed the results and commented on the paper. WT wrote the paper with input from all coauthors.

Competing interests

The authors declare that they have no conflict of interest.

Acknowledgements

This study is supported by the Max Planck Society (MPG). Yafang Cheng would like to thank the Minerva program of the MPG.

Financial support

The article processing charges for this open-access publication were covered by the Max Planck Society.

Review statement

This paper was edited by Veli-Matti Kerminen and reviewed by two anonymous referees.

References

Ackermann, I. J., Hass, H., Memmesheimer, M., Ebel, A., Binkowski, F. S., and Shankar, U.: Modal aerosol dynamics model for Europe: development and first applications, Atmos. Environ., 32, 2981–2999, https://doi.org/10.1016/S1352-2310(98)00006-5, 1998. 

Baker, A. R., Jickells, T. D., Witt, M., and Linge, K. L.: Trends in the solubility of iron, aluminium, manganese and phosphorus in aerosol collected over the Atlantic Ocean, Mar. Chem., 98, 43–58, https://doi.org/10.1016/j.marchem.2005.06.004, 2006. 

Brimblecombe, P.: The Big Smoke (Routledge Revivals): A History of Air Pollution in London Since Medieval Times, Routledge, Abingdon, London, UK, 2012. 

Chen, D., Liu, Z., Fast, J., and Ban, J.: Simulations of sulfate–nitrate–ammonium (SNA) aerosols during the extreme haze events over northern China in October 2014, Atmos. Chem. Phys., 16, 10707–10724, https://doi.org/10.5194/acp-16-10707-2016, 2016. 

Chen, T., Chu, B., Ge, Y., Zhang, S., Ma, Q., He, H., and Li, S. M.: Enhancement of aqueous sulfate formation by the coexistence of NO2/NH3 under high ionic strengths in aerosol water, Environ. Pollut., 252, 236–244, https://doi.org/10.1016/j.envpol.2019.05.119, 2019. 

Cheng, Y., Zheng, G., Wei, C., Mu, Q., Zheng, B., Wang, Z., Gao, M., Zhang, Q., He, K., Carmichael, G., Pöschl, U., and Su, H.: Reactive nitrogen chemistry in aerosol water as a source of sulfate during haze events in China, Sci. Adv., 2, e1601530, https://doi.org/10.1126/sciadv.1601530, 2016. 

Claquin, T., Schulz, M., and Balkanski, Y. J.: Modeling the mineralogy of atmospheric dust sources, J. Geophys. Res.-Atmos., 104, 22243–22256, https://doi.org/10.1029/1999jd900416, 1999. 

Clifton, C. L., Altstein, N., and Huie, R. E.: Rate constant for the reaction of nitrogen dioxide with sulfur(IV) over the pH range 5.3–13, Environ. Sci. Technol., 22, 586–589, https://doi.org/10.1021/es00170a018, 1988. 

Damian, V., Sandu, A., Damian, M., Potra, F., and Carmichael, G. R.: The kinetic preprocessor KPP – a software environment for solving chemical kinetics, Comput. Chem. Eng., 26, 1567–1579, https://doi.org/10.1016/S0098-1354(02)00128-X, 2002. 

Ding, J., Zhao, P., Su, J., Dong, Q., Du, X., and Zhang, Y.: Aerosol pH and its driving factors in Beijing, Atmos. Chem. Phys., 19, 7939–7954, https://doi.org/10.5194/acp-19-7939-2019, 2019. 

Dong, X., Fu, J. S., Huang, K., Tong, D., and Zhuang, G.: Model development of dust emission and heterogeneous chemistry within the Community Multiscale Air Quality modeling system and its application over East Asia, Atmos. Chem. Phys., 16, 8157–8180, https://doi.org/10.5194/acp-16-8157-2016, 2016. 

Dufour, G., Eremenko, M., Orphal, J., and Flaud, J.-M.: IASI observations of seasonal and day-to-day variations of tropospheric ozone over three highly populated areas of China: Beijing, Shanghai, and Hong Kong, Atmos. Chem. Phys., 10, 3787–3801, https://doi.org/10.5194/acp-10-3787-2010, 2010. 

Duvall, R. M., Majestic, B. J., Shafer, M. M., Chuang, P. Y., Simoneit, B. R. T., and Schauer, J. J.: The water-soluble fraction of carbon, sulfur, and crustal elements in Asian aerosols and Asian soils, Atmos. Environ., 42, 5872–5884, https://doi.org/10.1016/j.atmosenv.2008.03.028, 2008. 

Fountoukis, C. and Nenes, A.: ISORROPIA II: a computationally efficient thermodynamic equilibrium model for K+–Ca2+–Mg2+–
–Na+–
–
–Cl−–H2O aerosols, Atmos. Chem. Phys., 7, 4639–4659, https://doi.org/10.5194/acp-7-4639-2007, 2007. 

Gen, M. S., Zhang, R. F., Huang, D. D., Li, Y. J., and Chan, C. K.: Heterogeneous oxidation of SO2 in sulfate production during nitrate photolysis at 300 nm: effect of pH, relative humidity, irradiation intensity, and the presence of organic compounds, Environ. Sci. Technol., 53, 8757–8766, https://doi.org/10.1021/acs.est.9b01623, 2019. 

Ginoux, P., Chin, M., Tegen, I., Prospero, J. M., Holben, B., Dubovik, O., and Lin, S. J.: Sources and distributions of dust aerosols simulated with the GOCART model, J. Geophys. Res.-Atmos., 106, 20255–20273, https://doi.org/10.1029/2000jd000053, 2001. 

Grell, G. A., Peckham, S. E., Schmitz, R., McKeen, S. A., Frost, G., Skamarock, W. C., and Eder, B.: Fully coupled “online” chemistry within the WRF model, Atmos. Environ., 39, 6957–6975, https://doi.org/10.1016/j.atmosenv.2005.04.027, 2005. 

Guenther, A., Karl, T., Harley, P., Wiedinmyer, C., Palmer, P. I., and Geron, C.: Estimates of global terrestrial isoprene emissions using MEGAN (Model of Emissions of Gases and Aerosols from Nature), Atmos. Chem. Phys., 6, 3181–3210, https://doi.org/10.5194/acp-6-3181-2006, 2006. 

Guo, H., Sullivan, A. P., Campuzano-Jost, P., Schroder, J. C., Lopez-Hilfiker, F. D., Dibb, J. E., Jimenez, J. L., Thornton, J. A., Brown, S. S., Nenes, A., and Weber, R. J.: Fine particle pH and the partitioning of nitric acid during winter in the northeastern United States, J. Geophys. Res.-Atmos., 121, 10355–10376, https://doi.org/10.1002/2016jd025311, 2016. 

Hsu, S. C., Wong, G. T. F., Gong, G. C., Shiah, F. K., Huang, Y. T., Kao, S. J., Tsai, F. J., Lung, S. C. C., Lin, F. J., Lin, I. I., Hung, C. C., and Tseng, C. M.: Sources, solubility, and dry deposition of aerosol trace elements over the East China Sea, Mar. Chem., 120, 116–127, https://doi.org/10.1016/j.marchem.2008.10.003, 2010. 

Huang, J., Minnis, P., Chen, B., Huang, Z., Liu, Z., Zhao, Q., Yi, Y., and Ayers, J. K.: Long-range transport and vertical structure of Asian dust from CALIPSO and surface measurements during PACDEX, J. Geophys. Res.-Atmos., 113, D23212, https://doi.org/10.1029/2008JD010620, 2008. 

Ibusuki, T. and Takeuchi, K.: Sulfur-dioxide oxidation by oxygen catalyzed by mixtures of manganese(Ii) and iron(Iii) in aqueous-solutions at environmental reaction conditions, Atmos. Environ., 21, 1555–1560, https://doi.org/10.1016/0004-6981(87)90317-9, 1987. 

Jacob, D. J. and Brasseur, G. P.: Formulations of Radiative, Chemical, and Aerosol Rates, in: Modeling of Atmospheric Chemistry, Cambridge University Press, Cambridge, 205–252, 2017. 

Johnson, M. S., Meskhidze, N., Solmon, F., Gasso, S., Chuang, P. Y., Gaiero, D. M., Yantosca, R. M., Wu, S. L., Wang, Y. X., and Carouge, C.: Modeling dust and soluble iron deposition to the South Atlantic Ocean, J. Geophys. Res.-Atmos., 115, D15202, https://doi.org/10.1029/2009jd013311, 2010. 

Journet, E., Desboeufs, K. V., Caquineau, S., and Colin, J. L.: Mineralogy as a critical factor of dust iron solubility, Geophys. Res. Lett., 35, L07805 https://doi.org/10.1029/2007gl031589, 2008. 

Kong, L., Tang, X., Zhu, J., Wang, Z., Pan, Y., Wu, H., Wu, L., Wu, Q., He, Y., and Tian, S.: Improved inversion of monthly ammonia emissions in China in combination of the Chinese Ammonia Monitoring Network and ensemble Kalman filter, Environ. Sci. Technol., 53, 12529–12538, https://doi.org/10.1021/acs.est.9b02701, 2019. 

Kong, X., Forkel, R., Sokhi, R. S., Suppan, P., Baklanov, A., Gauss, M., Brunner, D., Barò, R., Balzarini, A., Chemel, C., Curci, G., Jiménez-Guerrero, P., Hirtl, M., Honzak, L., Im, U., Pérez, J. L., Pirovano, G., San Jose, R., Schlünzen, K. H., Tsegas, G., Tuccella, P., Werhahn, J., Žabkar, R., and Galmarini, S.: Analysis of meteorology–chemistry interactions during air pollution episodes using online coupled models within AQMEII phase-2, Atmos. Environ., 115, 527–540, https://doi.org/10.1016/j.atmosenv.2014.09.020, 2015. 

Lee, Y. N. and Schwartz, S. E.: Precipitation Scavenging, in: Dry Deposition and Resuspension, Elsevier, New York, USA, 453–470, 1983. 

Lei, Y., Zhang, Q., He, K. B., and Streets, D. G.: Primary anthropogenic aerosol emission trends for China, 1990–2005, Atmos. Chem. Phys., 11, 931–954, https://doi.org/10.5194/acp-11-931-2011, 2011. 

Li, M., Zhang, Q., Streets, D. G., He, K. B., Cheng, Y. F., Emmons, L. K., Huo, H., Kang, S. C., Lu, Z., Shao, M., Su, H., Yu, X., and Zhang, Y.: Mapping Asian anthropogenic emissions of non-methane volatile organic compounds to multiple chemical mechanisms, Atmos. Chem. Phys., 14, 5617–5638, https://doi.org/10.5194/acp-14-5617-2014, 2014. 

Li, G., Bei, N., Cao, J., Huang, R., Wu, J., Feng, T., Wang, Y., Liu, S., Zhang, Q., Tie, X., and Molina, L. T.: A possible pathway for rapid growth of sulfate during haze days in China, Atmos. Chem. Phys., 17, 3301–3316, https://doi.org/10.5194/acp-17-3301-2017, 2017a. 

(Content truncated due to size limit. Use line ranges to read remaining content)