#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[11]:


# Calculate the Totals (Schools and Students)
school_count = len(school_data_complete["school_name"].unique())
student_count = school_data_complete["Student ID"].count()

# Calculate the Total Budget
total_budget = school_data["budget"].sum()

# Calculate Avg. Math Score
math_score = school_data[""]


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[13]:


# Determine the School Type
school_types = school_data.set_index(["school_name"])["type"]

# Calculate the total student count
per_school_counts = school_data_complete["school_name"].value_counts()

# Calculate the total school budget and per capita spending
# per_school_budget = school_data_complete.groupby(["school_name"]).mean()["budget"]
per_school_budget = school_data_complete.groupby(["school_name"]).mean()["budget"]
per_school_capita = per_school_budget / per_school_counts

# Calculate the average test scores
per_school_math = school_data_complete.groupby(["school_name"]).mean()["math_score"]
per_school_reading = school_data_complete.groupby(["school_name"]).mean()["reading_score"]

# Calculate the passing scores by creating a filtered data frame
school_passing_math = school_data_complete[(school_data_complete["math_score"] >= 70)]
school_passing_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)]

per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
overall_passing_rate = (per_school_passing_math + per_school_passing_reading) / 2

# Convert to data frame
per_school_summary = pd.DataFrame({"School Type": school_types,
                                   "Total Students": per_school_counts,
                                   "Total School Budget": per_school_budget,
                                   "Per Student Budget": per_school_capita,
                                   "Average Math Score": per_school_math,
                                   "Average Reading Score": per_school_reading,
                                   "% Passing Math": per_school_passing_math,
                                   "% Passing Reading": per_school_passing_reading,
                                   "% Overall Passing Rate": overall_passing_rate})

# Minor data munging
per_school_summary = per_school_summary[["School Type", "Total Students", "Total School Budget", "Per Student Budget",
                                         "Average Math Score", "Average Reading Score", 
                                         "% Passing Math", "% Passing Reading", 
                                         "% Overall Passing Rate"]]
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the data frame
per_school_summary


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[14]:


top_schools = per_school_summary.sort_values(["% Overall Passing Rate"], ascending=False)
top_schools.head(5)


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[15]:


bottom_schools = per_school_summary.sort_values(["% Overall Passing Rate"], ascending=True)
bottom_schools.head(5)


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[16]:



ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]


ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()["reading_score"]
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()["reading_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()["reading_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()["reading_score"]


scores_by_grade = pd.DataFrame({"9th": ninth_graders_scores, "10th": tenth_graders_scores,
                                "11th": eleventh_graders_scores, "12th": twelfth_graders_scores})

scores_by_grade = scores_by_grade[["9th", "10th", "11th", "12th"]]
scores_by_grade.index.name = None


scores_by_grade


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[17]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[18]:


# Establish the bins 
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

# Categorize the spending based on the bins
per_school_summary["Spending Ranges (Per Student)"] = pd.cut(per_school_capita, spending_bins, labels=group_names)

spending_math_scores = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_rate = (spending_passing_math + spending_passing_reading) / 2

# Assemble into data frame
spending_summary = pd.DataFrame({"Average Math Score" : spending_math_scores,
                                 "Average Reading Score": spending_reading_scores,
                                 "% Passing Math": spending_passing_math,
                                 "% Passing Reading": spending_passing_reading,
                                 "% Overall Passing Rate": overall_passing_rate})

# Minor data munging
spending_summary = spending_summary[["Average Math Score", 
                                     "Average Reading Score", 
                                     "% Passing Math", "% Passing Reading",
                                     "% Overall Passing Rate"]]


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[ ]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[19]:


# Establish the bins 
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Categorize the spending based on the bins
per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], size_bins, labels=group_names)

# Calculate the scores based on bins
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
overall_passing_rate = (size_passing_math + size_passing_reading) / 2

# Assemble into data frame
size_summary = pd.DataFrame({"Average Math Score" : size_math_scores,
                             "Average Reading Score": size_reading_scores,
                             "% Passing Math": size_passing_math,
                             "% Passing Reading": size_passing_reading,
                             "% Overall Passing Rate": overall_passing_rate})

# Minor data munging
size_summary = size_summary[["Average Math Score", 
                             "Average Reading Score", 
                             "% Passing Math", "% Passing Reading",
                             "% Overall Passing Rate"]]

# Display results
size_summary


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[20]:


# 

type_math_scores = per_school_summary.groupby(["School Type"]).mean()["Average Math Score"]
type_reading_scores = per_school_summary.groupby(["School Type"]).mean()["Average Reading Score"]
type_passing_math = per_school_summary.groupby(["School Type"]).mean()["% Passing Math"]
type_passing_reading = per_school_summary.groupby(["School Type"]).mean()["% Passing Reading"]
overall_passing_rate = (type_passing_math + type_passing_reading) / 2

# Assemble into data frame
type_summary = pd.DataFrame({"Average Math Score" : type_math_scores,
                             "Average Reading Score": type_reading_scores,
                             "% Passing Math": type_passing_math,
                             "% Passing Reading": type_passing_reading,
                             "% Overall Passing Rate": overall_passing_rate})

# Minor data munging
type_summary = type_summary[["Average Math Score", 
                             "Average Reading Score",
                             "% Passing Math",
                             "% Passing Reading",
                             "% Overall Passing Rate"]]

# Display results
type_summary


# In[ ]:




