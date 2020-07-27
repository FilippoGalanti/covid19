# covid19 Visualizations

This script has been developed with the aim to provide some insight into the current covid19 pandemic. The first step was to aggregate the data by continent (an information hardly available anywhere). The second step is just a regular comparison by countries selected by the user.

<b>Prerequisites</b>

To properly run it needs some Python libraries listed in the prerequisitie file.

<b>Output</b>

There are 3 main outputs:

 <ul>
  <li>some generic data with total cases so far and last day increment;</li>

<PRE> 
               Confirmed  Deaths Mortality  Cases Increase  Death Increase
All             16252541  648637     3.99%          204606            4104
North America    4992574  205653     4.12%           66691            1606
Asia             3902392   89931     2.30%           73109            1317
South America    3717194  133525     3.59%           33510             754
Europe           2775971  201563     7.26%           12509             176
Africa            847109   17767     2.10%           18232             245
Oceania            16580     183     1.10%             555               6
Other                721      15     2.08%               0               0
World Records: most cases 282,756 on 7/23/20 - most deaths 9,966 on 7/23/20.
</PRE> 
  <li>4 graphs with total and daily cases and total and daily deaths;</li>
  
  <img src="https://raw.githubusercontent.com/FilippoGalanti/covid19/master/Covid19_Continents.png" alt="Output Example">
  
  <li>a csv with the data and the daily changes for the continents or the selected countries</li>
</ul> 

<b>Issues and Future Developments</b>

The code to get the data from some online csv (<a href="https://github.com/CSSEGISandData/COVID-19">COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University</a>) need some deeps improvement since it's running pretty inefficiently - it's downloading all the data evrytime even if there is already something previously downloaded. 
I'll try to run this part more efficiently storing the data locally and adding only what is missing.
