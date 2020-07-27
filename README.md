# covid19

This script has been developed with the aim to provide some insight into the current covid19 pandemic. The first step was to aggregate the data by continent (an information hardly available anywhere). The second step is just a regular comparison by countries selected by the user.

<b>Prerequisites</b>

To properly run it needs some Python libraries listed in the prerequisitie file.

<b>Output</b>

There are 3 main outputs:

 <ul>
  <li>some generic data with total cases so far and last day increment;</li>
  <li>4 graphs with total and daily cases and total and daily deaths;</li>
  <li>a csv with the data and the daily changes for the continents or the selected countries</li>
</ul> 

<b>Issues and Future Developments</b>

The code to get the data from some online csv (<a href="https://github.com/CSSEGISandData/COVID-19">Github Repo</a>) need some deeps improvement since it's running pretty inefficiently - it's downloading all the data evrytime even if there is already something previously downloaded. 
I'll try to run this part more efficiently storing the data locally and adding only what is missing.
