import matplotlib.pyplot as plt
import polars as pl

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
plt.rcParams["font.family"] = "sans-serif"

# %% Load the data
pl_bikes = (
    pl.read_csv(
        "../data/bikes.csv", 
        separator=";",
        encoding="latin1"
    )
    .with_columns(
        pl.col("Date").str.strptime(pl.Datetime, fmt="%d/%m/%Y", strict=False)
    )
    .sort("Date")
)

# %% Plot Berri 1 data
# Next up, we're just going to look at the Berri bike path. Berri is a street in Montreal, with a pretty important bike path. I use it mostly on my way to the library now, but I used to take it to work sometimes when I worked in Old Montreal.
# So we're going to create a dataframe with just the Berri bikepath in it
(
    pl_bikes
    .select(["Date", "Berri 1"])
    .sort("Date")
    .to_pandas()
    .set_index("Date")["Berri 1"]
    .plot()
)
plt.show()

# Create a dataframe with just the Berri bikepath using Polars
pl_berri_bikes = pl_bikes.select(["Date", "Berri 1"])
# %% Add weekday column
pl_berri_bikes = pl_berri_bikes.with_columns(
    pl.col("Date").dt.weekday().alias("Weekday")
)

# %%
# Let's add up the cyclists by weekday
# This turns out to be really easy!

weekday_counts_pl = (
    pl_bikes
    .group_by("Date")
    .agg(pl.col("Berri 1").sum().alias("Berri 1"))
    .sort("Weekday")
)
weekday_counts_pl
#Group by weekday and sum using Polars


# %% Rename index
day_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

weekday_counts_named = (
    weekday_counts_pl
    .with_columns(
        pl.col("Weekday").map_dict(day_names).alias("Weekday_name")
    )
    .select(["Weekday_name", "Berri 1"])
)
weekday_counts_named

# %% Plot results
(
    weekday_counts_named
    .to_pandas()
    .set_index("Weekday_name")
    .plot(kind="bar")
)
plt.show()
# %% Final message
print("Analysis complete!")

# %%
