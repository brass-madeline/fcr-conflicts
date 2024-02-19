import csv

# Create a dictionary to store the data
data = []
data2 = []    


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

    for game in data:
        for game2 in data:
            if game["id"] != game2["id"]:
                if game["date"] == game2["date"]:
                    if game["start time"] >= game2["start time"] and game["start time"] < game2["end time"]:
                        if game["Home head coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                            game["conflict"] = True
                            game["conflictId"] = game2["id"]
                            game2["conflict"] = True
                            game2["conflictId"] = game["id"]
                        if game["Away head coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                            game["conflict"] = True
                            game["conflictId"] = game2["id"]
                            game2["conflict"] = True
                            game2["conflictId"] = game["id"]
                        if game["Home assistant coach"] != "":
                            if game["Home assistant coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                                game["conflict"] = True
                                game["conflictId"] = game2["id"]
                                game2["conflict"] = True
                                game2["conflictId"] = game["id"]
                        if game["Away assistant coach"] != "":
                            if game["Away assistant coach"] in [game2["Home head coach"], game2["Home assistant coach"],game2["Away head coach"], game2["Away assistant coach"]]:
                                game["conflict"] = True
                                game["conflictId"] = game2["id"]
                                game2["conflict"] = True
                                game2["conflictId"] = game["id"]
                        # else:
                        #     game["conflict"]=False
                        #     game["conflictId"]=False


# Print the data


# Now, 'data' contains a list of dictionaries, with each dictionary representing a row
for row in data:
    if row['id'] == '164435':
        print(row['conflict'])

with open("conflict_data.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
    writer.writeheader()
    for game in data:
        writer.writerow(game)
