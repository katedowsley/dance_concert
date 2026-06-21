import argparse
import pandas as pd
from utils import import_data

"""
Inputs:
- student_class_list: JR export of students in the concert and which classes they are in (.csv)
- routines_in_shows: list of JR classes in the concert (must match class name in JR), name of the item, columns for each show (eg "10am", "1pm", "5:15pm") with 1 in the column if that routine is in that show.
- show_list: list of each show in the concert. Must match the column names in "routines_in_shows"

Desired functionality:
- present a summary of concert 

"""

def main(student_class_list, routines_in_shows, show_list):
    student_class_list_df = import_data(student_class_list)
    routines_in_shows_df = import_data(routines_in_shows)
    show_list_df = import_data(show_list)
    print(student_class_list_df.columns)

    for show in show_list_df["Show"]:
        routines_in_current_show_df = routines_in_shows_df[routines_in_shows_df[show].notna()] 
        students_routine_current_show_df = pd.merge(student_class_list_df, routines_in_current_show_df, how = "inner", left_on = "Class Name", right_on = "Class")
        unique_students_current_show_df = students_routine_current_show_df[["Student First Name", "Student Last Name"]].drop_duplicates()
        print(f"Number of students in {show} concert is {len(unique_students_current_show_df)}")

    # Students with x number of routines
    print(student_class_list_df.groupby(["Student First Name", "Student Last Name"]).count().groupby("Class Name").count()["Status"])
    # print("dofakdsfnasdf")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Summarise concert info")
    parser.add_argument("--student_class_list", type = str, required=True)
    parser.add_argument("--routines_in_shows", type = str, required=True)
    parser.add_argument("--show_list", type = str, required=True)

    args = parser.parse_args()
    main(args.student_class_list, args.routines_in_shows, args.show_list)