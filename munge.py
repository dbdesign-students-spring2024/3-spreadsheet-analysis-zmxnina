# place your code to clean up the data file below.
import os
import csv

def total_count(record, start_hour, end_hour):
    total = 0
    for i in range(start_hour, end_hour, 2):
        time_field = f"TIME_{i:02d}01_{(i+2)%24:02d}00_CNT"
        total += int(record[time_field])
    return total

def main():
    input_filepath = os.path.join("data", "LEOKA_ASSAULT_TIME_WEAPON_INJURY_1995_2022.csv")
    output_filepath = os.path.join("data", "clean_data.csv")

    input_file = open(input_filepath, "r", encoding="utf_8")
    output_file = open(output_filepath, "w", encoding="utf_8")

    fieldnames = ["DATA_YEAR","STATE_ABBR","POPULATION_GROUP_DESC","TIME_0001_0600_CNT","TIME_0601_1200_CNT","TIME_1201_1800_CNT","TIME_1801_0000_CNT","FIREARM_INJURY_CNT","FIREARM_NO_INJURY_CNT","KNIFE_INJURY_CNT","KNIFE_NO_INJURY_CNT","HANDS_FISTS_FEET_INJURY_CNT","HANDS_FISTS_FEET_NO_INJURY_CNT","OTHER_INJURY_CNT","OTHER_NO_INJURY_CNT","LEOKA_FELONY_KILLED","LEOKA_ACCIDENT_KILLED","TOTAL_ASSAULTED"]

    new_fields = ["TIME_0001_0600_CNT","TIME_0601_1200_CNT","TIME_1201_1800_CNT","TIME_1801_0000_CNT","TOTAL_ASSAULTED"]

    csv_reader = csv.DictReader(input_file)
    csv_writer = csv.DictWriter(output_file, fieldnames = fieldnames)
    csv_writer.writeheader()

    for record in csv_reader:
        if int(record["DATA_YEAR"]) >= 2018:
            total_by_time = sum(total_count(record, start, start + 6) for start in range(0, 24, 6))
            total_by_type = sum(int(record[field]) for field in fieldnames[7:-3])
                                
            if total_by_time != total_by_type or total_by_time == 0:
                continue

            munged_record = {}

            for field in fieldnames:
                if field not in new_fields:
                    munged_record[field] = record[field]
            
            munged_record["TIME_0001_0600_CNT"] = total_count(record, 0, 6)
            munged_record["TIME_0601_1200_CNT"] = total_count(record, 6, 12)
            munged_record["TIME_1201_1800_CNT"] = total_count(record, 12, 18)
            munged_record["TIME_1801_0000_CNT"] = total_count(record, 18, 24)
            munged_record["TOTAL_ASSAULTED"] = total_by_time
            
            csv_writer.writerow(munged_record)

    input_file.close()
    output_file.close()

if __name__ == "__main__":
    main()