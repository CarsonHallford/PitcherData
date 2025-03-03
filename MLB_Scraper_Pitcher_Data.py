# MLB Scraper Pitcher Data
import pandas as pd
import pybaseball as pyb
import numpy as np
from api_scraper import MLB_Scrape

# Set display options to print all columns without truncation
pd.set_option("display.max_columns", None)  # Ensure all columns are displayed
pd.set_option("display.max_rows", None)  # Display all rows, be cautious with large DataFrames
pd.set_option("display.width", None)  # Remove column width limit

y0 = 50  # Release y-position (feet)
yf = 17 / 12  # Home plate y-position (feet)

# Initialize the scraper
scraper = MLB_Scrape()

# Retrieve game data for the specific game ID
game_data = scraper.get_data(game_list_input=[778935])

# Convert the game data to a Polars DataFrame
data_df = scraper.get_data_df(data_list=game_data)

# Convert the Polars DataFrame to a Pandas DataFrame
pandas_df = data_df.to_pandas()


df_pyb = data_df.to_pandas()
df_pyb["PitchesThrown"] = 1
hit_descriptions = {
    "field_out": 0,
    "nan": 0,
    "strikeout": 0,
    "double": 1,
    "strikeout_double_play": 0,
    "single": 1,
    "force_out": 0,
    "hit_by_pitch": 0,
    "grounded_into_double_play": 0,
    "home_run": 1,
    "walk": 0,
    "caught_stealing_2b": 0,
    "sac_bunt": 0,
    "triple": 1,
    "sac_fly": 0,
    "field_error": 0,
    "double_play": 0,
    "catcher_interf": 0,
    "fielders_choice_out": 0,
    "fielders_choice": 0,
    "pickoff_1,b": 0,
    "other_out": 0,
    "caught_stealing_home": 0,
    "pickoff_caught_stealing_2b": 0,
    "caught_stealing_3b": 0,
    "sac_fly_double_play": 0,
    "pickoff_caught_stealing_home": 0,
    "pickoff_2b": 0,
    "run": 0,
    "triple_play": 0,
    "batter_interference": 0,
    "pickoff_3b": 0,
    "sac_bunt_double_play": 0,
    "pickoff_caught_stealing_3b": 0,
}


ab_flag_dict = {
    "field_out": 1,
    "nan": 0,
    "strikeout": 1,
    "double": 1,
    "strikeout_double_play": 1,
    "single": 1,
    "force_out": 1,
    "hit_by_pitch": 0,
    "grounded_into_double_play": 1,
    "home_run": 1,
    "walk": 0,
    "caught_stealing_2b": 0,
    "sac_bunt": 0,
    "triple": 1,
    "sac_fly": 0,
    "field_error": 1,
    "double_play": 1,
    "catcher_interf": 0,
    "fielders_choice_out": 1,
    "fielders_choice": 1,
    "pickoff_1b": 0,
    "other_out": 0,
    "caught_stealing_home": 0,
    "pickoff_caught_stealing_2b": 0,
    "caught_stealing_3b": 0,
    "sac_fly_double_play": 1,
    "pickoff_caught_stealing_home": 0,
    "pickoff_2b": 0,
    "run": 0,
    "triple_play": 1,
    "batter_interference": 1,
    "pickoff_3b": 0,
    "sac_bunt_double_play": 1,
    "pickoff_caught_stealing_3b": 0,
}

swing_code = {
    "ball": 0,
    "foul_tip": 1,
    "called_strike": 0,
    "swinging_strike": 1,
    "pitchout": 0,
    "bunt_foul_tip": 1,
    "foul": 1,
    "hit_into_play_no_out": 1,
    "hit_into_play": 1,
    "hit_into_play_score": 1,
    "missed_bunt": 1,
    "hit_by_pitch": 0,
    "blocked_ball": 0,
    "swinging_strike_blocked": 1,
    "foul_bunt": 1,
}

is_ball = [11, 12, 13, 14]

strike = [1, 2, 3, 4, 5, 6, 7, 8, 9]

df_pyb = df_pyb[(df_pyb["pitcher_name"] == "Luis Curvelo")]
pitcher_pyb = df_pyb[
    [
        "game_id",
        "pitcher_name",
        "ab_number",
        "pitch_description",
        "balls",
        "strikes",
        "play_description",
        "PitchesThrown",
        "pfxz",
        "pfxx",
        "spin_rate",
        "start_speed",
        "ivb",
        "hb",
        "is_whiff",
        "play_description",
        "play_code",
        "zone",
        "is_swing",
        "is_strike",
        "ax",
        "ay",
        "az",
        "vx0",
        "vy0",
        "vz0",
        "extension",
        "launch_speed",
        "batter_name",
    ]
]

