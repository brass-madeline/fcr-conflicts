import csv
from datetime import datetime, timedelta
import string

# Create a dictionary to store the data
data = []
data2 = []    

def is_within_one_hour(time1_str, time2_str):
    # Convert string times to datetime objects
    time1 = datetime.strptime(time1_str, "%H:%M")
    time2 = datetime.strptime(time2_str, "%H:%M")

    # Calculate the time difference
    time_difference = abs(time2 - time1)

    # Check if the time difference is less than or equal to one hour
    one_hour = timedelta(hours=1)
    return time_difference <= one_hour

# Open the CSV file
with open("all-matchups.csv") as csvfile:
    reader = csv.DictReader(csvfile)

    # Iterate over the rows in the CSV file
    for row in reader:
        game = {}
        for key, value in row.items():
            game[key] = value

        # Add the row to the data dictionary
        home_name_list = row["home name"].split("Team")
        game["Home game coaches"] = home_name_list[-1]
        if "Thurs" in game["Home game coaches"]:
            game["Home game coaches"] = game["Home game coaches"].split("Thurs")[0]
        if "Wed" in game["Home game coaches"]:
            game["Home game coaches"] = game["Home game coaches"].split("Wed")[0]        
        if "Mon" in game["Home game coaches"]:
            game["Home game coaches"] = game["Home game coaches"].split("Mon")[0]
        if "Tues" in game["Home game coaches"]:
            game["Home game coaches"] = game["Home game coaches"].split("Tues")[0]
        if "Fri" in game["Home game coaches"]:
            game["Home game coaches"] = game["Home game coaches"].split("Fri")[0]



        # Add the home head coach field
        game["Home head coach"] = game["Home game coaches"].split("/")[0].strip()

        try:
            home_assistant_coach_list = game["Home game coaches"].split("/")[1].split()
            game["Home assistant coach"] = home_assistant_coach_list[0].strip()
        except IndexError:
            game["Home assistant coach"] = ""

        # Add the away game coaches field
        away_name_list = row["away name"].split("Team")
        game["Away game coaches"] = away_name_list[-1]

        if "Thurs" in game["Away game coaches"]:
            game["Away game coaches"] = game["Away game coaches"].split("Thurs")[0]
        if "Wed" in game["Away game coaches"]:
            game["Away game coaches"] = game["Away game coaches"].split("Wed")[0]        
        if "Mon" in game["Away game coaches"]:
            game["Away game coaches"] = game["Away game coaches"].split("Mon")[0]
        if "Tues" in game["Away game coaches"]:
            game["Away game coaches"] = game["Away game coaches"].split("Tues")[0]
        if "Fri" in game["Away game coaches"]:
            game["Away game coaches"] = game["Away game coaches"].split("Fri")[0]

        # Add the away head coach field
        game["Away head coach"] = game["Away game coaches"].split("/")[0].strip()

    

        # Add the away assistant coach field
        try:
            away_assistant_coach_list = game["Away game coaches"].split("/")[1].split()
            game["Away assistant coach"] = away_assistant_coach_list[0].strip()
        except IndexError:
            game["Away assistant coach"] = ""
        
        data.append(game)


    for game in data:
       game["conflict"]=False
       game["conflictId"]=False
       game["locationConflict"]=False

    for game in data:
        for game2 in data:
            if game["id"] != game2["id"]:
                if game["date"] == game2["date"]:
                    if game["start time"] >= game2["start time"] and game["start time"] < game2["end time"]:
                        if  '?' not in game["Home head coach"] and game["Home head coach"] != "" and game["Home head coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                            game["conflict"] = True
                            game["conflictId"] = game2["id"]
                            game2["conflict"] = True
                            game2["conflictId"] = game["id"]
                        if '?' not in game["Away head coach"] and game["Away head coach"] != "" and game["Away head coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                            game["conflict"] = True
                            game["conflictId"] = game2["id"]
                            game2["conflict"] = True
                            game2["conflictId"] = game["id"]
                        if '?' not in game["Home assistant coach"] and game["Home assistant coach"] != "":
                            if game["Home assistant coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                                game["conflict"] = True
                                game["conflictId"] = game2["id"]
                                game2["conflict"] = True
                                game2["conflictId"] = game["id"]
                        if '?' not in game["Away assistant coach"] and game["Away assistant coach"] != "":
                            if game["Away assistant coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                                game["conflict"] = True
                                game["conflictId"] = game2["id"]
                                game2["conflict"] = True
                                game2["conflictId"] = game["id"]
                        # else:
                        #     game["conflict"]=False
                        #     game["conflictId"]=False
                    # Find games that have a start time within one hour after end 
                    if is_within_one_hour(game["end time"], game2["start time"]):
                        print(game["Home head coach"])
                        if '?' not in game["Home head coach"] and game["Home head coach"] != "" and game["Home head coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]] and game["field name"].strip().split()[0] != game2["field name"].strip().split()[0]:
                            game["locationConflict"] = game2["id"]
                        if '?' not in game["Away head coach"] and game["Away head coach"] != "" and game["Away head coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]] and game["field name"].strip().split()[0] != game2["field name"].strip().split()[0]:
                            game["locationConflict"] = game2["id"]
                        if '?' not in game["Home assistant coach"] and game["Home assistant coach"] != "" and game["Home assistant coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]] and game["field name"].strip().split()[0] != game2["field name"].strip().split()[0]:
                            game["locationConflict"] = game2["id"]                                                        
                        if '?' not in game["Away assistant coach"] and game["Away assistant coach"] != "" and game["Away assistant coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]] and game["field name"].strip().split()[0] != game2["field name"].strip().split()[0]:
                            game["locationConflict"] = game2["id"]





# Print the data


# Now, 'data' contains a list of dictionaries, with each dictionary representing a row
# for row in data:
#     if row['id'] == '164435':
#         print(row['conflict'])

with open("conflict_data.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
    writer.writeheader()
    for game in data:
        writer.writerow(game)

