# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)

# This is necessary to show lots of columns in pandas 0.12.
# Not necessary in pandas 0.13.
pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 60)

# %%
# Let's continue with our NYC 311 service requests example.
# because of mixed types we specify dtype to prevent any errors
complaints = pd.read_csv("../data/311-service-requests.csv", dtype="unicode")
pl_complaints = pl.read_csv('../data/311-service-requests.csv', infer_schema_length=0)


# %%
# TODO: rewrite the above using the polars library (you might have to import it above) and call the data frame pl_complaints

# %%
# 3.1 Selecting only noise complaints
# I'd like to know which borough has the most noise complaints. First, we'll take a look at the data to see what it looks like:
complaints[:5]

# %%
# TODO: rewrite the above in polars
pl_complaints.head(5)
# %%
# To get the noise complaints, we need to find the rows where the "Complaint Type" column is "Noise - Street/Sidewalk".
noise_complaints = complaints[complaints["Complaint Type"] == "Noise - Street/Sidewalk"]
noise_complaints[:3]
# %%
# TODO: rewrite the above in polars
pl_noise_complaints = pl_complaints.filter(pl.col("Complaint Type")== "Noise - Street/Sidewalk")
pl_noise_complaints.head(3)

# %%
# Combining more than one condition
is_noise = complaints["Complaint Type"] == "Noise - Street/Sidewalk"
in_brooklyn = complaints["Borough"] == "BROOKLYN"
complaints[is_noise & in_brooklyn][:5]

# %%
# TODO: rewrite the above using the Polars library. In polars these conditions are called Expressions.
# Check out the Polars documentation for more info.
pl_complaints.filter(
    (pl.col("Complaint Type") == "Noise - Street/Sidewalk") &
    (pl.col("Borough") == "BROOKLYN")).head(5)

# %%
# If we just wanted a few columns:
complaints[is_noise & in_brooklyn][
    ["Complaint Type", "Borough", "Created Date", "Descriptor"]
][:10]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.filter(
    (pl.col("Complaint Type") == "Noise - Street/Sidewalk") &
    (pl.col("Borough") == "BROOKLYN")).select(["Complaint Type", "Borough", "Created Date", "Descriptor"]).head(10)

# %%
# 3.3 So, which borough has the most noise complaints?
is_noise = complaints["Complaint Type"] == "Noise - Street/Sidewalk"
noise_complaints = complaints[is_noise]
noise_complaints["Borough"].value_counts()

# %%
# TODO: rewrite the above using the polars library
pl_noise_complaints = pl_complaints.filter(pl.col("Complaint Type") == "Noise - Street/Sidewalk")
pl_noise_complaints["Borough"].value_counts()

# %%
# What if we wanted to divide by the total number of complaints?
noise_complaint_counts = noise_complaints["Borough"].value_counts()
complaint_counts = complaints["Borough"].value_counts()

noise_complaint_counts / complaint_counts.astype(float)

# %%
# TODO: rewrite the above using the polars library
pl_noise_complaint_counts = pl_noise_complaints["Borough"].value_counts().rename({'count':'noise'})
pl_complaint_counts = pl_complaints['Borough'].value_counts().rename({'count':'total'})
df = pl_noise_complaint_counts.join(pl_complaint_counts, on = 'Borough')
df = df.with_columns((pl.col('noise') / pl.col('total')).cast(pl.Float32).alias('noise_fraction')).select(['Borough', 'noise_fraction'])

# %%
# Plot the results
(noise_complaint_counts / complaint_counts.astype(float)).plot(kind="bar")
plt.title("Noise Complaints by Borough (Normalized)")
plt.xlabel("Borough")
plt.ylabel("Ratio of Noise Complaints to Total Complaints")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# TODO: rewrite the above using the polars library. NB: polars' plotting method is sometimes unstable. You might need to use seaborn or matplotlib for plotting.
import altair as alt

alt.Chart(df).mark_bar().encode(
    x=alt.X('Borough', title='Boroughs', axis=alt.Axis(labelAngle=45)),
    y=alt.Y('noise_fraction', title = 'Ratio of Noise Complaints to Total Complaints')
).properties(title='Noise Complaints by Borough (Normalized)')
# %%
