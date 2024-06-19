import pandas as pd
import numpy as np

# Read data from all sheets
sheets = ["April 27", "May 4", "May 11" ]
dfs = [pd.read_excel("Spring 2024 FC Richmond U5-U8 Referee Sign.xlsx", sheet_name=sheet, skiprows=2) for sheet in sheets]

# Concatenate all dataframes into a single dataframe
df = pd.concat(dfs, ignore_index=True)

print(len(df.index))
# print(df)

# Filter out canceled games and no-show referees
filtered_df = df[(df['Game Cancellation'].isin([0, np.nan])) & (df['Referee No Show'].isin([0, np.nan]))]
# Remove leading and trailing whitespace from 'REFEREE SIGN UP'
filtered_df['REFEREE SIGN UP'] = filtered_df['REFEREE SIGN UP'].str.strip().str.lower()

print(len(filtered_df.index))


# Print a sample of the DataFrame after applying filtering conditions


# Group by referee sign up and count the number of shifts worked
referee_counts = filtered_df.groupby('REFEREE SIGN UP').size()

# Create a dataframe for the result
result_df = pd.DataFrame({'Name': referee_counts.index, 'Hours Worked': referee_counts.values})

# Export the result to Excel
result_df.to_excel("shifts_worked_filtered.xlsx", index=False)