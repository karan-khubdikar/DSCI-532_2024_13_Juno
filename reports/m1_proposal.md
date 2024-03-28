---
editor_options: 
  markdown: 
    wrap: 72
---

# 1. Motivation and purpose

Our role: Data science consultants

Target audience: Employment policy makers

There is a lot of data on gender biases in employment and on gender bias
in leadership roles. Our dashboard can be used as a tool to explore this
data. Since our dashboard will allow for interactivity by filtering
based on year, province, industry, etc, it could allow policy makers to
identify where gender biases might be most extreme/most important to
address. Our tool will save policy makers time by presenting the data in
an easy to use and interpretable manner which will help them to make
efficient use of resources. This prevents them from having to do the
"groundwork" of getting data and cleaning it etc which is not how policy
makers should be spending their time. Furthermore, our dashboard will
summarise important information so that policymakers can easily explore
both general and specific trends in gender representation interactively.

# 2. Description of the data

The data is obtained from Statistics Canada. Table 33-10-0501-01
Representation of women and men on boards of directors and in officer
positions, by firm attributes (DOI:
<https://doi.org/10.25318/3310050101-eng>)

Statistics Canada's Representation of women and men on boards of
directors and in officer positions, by firm attributes data highlight
women in leadership and strategic decision-making roles and women that
lead the day-to-day operations within corporations conducting business
in Canada. It allows the user to compare and analyze data based on
industry, size (assets), province, country of control and type of
corporation. For the purpose of this project, we only wish to focus on
Canadian companies (we currently have 303,000 rows of data).

We will work with the following data points: 1. Gender 2. Size of
corporation (number of employees and size of company) 3. Type of
industry 4. Position of the employee (Director, Top officers or Other
officer)

# 3. Research questions

Marci is the Minister for Women and Gender Equality and Youth of Canada,
and she is interested in developing new policies to improve gender
equality in the workplace in Canada. Specifically, she is keen to
explore improving gender equality in top-level management positions.
Since she is in the beginning phases of policymaking, she wants to be
able to get an overview of the proportion of females and males in
top-level managerial positions in different industries in Canada. To
make the most efficient use of her ministry's resources, she wants to be
able to identify specific provinces and industries which are performing
exceptionally well or badly in terms of gender inequality in these
positions. This information will help her to decide on which
stakeholders to consult in the policymaking process, as well as to
consider which provinces and industries she should concentrate her
efforts in.

When Marci opens our 'Girl Boss' app, she will see a map of Canada,
which she can use as a filtering tool to choose which province(s) she
wants to look at. She can also choose which industries and time periods
she wants to examine. Based on the selected subset, she will be able to
view graphs showing both the overall gender makeup of the top-level
positions in that province, and in each industry. In addition, she will
also be able to see how the trends have changed over time, using the
time period she has selected. After exploring different subsets, Marci
realizes that the construction industry has shown marked improvement in
gender equality from 2017 to 2020 on the whole, while the energy
industry in British Columbia seems to have had disproportionally more
men in top-level leadership positions all this time. In fact, she
realizes that, after the pandemic in 2020, the gap between males and
females in executive positions in the energy industry in BC increased
dramatically, and this alarms her.

As a result, Marci decides to consult industry leaders and experts in
the construction industry to understand the changes they made to
encourage more gender-equal outcomes, while commissioning a directorate
based in British Columbia to investigate ways to improve gender equality
in the province, with a special focus on the energy industry.

# 4. App sketch and description

<img src="/img/sketch.png" title="App sketch"/>

The app contains the landing page which shows the graph containing the %
of women in the top leadership positions for all the provinces in
Canada. The left-hand side of the page contains the filters to be
applied to dive further. Filter options are available for province,
year, and checklist for the corporation type and industries. The user
can select a specific province to look into or restrict the year for
which they want to consider the data. The province can be selected by
clicking on the map or by using the dropdown. The top right corner
displays the overall percentage of women and men and based on the
filters applied, these numbers would be updated. Just below these
overall numbers, we have 2 graphs, a pie chart showing the distribution
across industries and a bar graph showing the distribution across the
corporation types. We also have a line graph below the map which depicts
the yearly trend showing the % of women and men at the top positions.
