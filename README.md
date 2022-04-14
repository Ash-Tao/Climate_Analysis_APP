# SQLAlchemy-challenge

## Target
Use Python and SQLAlchemy to do basic climate analysis and data exploration of giveb climate database. All analysis were completed using `SQLAlchemy ORM queries`, `Pandas`, and `Matplotlib`.<br/>

## Step 1 - Climate Analysis and Exploration
* Use SQLAlchemy `create_engine` to connect to your sqlite database.<br/>

* Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.<br/>

* Link Python to the database by creating an SQLAlchemy session.<br/>
<br/>

### Task 1 - Precipitation Analysis

* Finding the most recent date in the data set.<br/>

* Retrieve the last 12 months of precipitation data.<br/>

* Load the query for selecting only the `date` and `prcp` values into a Pandas DataFrame and set the index to the date column.<br/>

* Sort the DataFrame values by `date`.<br/>

* Plot the results.<br/>
  <img src="https://github.com/Ash-Tao/sqlalchemy-challenge/blob/main/Output/Precipitation%20(2016-08-24%20-%202017-08-23).png"><br/>

* Use Pandas to print the summary statistics for the precipitation data.<br/>

### Task 2 - Station Analysis

* Find the total number of stations in the dataset.<br/>

* Find the most active stations.<br/>

* Retrieve the last 12 months of temperature observation data (TOBS).<br/>

* Plot the results.<br/>
  <img src=https://github.com/Ash-Tao/sqlalchemy-challenge/blob/main/Output/Temperature%20Observation%20(2016-08-24%20-%202017-08-23).png><br/>

* Use Pandas to print the summary statistics for the precipitation data.<br/>

* Close out your session.<br/>
<br/>

## Step 2 - Climate App

* Use Flask to create your routes.<br/>

### Routes

* `/`<br/>
  * Home page.<br/>
  * List all routes that are available.<br/>

* `/api/v1.0/precipitation`<br/>
  * Returns the jsonified precipitation data for the last year in the database.<br/>
  * Use `date` as the key and `prcp` as the value.<br/>
  * Return the JSON representation of your dictionary.<br/>

* `/api/v1.0/stations`
  * Returns jsonified data of all of the stations in the database.<br/>

* `/api/v1.0/tobs`
  * Returns jsonified data for the most active station (USC00519281) for the last year of data.<br/>

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`<br/>
  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br/>
  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.<br/>
  * When given the start and the end date, calculate the dates between the start and end date inclusive.<br/>
<br/>

- - -

## Bonus: Other Analyses

### Temperature Analysis I

__Conclusion:__<br/>
> I will use a paired t-test as we compared the means of the same group. And the lower the p-value, the less likely the results are due purely to chance. i.e. in this case, the mean temperature observations are of the same stations, just for different time points. <br/>
> The null hypothesis (H0): The mean of the paired differences equals zero in the population. <br/>
> The alternative hypothesis (H1): The mean of the paired differences does not equal zero in the population.<br/>
> he p-value,pvalue=3.9025129038616655e-191, I got from the calculation is less than 0.05.<br/>
> If a p-value < 0.05, we should reject the null hypothesis and __accept the alternative hypothesis__.<br/>
> In other words, there is a meaningful difference between the June and December temperatures in Hawaii. This difference has very little to do with the random sampling itself. The variance obtained from the sample is consistent with the actual weather conditions in Hawaii.<br/>
* Use pandas to perform this portion.<br/>
  * Convert the date column format from string to datetime.<br/>
  * Set the date column as the DataFrame index<br/>
  * Drop the date column<br/>

* Identify the average temperature in June at all stations across all available years in the dataset. Repeat on December temperature.<br/>

* Use the t-test to determine whether the difference in the means, if any, is statistically significant.<br/>

### Temperature Analysis II

* Find out what the temperature has previously looked like.<br/>
  > Use the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from a previous year (i.e., use "2017-08-01").<br/>
  * Plot the min, avg, and max temperature as a bar chart.<br/>
    * Use "Trip Avg Temp" as the title.<br/>
    * Use the average temperature as the bar height (y value).<br/>
    * Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).<br/>
      <img src="https://github.com/Ash-Tao/sqlalchemy-challenge/blob/main/Output/Trip%20Avg%20Temp%20(2016-08-01%20-%202016-08-07).png"><br/>
* Daily Rainfall Average<br/>
  > Calculate the rainfall per weather station using the previous year's matching dates.<br/>
  * Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation.<br/>

* Daily Temperature Normals<br/>
  > Use the `daily_normals` function to calculate the averages for the min, avg, and max temperatures for your trip using the matching dates from a previous year. This date string will be in the format `%m-%d`.<br/>
  * Set the start and end date of the trip.<br/>
  * Use the date to create a range of dates.<br/>
  * Strip off the year and save a list of strings in the format `%m-%d`.<br/>
  * Use the `daily_normals` function to calculate the normals for each date string and append the results to a list called `normals`.<br/>
* Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.<br/>
* Use Pandas to plot an area plot (`stacked=False`) for the daily normals.<br/>
  <img src="https://github.com/Ash-Tao/sqlalchemy-challenge/blob/main/Output/Daily%20Temperature%20Normals%20(2016-08-01%20-%202016-08-07).png"><br/>
* Close out your session.<br/>

### Files
- [Output](https://github.com/Ash-Tao/sqlalchemy-challenge/tree/main/Output)<br/>
  - Precipitation (2016-08-24 - 2017-08-23).png<br/>
  - Temperature Observation (2016-08-24 - 2017-08-23).png<br/>
  - Daily Temperature Normals (2016-08-01 - 2016-08-07).png<br/>
  - Daily Temperature Normals (2016-08-01 - 2016-08-07).png<br/>

- [Jupyter Notebook](https://github.com/Ash-Tao/sqlalchemy-challenge/tree/main/Jupyter%20Notebook)<br/>
  - climate.ipynb<br/>
  - temp_analysis_bonus_1.ipynb<br/>
  - temp_analysis_bonus_w.ipynb<br/>
- [Climate App](https://github.com/Ash-Tao/sqlalchemy-challenge/blob/main/app.py)<br/>
