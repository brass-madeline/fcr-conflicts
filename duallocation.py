import pandas as pd

# Read data from CSV file
df = pd.read_csv('all-matchups.csv')

def extract_coaches(team_name):
    # Extracting the part of the team name that contains coach information
    coaches_part = team_name.split("Team ")[1]
    
    # Removing any additional information after the team name
    coaches_part = coaches_part.split(",")[0]
    
    # Check if there is a slash ("/") in the remaining string
    if "/" in coaches_part:
        # Splitting the remaining string using "/"
        coaches_list = coaches_part.split("/")
        
        # Take the first word as the second coach's name
        if len(coaches_list) > 1:
            coaches_list[1] = coaches_list[1].split()[0]
    else:
        # If no slash is present, only the first word is the coach's name
        coaches_list = [coaches_part.split()[0]]
    
    return coaches_list

# Extracting coach names from home and away teams
df['home_coaches'] = df['home name'].apply(extract_coaches)
df['away_coaches'] = df['away name'].apply(extract_coaches)

# Function to extract location from field name
def extract_location(field_name):
    return field_name.split()[0]

# Extracting location from field name
df['location'] = df['field name'].apply(extract_location)

# Dictionary to store dates for each coach at both locations
coaches_dates = {}

# Iterate through the rows to find coaches at both locations on the same date
for _, row in df.iterrows():
    date = row['date']
    home_coaches = row['home_coaches']
    away_coaches = row['away_coaches']
    location = row['location']

    # Check if any coach (home or away) is coaching at both locations
    for home_coach in home_coaches:
        if home_coach.strip() not in coaches_dates:
            coaches_dates[home_coach.strip()] = {'Robious': set(), 'Horner': set()}

        # Add the date to the corresponding location set
        coaches_dates[home_coach.strip()][location].add(date)

    for away_coach in away_coaches:
        if away_coach.strip() not in coaches_dates:
            coaches_dates[away_coach.strip()] = {'Robious': set(), 'Horner': set()}

        # Add the date to the corresponding location set
        coaches_dates[away_coach.strip()][location].add(date)

# Create a DataFrame from the result
result_data = {'coach name': [], 'dates on both fields': []}

for coach, locations_dates in coaches_dates.items():
    robious_dates = locations_dates.get('Robious', set())
    horner_dates = locations_dates.get('Horner', set())

    # Check if the coach has dates at both locations
    if robious_dates and horner_dates:
        result_data['coach name'].append(coach)
        # Join the dates with commas
        result_data['dates on both fields'].append(','.join(sorted(robious_dates.intersection(horner_dates))))

result_df = pd.DataFrame(result_data)

# Export the result to a CSV file
result_df.to_csv('coaches_dates_at_both_locations.csv', index=False)