pitcher_pyb = pitcher_pyb.sort_values(by=["pitch_description"])
pitcher_pyb["InZone"] = np.where(pitcher_pyb["zone"].isin(strike), 1, 0)
pitcher_pyb["OutZone"] = np.where(pitcher_pyb["zone"].isin(is_ball), 1, 0)

pitcher_pyb["vy_f"] = -np.sqrt(
    pitcher_pyb["vy0"] ** 2 - (2 * pitcher_pyb["ay"] * (y0 - yf))
)

# Compute time (t)
pitcher_pyb["t"] = (pitcher_pyb["vy_f"] - pitcher_pyb["vy0"]) / pitcher_pyb["ay"]

# Compute final z-velocity (vz_f)
pitcher_pyb["vz_f"] = pitcher_pyb["vz0"] + (pitcher_pyb["az"] * pitcher_pyb["t"])

# Compute final x-velocity (vx_f)
pitcher_pyb["vx_f"] = pitcher_pyb["vx0"] + (pitcher_pyb["ax"] * pitcher_pyb["t"])

# Compute VAA
pitcher_pyb["VAA"] = -np.arctan(pitcher_pyb["vz_f"] / pitcher_pyb["vy_f"]) * (
    180 / np.pi
)

# Compute Horizontal Approach Angle (HAA)
pitcher_pyb["HAA"] = -np.arctan(pitcher_pyb["vx_f"] / pitcher_pyb["vy_f"]) * (
    180 / np.pi
)

# Get average vRel per pitch type
pitch_type_vrel = (
    df_pyb.groupby("pitch_description", as_index=False)["z0"].mean()
).round(1)
pitch_type_vrel.rename(columns={"z0": "vRel"}, inplace=True)

# Get average hRel per pitch type
pitch_type_hrel = (
    df_pyb.groupby("pitch_description", as_index=False)["x0"].mean()
).round(1)
pitch_type_hrel.rename(columns={"x0": "hRel"}, inplace=True)
pitcher_hand_unique = df_pyb[["pitch_description", "pitcher_hand"]].drop_duplicates(
    subset=["pitch_description"]
)
pitch_type_hrel = pitch_type_hrel.merge(
    pitcher_hand_unique, on="pitch_description", how="left"
)
pitch_type_hrel["hRel"] = np.where(
    pitch_type_hrel["pitcher_hand"] == "L",
    -pitch_type_hrel["hRel"],
    pitch_type_hrel["hRel"],
)

whiff_pitches = pitcher_pyb[pitcher_pyb["is_whiff"] == True]
pitch_type_whiff = (
    whiff_pitches.groupby("pitch_description").size().reset_index(name="whiff_count")
)
pitch_type_whiff.rename(columns={"whiff_count": "Whiffs"}, inplace=True)
pitch_type_whiff["Whiffs"] = pitch_type_whiff["Whiffs"].astype(int)

strike_pitches = pitcher_pyb[pitcher_pyb["play_code"] == "C"]
pitch_type_cs = (
    strike_pitches.groupby("pitch_description").size().reset_index(name="CS")
)

pitches_in_zone = pitcher_pyb.groupby("pitch_description")["InZone"].sum().reset_index()
pitches_in_zone.rename(columns={"InZone": "Pitches_In_Zone"}, inplace=True)

pitches_out_of_zone = (
    pitcher_pyb.groupby("pitch_description")["OutZone"].sum().reset_index()
)
pitches_out_of_zone.rename(columns={"OutZone": "Pitches_Out_Of_Zone"}, inplace=True)
# print(pitches_out_of_zone)


swings_out_of_zone = pitcher_pyb[
    pitcher_pyb["zone"].isin([11, 12, 13, 14]) & pitcher_pyb["is_swing"] == True
]
swings_out_of_zone = (
    swings_out_of_zone.groupby("pitch_description")["is_swing"]
    .sum()
    .astype(int)  # Convert to integer
    .reset_index()
)
# print(swings_out_of_zone)


pitch_type_spin = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["spin_rate"].mean()
).round(1)
pitch_type_spin.rename(columns={"spin_rate": "Spin Rate"}, inplace=True)

pitch_type_swing = (
    pitcher_pyb.groupby("pitch_description")["is_swing"].sum().astype(int).reset_index()
)
pitch_type_swing.rename(columns={"is_swing": "Swings"}, inplace=True)


pitch_type_ivb = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["ivb"].mean()
).round(1)
pitch_type_ivb.rename(columns={"ivb": "iVB"}, inplace=True)

