# Reflections

## Additional Features

To load our data more efficiently, we switched to using binary parquet files instead of csv to store our data. We also utilized caching to improve performance.

We made major layout and stylistic changes based on feedback from both our peers and Joel, including reorganizing the charts, changing the background color, and adding a favicon. We also prevented users from clearing filters, which would result in blank charts, and changed the x-axis labels such that they do not get cut off by the axis. Notably, we made the map reactive, such that it is no longer static, but highlights the selected province on the map. Lastly, we made formatting changes to our charts to improve readability.

## Reflection on Useful Feedback

We appreciated all the feedback we received, as the feedback was professionally worded and well-structured, such that we were able to take concrete action based on the information. Among all the feedback we received, we found the feedback on preferred layouts and formats to be most useful, as we were not able to see the dashboard with fresh eyes prior to hearing from Joel and our peers. Through this, we were able to better understand how different users might find most intuitive in navigating the app, and make changes to improve the overall user experience. Perhaps more feedback on additional charts or statistics users might be interested in would have also been useful, especially if the feedback comes from someone with a fresh perspective.

## Strengths and Future Improvements

We are pleased with our dashboard, as it looks good and performs well, loading quickly both locally and on Render. After making the layout changes suggested by our peers and Joel, we feel that the dashboard is even more intuitive, user-friendly, and aesthetically pleasing. The insights which can be drawn from our dashboard are meaningful, especially with our improved plots, and we are excited for more people to use our dashboard to explore gender inequality in the top-level leadership in Canadian companies.

Given more time, we would have liked to explore different kinds of engineered features and charts. We were toying with the idea of a separate section, perhaps in separate tabs to avoid crowding the page, which would allow users to compare charts and statistics from different industries or provinces against averages from all other industries or provinces. This might be informative for users who might want to do an even deeper dive into the trends in a subset of data, and the comparison not just to the Canadian national average, but to the average of all other industries might also provide insightful directions for exploration in policymaking. These could be future additions to our dashboard.
