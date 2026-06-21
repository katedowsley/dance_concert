from abc import ABC, abstractmethod
import argparse
import pandas as pd
import networkx as nx
from pyvis.network import Network
from collections import Counter
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt


from utils import import_data

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
- boys should have their own dressng room

Other:
- one show at a time, for kids in multiple shows assign first show of the day and use that as an input for later shows


Possible methods:
- rules-based 
- social network analysis with graphs
    - community pooling
    - node2vec
- k-means clustering (constrained). or any other constrained clustering techniques
    - each student is a dot, and each class is a dimension with a a 1 or 0, depending on whether a student is in that class. then PCA
    - OR convert the graph to a vectorised space and and combine
    - constrained by sizes of dressing rooms
    - constrained by sizes
- other clustering methods:
    - hierarchical
    - https://deepfa.ir/en/blog/introduction-to-clustering-algorithms-concepts-applications-key-algorithms
- Mixed-Integer Linear Programming (MILP)
    - optimisation with several constraints

"""

#TODO - use concert item to link students, not just class

# def import_data_frame(pd)

# Abstraction for clustering (inerface)
class Clusterer(ABC): #Note: dependency inversion to implement different clustering algorithms
    @abstractmethod
    def cluster(self, df):
        pass
    # @abstractnmethod
    # def 


# Low level module: concrete implementation
class KMeansClustering(Clusterer):
    def cluster(self, df):
        unique_students = df[["Student First Name", "Student Last Name"]].drop_duplicates()
        unique_classes = df["Class Name"].unique()
        data_points = []
        for idx, student in unique_students.iterrows():
            student_class_bool = []
            for class_name in unique_classes:
                student_in_class = df[(df["Class Name"] == class_name) & (df["Student First Name"] == student["Student First Name"]) & (df["Student Last Name"] == student["Student Last Name"])]
                if len(student_in_class)>0:
                    student_class_bool.append(1)
                else:
                    student_class_bool.append(0)
            data_points.append(student_class_bool)
        print(data_points)
        # pass

        


# High level module: depends on abstraction
class DressingRoomClustering:
    def __init__(self, clusterer: Clusterer):
        self.clusterer = clusterer

    



class RoomSorter:
    def __init__(self, fname: str):
        self.student_class_df = import_data(fname) #TODO change this so that it could be initialised with an existing df --> good for testing

    def create_graph(self):
        self.student_graph = nx.Graph()

        unique_students = self.student_class_df[["Student First Name", "Student Last Name"]].drop_duplicates()
        nodes = []
        for index, student in unique_students.iterrows():
            temp_student_df = self.student_class_df[(self.student_class_df["Student First Name"] == student["Student First Name"]) & (self.student_class_df["Student Last Name"] == student["Student Last Name"])]
            student_id = student["Student First Name"]+student["Student Last Name"]
            student_info = temp_student_df.iloc[0][["Contact First Name", "Contact Last Name", "Birthdate", "Gender"]].to_dict()
            student_info["Classes"] = list(temp_student_df["Class Name"])

            nodes.append((student_id, student_info))
        unique_classes = self.student_class_df["Class Name"].unique()
        edges = []
        for class_name in unique_classes:
            temp_class_df = self.student_class_df[(self.student_class_df["Class Name"] == class_name)]
            for index, student_row in temp_class_df.iterrows():
                curr_student = student_row["Student First Name"] + student_row["Student Last Name"]
                students_to_join_df = temp_class_df[temp_class_df.index>index]
                for index_next, next_student_row in students_to_join_df.iterrows():
                    next_student = next_student_row["Student First Name"] + next_student_row["Student Last Name"]
                    edges.append((curr_student, next_student))
            a = 1
    
        self.student_graph.add_nodes_from(nodes)

        # Account for repeated edges with weights
        edge_counts = Counter(edges)

        # Add edges with the calculated frequency as the weight
        for (u, v), count in edge_counts.items():
            self.student_graph.add_edge(u, v, weight=count)

        # self.student_graph.add_edges_from(edges)
   
    def visualise_graph(self):
        net = Network()
        net.from_nx(self.student_graph)
        for node in net.nodes:
            node["title"] = node["id"] + "<br>" +"<br>".join(node["Classes"]) 
        net.show("testgraph.html", notebook = False)
        a=1
        pass
    
    


    

def main(student_class_list):
    print("yeehaw")
    plt.plot()
    room_sorter = RoomSorter(student_class_list)
    room_sorter.create_graph()
    room_sorter.visualise_graph()
    a = 1
    # import the student item df
    # import the list of dressing rooms

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Module to assign dressing rooms")
    parser.add_argument("--student_class_list", required = True, type = str)
    args = parser.parse_args()
    main(args.student_class_list)