pitch_type_hb = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["hb"].mean()
).round(1)
pitch_type_hb.rename(columns={"hb": "HB"}, inplace=True)

pitch_avg_velo = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["start_speed"].mean()
).round(1)
pitch_avg_velo.rename(columns={"start_speed": "Avg Velo"}, inplace=True)

pitch_avg_exten = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["extension"].mean()
).round(1)
pitch_avg_exten.rename(columns={"extension": "Extension"}, inplace=True)

# Compute the mean VAA for each pitch type
vaa_means = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["VAA"].mean()
).round(1)

# Compute the mean HAA for each pitch type
haa_means = (
    pitcher_pyb.groupby("pitch_description", as_index=False)["HAA"].mean()
).round(1)

# Compute the highest exit velocity for each pitch type
df_hits = pitcher_pyb.dropna(subset=["launch_speed"])
# Group by pitch type and find the index of the max exit velocity, handling NaN values
idx = df_hits.groupby("pitch_description")["launch_speed"].idxmax().dropna()
# Retrieve the rows with max exit velocity
max_exit_velo = df_hits.loc[
    idx, ["pitch_description", "batter_name", "launch_speed"]
].copy()
max_exit_velo.rename(columns={"launch_speed": "Max Exit Velo"}, inplace=True)

pitch_type_counts = pitcher_pyb.groupby(
    ["pitcher_name", "pitch_description"], as_index=False
)["PitchesThrown"].sum()


pitch_type_counts["Total Pitches"] = pitch_type_counts["PitchesThrown"].sum()

pitch_type_counts["Usage"] = (
    (pitch_type_counts["PitchesThrown"] / pitch_type_counts["Total Pitches"]) * 100
).round(2)

pitch_type_counts = (
    pitch_type_counts.merge(pitch_type_spin, on="pitch_description", how="left")
    .merge(pitch_avg_velo, on="pitch_description", how="left")
    .merge(pitch_type_ivb, on="pitch_description", how="left")
    .merge(pitch_type_hb, on="pitch_description", how="left")
    .merge(pitch_type_whiff, on="pitch_description", how="left")
    .merge(pitch_type_cs, on="pitch_description", how="left")
    .merge(pitches_in_zone, on="pitch_description", how="left")
    .merge(pitches_out_of_zone, on="pitch_description", how="left")
    .merge(swings_out_of_zone, on="pitch_description", how="left")
    .merge(pitch_type_swing, on="pitch_description", how="left")
    .merge(pitch_type_vrel, on="pitch_description", how="left")
    .merge(pitch_type_hrel, on="pitch_description", how="left")
    .merge(vaa_means, on="pitch_description", how="left")
    .merge(haa_means, on="pitch_description", how="left")
    .merge(pitch_avg_exten, on="pitch_description", how="left")
    .merge(max_exit_velo, on="pitch_description", how="left")
)

pitch_type_counts = pitch_type_counts.sort_values(by="PitchesThrown", ascending=False)

pitch_type_counts["Whiffs"] = pitch_type_counts["Whiffs"].fillna(0).astype(int)
pitch_type_counts["CS"] = pitch_type_counts["CS"].fillna(0).astype(int)
pitch_type_counts["CS+Whiffs"] = pitch_type_counts["CS"] + pitch_type_counts["Whiffs"]
pitch_type_counts["Zone%"] = (
    (pitch_type_counts["Pitches_In_Zone"] / pitch_type_counts["PitchesThrown"]) * 100
).round(1)
pitch_type_counts["is_swing"] = pitch_type_counts["is_swing"].fillna(0).astype(int)
pitch_type_counts["Chase%"] = (
    (pitch_type_counts["is_swing"] / pitch_type_counts["Pitches_Out_Of_Zone"]) * 100
).round(1)
pitch_type_counts["Whiff%"] = (
    (pitch_type_counts["Whiffs"] / pitch_type_counts["Swings"]) * 100
).round(1)


pitch_type_counts = pitch_type_counts[
    [
        "pitcher_name",
        "pitch_description",
        "PitchesThrown",
        "Usage",
        "Spin Rate",
        "Avg Velo",
        "iVB",
        "HB",
        "Whiffs",
        "CS",
        "CS+Whiffs",
        "Zone%",
        "Chase%",
        "Whiff%",
        "vRel",
        "hRel",
        "VAA",
        "HAA",
        "Extension",
    ]
]


pitch_type_counts.rename(
    columns={
        "PitchesThrown": "Count",
        "pitch_description": "Pitch Type",
        "batter_name": "Batter",
        "pitcher_name": "Pitcher",
    },
    inplace=True,
)


print(pitch_type_counts)
