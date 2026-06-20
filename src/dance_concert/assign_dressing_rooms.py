from abc import ABC, abstractionmethod
import argparse
import pandas as pd
"""
Inputs:
- list of students in the concert - items + shows + teachers. One line per item per show per student
- dressing room information (sizes, limits, teacher supervision)
- preset classes (or specific students) for certain rooms

Outputs:
- List of students for each dressing room.
    - excel format
    - printable format for dressing room tick sheet
- Output compatible with show sculptor
- possible options:
    - after this combine the show sorter list of quick changes with dressing room allocations
        to create runner sheets and show-sculptor tags for qcs

Logic considerations:
- balancing number of costume/hair/tights changes in a room
- kids should be in a room with other kids that they know 

Other:
- one show at a time, for kids in multiple shows assign first show of the day and use that as an input for later shows
"""

# def import_data_frame(pd)

class DataClass(ABC):
    @abstractionmethod
    def import_data(self, file_path: str):
        pass
    # @abstractionmethod
    # def 

class RoomSorter():
    def import_data(self, fname: str):
        if ".csv" in fname:
            self.student_item_df = pd.read_csv(fname)

        elif any(excl_ext in fname for excl_ext in ['.xlsx', '.xls', '.xlsm', '.xlsb']):
            self.student_item_df = pd.read_csv(fname)
        else:
            TypeError(f"Input data must be in the form of a csv or excel file")




    

def main():
    print("yeehaw")
    room_sorter = RoomSorter()
    room_sorter.import_data()

    # import the student item df
    # import the list of dressing rooms

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Module to assign dressing rooms")
    parser.add_argument("--student_item_list")
    main()