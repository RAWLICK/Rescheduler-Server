import pandas as pd
# Below thing is suppresing warnings made by pandas for the DataFrame we are working for
pd.options.mode.chained_assignment = None
from datetime import datetime
import math
from functools import reduce
from datetime import timedelta
from flask import jsonify
import json

def CompressionFunction(
        ImportedDataFrame, 
        currentTime, 
        PriorSelections, 
        FixedSelections,
        RemovingSelections):

    # ImportedDataFrame = json.dumps([
    #     {
    #         # 0
    #         "StartTime": "06:00",
    #         "EndTime": "07:00",
    #         "Work": "Physics",
    #         "StartAngle": 180,
    #         "EndAngle": 210,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "Green"
    #     },
    #     {
    #         # 1
    #         "StartTime": "07:00",
    #         "EndTime": "08:00",
    #         "Work": "Chemistry",
    #         "StartAngle": 210,
    #         "EndAngle": 240,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 2
    #         "StartTime": "08:00",
    #         "EndTime": "09:00",
    #         "Work": "Maths",
    #         "StartAngle": 240,
    #         "EndAngle": 270,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 3
    #         "StartTime": "09:00",
    #         "EndTime": "10:00",
    #         "Work": "Biology",
    #         "StartAngle": 270,
    #         "EndAngle": 300,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 4
    #         "StartTime": "10:00",
    #         "EndTime": "11:00",
    #         "Work": "SST",
    #         "StartAngle": 300,
    #         "EndAngle": 330,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 5
    #         "StartTime": "11:00",
    #         "EndTime": "12:30",
    #         "Work": "Economics",
    #         "StartAngle": 330,
    #         "EndAngle": 375,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 6
    #         "StartTime": "12:30",
    #         "EndTime": "13:30",
    #         "Work": "Sanskrit",
    #         "StartAngle": 375,
    #         "EndAngle": 405,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 7
    #         "StartTime": "13:30",
    #         "EndTime": "14:30",
    #         "Work": "Business",
    #         "StartAngle": 405,
    #         "EndAngle": 435,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 8
    #         "StartTime": "14:30",
    #         "EndTime": "15:30",
    #         "Work": "Art",
    #         "StartAngle": 435,
    #         "EndAngle": 465,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 9
    #         "StartTime": "15:30",
    #         "EndTime": "16:30",
    #         "Work": "Sports",
    #         "StartAngle": 465,
    #         "EndAngle": 495,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 10
    #         "StartTime": "16:30",
    #         "EndTime": "17:30",
    #         "Work": "Cooking",
    #         "StartAngle": 495,
    #         "EndAngle": 525,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    #     {
    #         # 11
    #         "StartTime": "17:30",
    #         "EndTime": "18:30",
    #         "Work": "Hindi",
    #         "StartAngle": 525,
    #         "EndAngle": 555,
    #         "TaskDate": "05/01/2025",
    #         "Slice_Color": "blue"
    #     },
    # ])

    # Converting ImportedDataframe into a dataframe which this Compress Function can consume accordingly
    # Remember to use single quote (') and double quotes(") seperately in fString instead of same to avoid any error.
    # json.loads() helps us changing the stringified ImportedDataFrame back into a list of dictionaries

    dataframe = pd.DataFrame([])
    for i in json.loads(ImportedDataFrame):
        TaskDate = i["TaskDate"]
        newObject = {
            "StartTime": f"{i['TaskDate']} {i['StartTime']}",
            "EndTime": f"{i['TaskDate']} {i['EndTime']}",
            "Work": i["Work"]
        }
        dataframe = pd.concat([dataframe, pd.DataFrame([newObject])], ignore_index=True)

    # Picking out the Work, StartTiming and End Timing from the dataframe and converting StartTiming and End Timing in datetime format so that it can be compared within

    Work = list(dataframe['Work'])
    Start = list(datetime.strptime(x, "%d/%m/%Y %H:%M") for x in dataframe['StartTime'])
    End = list(datetime.strptime(x, "%d/%m/%Y %H:%M") for x in dataframe['EndTime'])

    # These below are the works which has to be removed from the schedule 
    # We have used for loop with reverse=True because we don't want to mess with the index value when one of the value gets removed which doesn't happen when removed from the last

    if (RemovingSelections != ""):
        Input_Removing_Work = RemovingSelections
        Removing_Work = Input_Removing_Work.split(",")[:]
        Removing_Work_List = list(Work[int(x)] for x in (Removing_Work))
        print("\n")
        print("So the works which you are Removing are: ", Removing_Work_List)
        print("\n")

        for i in sorted(Removing_Work, reverse=True):
            del Work[int(i)]
            del Start[int(i)]
            del End[int(i)]
        
        Original_End = list(datetime.strptime(x, "%d/%m/%Y %H:%M") for x in dataframe['EndTime'])

    # Entering the current time and converting it in datetime format
    inp_time = currentTime
    cur_time = datetime.strptime(inp_time, "%d/%m/%Y %H:%M")
    print('\n')
    print('Current Time: ', cur_time)
    print('\n')

    # Now asking the user which are those works which he wants and is currently present before the current time.
    # User's input was stored in "PriorSelections" which was passed as a parameter
    # This data is asked through index number and holded in "Input_Prev_Work", then "Input_Prev_Work" is filtered from string of commas and holded as "Prev_Work".
                        
    if (PriorSelections != ""):              
        Input_Prev_Work = PriorSelections
        Prev_Work = Input_Prev_Work.split(",")[:]

        # Then "Prev_Work" is converted into a list of those actual Previous Works known as "Prev_Work_List" to be accessible forth
        # Complete_Fragements is actually sum of all fragments which are divided on the basis of Pinned Works
        # Now Prev_Work_List is added in Complete_Fragments because Complete_Fragements in itself means containing all items
        print("\n")
        print("So you want", list(Work[int(x)] for x in (Prev_Work)))
        print("\n")
        Prev_Work_List = list(Work[int(x)] for x in (Prev_Work))
        Complete_Fragments = Prev_Work_List[:]

    # Now asking user which are those works timings which he didn't want change on course of compression of timings
    # User's input was stored in "FixedSelections" which was passed as a parameter
    # Then splitting the "Input_Pin_Work" with comma to filter it making it "Pinned Work"
    # Then making a list of those split pieces named "Pinned_Work_List"

    if (FixedSelections != ""):
        Input_Pin_Work = FixedSelections
        Pinned_Work = Input_Pin_Work.split(",")[:]
        Pinned_Work_List = list(Work[int(x)] for x in (Pinned_Work))

        # Then making a list of Starting Time of those Fixed Works naming "Pinned_Work_StartTiming"
        # Then making a list of Ending Time of those Fixed Works naming "Pinned_Work_EndTiming"

        Pinned_Work_StartTiming = list(Start[int(x)] for x in (Pinned_Work))
        # print("Pinned Work StartTiming", Pinned_Work_StartTiming)
        Pinned_Work_EndTiming = list(End[int(x)] for x in (Pinned_Work))
        print("So your Pinned Works are", Pinned_Work_List)
        print("\n")

    # Ensures that the Time_Duration on which the cur_time falls get automatically chosen and get compressed in the upcoming to-be made schedule.
    # This below boolean list is a list of lot of "FALSE" but one "TRUE" which is used to know about that Time_Duration which is falling at present

    boolean_list = []
    for i in range (0, len(Start)):
        if (cur_time >= Start[i] and cur_time < End[i]):
            boolean_list.append("True")
        else: 
            boolean_list.append("False")
    if("True" not in boolean_list):
        boolean_list = []
        for i in range (0, len(Start)):
            if (Start[i] > cur_time and "True" not in boolean_list):
                boolean_list.append("True")
            else:
                boolean_list.append("False")

    # Now making a Fragment_Dictionary in which the fragments will be divided on the basis of works present between every fixed time.
    # First fragment will be manually named containing Previous Work List and List of work from current Time Duration Work to First Fixed Work

    Fragment_Dictionary = {}

    # Work[boolean_list.index("True"): ] means selecting till last

    if (PriorSelections == "" and FixedSelections == ""):
        Fragment_Dictionary.update({"Fragment_" + str(1) : list(Work[boolean_list.index("True"): ])})
        print(Fragment_Dictionary)
        print("\n")
        # Output: {'Fragment_1': ['Work 3', 'Work 3 Break', 'Work 4', 'Work 4 Break', 'Sona', 'Work 5', 'Work 5 Break', 'Work 6', 'Free 1', 'Free 2']}  

    elif (PriorSelections != "" and FixedSelections == ""):
        Fragment_Dictionary.update({"Fragment_" + str(1) : Prev_Work_List + list(Work[boolean_list.index("True"): ])})
        print(Fragment_Dictionary)
        print("\n")
        # Output: {'Fragment_1': ['Work 1', 'Work 2', 'Work 2 Break', 'Work 3', 'Work 3 Break', 'Work 4', 'Work 4 Break', 'Sona', 'Work 5', 'Work 5 Break', 'Work 6', 'Free 1', 'Free 2']}  

    elif (PriorSelections == "" and FixedSelections != ""):
        Fragment_Dictionary.update({"Fragment_" + str(1) : list(Work[boolean_list.index("True"): int(Pinned_Work[0])])})

        # Now rest of the fragments will be managed with for loop
        # Pinned_Work is actually a list of numbers not string of works.
        # int(Pinned_Work[i])+1 is used to increase the number obtained from Pinned_Work by 1, while
        # int(Pinned_Work[i+1]) is used to move to the next index of Pinned_Work

        for i in range(0, len(Pinned_Work_List)-1):
            Fragment_Dictionary.update({"Fragment_" + str(i+2) : list(Work[int(Pinned_Work[i])+1 : int(Pinned_Work[i+1])])})

        Fragment_Dictionary.update({"Last_Fragment" : list(Work[int(Pinned_Work[-1])+1 : ])})
        print(Fragment_Dictionary)
        print("\n")
        # Output: {'Fragment_1': ['Work 3', 'Work 3 Break', 'Work 4', 'Work 4 Break'], 'Fragment_2': ['Sona', 'Work 5', 'Work 5 Break'], 'Fragment_3': ['Work 6', 'Free 1'], 'Fragment_4': ['Free 2']}

    elif (PriorSelections != "" and FixedSelections != ""):
        Fragment_Dictionary.update({"Fragment_" + str(1) : Prev_Work_List + list(Work[boolean_list.index("True"): int(Pinned_Work[0])])})

        for i in range(0, len(Pinned_Work_List)-1):
            Fragment_Dictionary.update({"Fragment_" + str(i+2) : list(Work[int(Pinned_Work[i])+1 : int(Pinned_Work[i+1])])})

        Fragment_Dictionary.update({"Last_Fragment" : list(Work[int(Pinned_Work[-1])+1 : ])})
        print(Fragment_Dictionary)
        print("\n")
        # Output: {'Fragment_1': ['Work 1', 'Work 2', 'Work 2 Break', 'Work 3', 'Work 3 Break', 'Work 4', 'Work 4 Break'], 'Fragment_2': ['Sona', 'Work 5', 'Work 5 Break'], 'Fragment_3': ['Work 6', 'Free 1'], 'Fragment_4': ['Free 2']}

    # Nested Fragments List as by name is a list with some sublists rather than a Dictionary from above "Fragment_Dictionary". It in contrast just doesn't mention the Fragment Number.  

    Nested_Fragments_List = []
    for i in Fragment_Dictionary:
        Nested_Fragments_List.append(Fragment_Dictionary[i])
    print("Nested_Fragments_List: ", Nested_Fragments_List)
    print("\n")
    # Output: [['Work 1', 'Work 2', 'Work 2 Break', 'Work 3', 'Work 3 Break', 'Work 4', 'Work 4 Break'], ['Sona', 'Work 5', 'Work 5 Break'], ['Work 6', 'Free 1'], ['Free 2']] or may vary according to the parameters passed.

    # Complete_Fragments is the next step where the sublists of Nested Fragment List gets combined and make one list.

    Complete_Fragments = [item for sublist in Nested_Fragments_List for item in sublist]
    print("Complete Fragments: ", Complete_Fragments)
    print("\n")

    if (FixedSelections == ""):
        Total_Fragment_Duration = timedelta(0)
        Total_Fragment_Duration = Original_End[-1] - cur_time
        print("Total_Fragment_Duration(Total Time Left): ", Total_Fragment_Duration)
        print("\n")
        # Output: 0 days 11:30:00

        # Finding the ratios
        # Time_Interval is the duration difference between each work in terms of minutes.
        # Time_Interval_List is the list of "Time_Interval" from above.
        # Time_Interval_List_Ratio is finding the ratio of each "Time_Interval" comparing from the whole "Time_Interval_List" with help of HCF (Highest Common Factor) so to find the real value of each work.

        Time_Interval_List = []
        Time_Interval_List_Ratio = []

        for i in range(0, len(Start)):
            Time_Interval = End[i] - Start[i]
            Time_Interval_List.append(int(Time_Interval.total_seconds() / 60))
        print("Time Interval List: ", Time_Interval_List)
        # Output: [60, 60, 60,..]
        print("\n")

        # Here reduce plays role of iteration(ek ek karke dena because there is a whole list present)
        Hcf = reduce(math.gcd, Time_Interval_List)
        for i in Time_Interval_List:
            Ratio = i/Hcf
            Time_Interval_List_Ratio.append(int(Ratio))
        print("Time Interval List Ratio: ", Time_Interval_List_Ratio)
        # Output: [4, 4, 4,..]
        print("\n")

        # Complete_Fragments_Index vo saare kaam ka index hai jo ki left out hai karne ko (Hindi_Lang)
        Complete_Fragments_Index = []
        List_Work = list(Work)
        for i in Complete_Fragments:
            Complete_Fragments_Index.append(List_Work.index(i))
        print("Complete Fragments Index: ",Complete_Fragments_Index)
        # Output: [2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 18]
        print("\n")

        # Required_Ratio_List tells vo left out kaam jinka ratio jaanna hai, naki sabka (Hindi_Lang)
        Required_Ratio_List = []
        for i in Complete_Fragments_Index:
            Required_Ratio_List.append(Time_Interval_List_Ratio[i])
        print("Required Ratio List: ", Required_Ratio_List)
        # Output: [4,4,1..]
        print("\n")

        # Finding the sum of ratios
        Sum_Of_Ratios = 0
        for i in Required_Ratio_List:
            Sum_Of_Ratios += i
        print("Sum Of Ratios: ", Sum_Of_Ratios)
        print("\n")
        # Output: 54

        # Duration_According_Ratio tells what time should be given to each work in minutes according to ratio so that it get completed on time
        Duration_According_Ratio = []
        for i in Required_Ratio_List:
            Duration_According_Ratio.append(round(i/Sum_Of_Ratios * (Total_Fragment_Duration.total_seconds() / 60)))
        print("Duration According Ratio: ",Duration_According_Ratio)
        print("\n")
        # Output: [51, 51, 26...]

        # Sum_Dur_Acc_Rat is the sum of Duration_According_Ratio
        Sum_Dur_Acc_Rat = 0
        for i in Duration_According_Ratio:
            Sum_Dur_Acc_Rat += i
        print("Sum_Dur_Acc_Rat: ", Sum_Dur_Acc_Rat, "minutes")
        print("\n")
        # Output: 691

        # This part of code will ensure that the Sum of Ratios would not cross the line or say the "Proposed Left Time" or "Total Fragment Duration"
        if (Sum_Dur_Acc_Rat > (Total_Fragment_Duration.total_seconds() / 60)):
            Difference = int(Sum_Dur_Acc_Rat - (Total_Fragment_Duration.total_seconds() / 60))
            Duration_According_Ratio[-1] -= Difference

        # Creating a new DataFrame for Ratio Compressed Output
        TimeDelta_Minutes = []
        for i in range(0, len(Duration_According_Ratio)):
            TimeDelta_Minutes.append(timedelta(minutes=int(Duration_According_Ratio[i])))
        # print("TimeDelta_Minutes: ",TimeDelta_Minutes)
        # Output: [datetime.timedelta(seconds=3060), datetime.timedelta(seconds=3060),...]

        # Adding The Starting Time
        Compressed_Data = [[cur_time, cur_time + TimeDelta_Minutes[0], Complete_Fragments[0]]]

        # Making the DataFrame
        Compressed_DataFrame = pd.DataFrame(Compressed_Data, columns=['Start_', 'End_', 'Work_'])

        for i in range(1, len(Complete_Fragments)):
            newData = [[Compressed_DataFrame.End_[i-1], Compressed_DataFrame.End_[i-1] + TimeDelta_Minutes[i], Complete_Fragments[i]]]
            # upper_part = Compressed_DataFrame.loc[:i - 1]
            # lower_part = Compressed_DataFrame.loc[i:]
            Compressed_DataFrame = pd.concat([Compressed_DataFrame, pd.DataFrame(newData, columns=['Start_', 'End_', 'Work_'], index=[i])], ignore_index=True)

        #Sorting the rows on the basis of 'Start_' column with respect to time and resetting the index of dataframe.
        Compressed_DataFrame = Compressed_DataFrame.sort_values(by='Start_').reset_index(drop=True)

    # Here else is for, if the paramters have values for fixedTimings
    else: 
        # LenTills_Addition tells us, how many of the works we have actually covered with respect to fixed timing while going on with the "for loop"
        # LenTills_Dictionary is a dictionary that counts the len value of works (number of works) till each fixed timing
        # LenTills_List is same as above but in list format

        LenTills_Addition = 0
        LenTills_Dictionary = {}
        LenTills_List = []
        for i in range(0, len(Nested_Fragments_List)):
            LenTills_Addition += len(Nested_Fragments_List[i])
            LenTills_Dictionary.update({"LenTillPin" + str(i+1) : LenTills_Addition})
            LenTills_List.append(LenTills_Addition)
        print("LenTills_Dictionary: ", LenTills_Dictionary)
        print("\n")
        # Output: {'LenTillPin1': 7, 'LenTillPin2': 10, 'LenTillPin3': 12, 'LenTillPin4': 13}
        print("LenTills_List: ", LenTills_List)
        # Output: [7, 10, 12, 13]
        print("\n")

        # "LenBtwPins_Dictionary" tells us about len value like "LenTills_Dictionary" but in contrast it mention the len value of works present between each fixed timings rather than from the start.

        LenBtwPins_Dictionary = {}
        for i in range(0, len(Nested_Fragments_List)):
            LenBtwPins_Dictionary.update({"LenBtwPin" + str(i+1) : len(Nested_Fragments_List[i])})
        print("LenBtwPins_Dictionary: ", LenBtwPins_Dictionary)
        print("\n")
        # Output: {'LenBtwPin1': 7, 'LenBtwPin2': 3, 'LenBtwPin3': 2, 'LenBtwPin4': 1}

        # "Fragment_Dur_Dict" is Duration between each fragment (fragment on basis of pinned timing) in form of a Dictionary
        # First update of this dictionary is done manually and then it went on with loop.

        Fragment_Dur_Dict = {}
        Fragment_Dur_Dict.update({"Fragment_" + str(1) + "_Duration" : Pinned_Work_StartTiming[0] - cur_time})

        for i in range(0, len(Pinned_Work_List)-1):
            Fragment_Dur_Dict.update({"Fragment_" + str(i+2) + "_Duration" : Pinned_Work_StartTiming[i+1] - Pinned_Work_EndTiming[i]})

        # This Last Update actually ensures that Total_Fragment_Duration covers till the end of the original schedule including the timings of Removed Works
        if (RemovingSelections != ""):
            Fragment_Dur_Dict.update({"Fragment_Last_Duration" : Original_End[-1] - Pinned_Work_EndTiming[-1]})
        elif (RemovingSelections == ""):
            Fragment_Dur_Dict.update({"Fragment_Last_Duration" : End[-1] - Pinned_Work_EndTiming[-1]})

        print("Fragment_Dur_Dict: ", Fragment_Dur_Dict)
        print("\n")
        # Output: {'Fragment_1_Duration': Timedelta('0 days 03:00:00'), 'Fragment_2_Duration': Timedelta('0 days 03:00:00'), 'Fragment_3_Duration': Timedelta('0 days 04:00:00'), 'Fragment_4_Duration': Timedelta('0 days 01:30:00')}

        # "Total_Fragment_Duration" is the sum of duration of all the fragments present.

        Total_Fragment_Duration = timedelta(0)
        for i in Fragment_Dur_Dict:
            Total_Fragment_Duration += Fragment_Dur_Dict[i]
        print("Total_Fragment_Duration(Total Time Left): ", Total_Fragment_Duration)
        print("\n")
        # Output: 0 days 11:30:00

        # Finding the ratios
        # Time_Interval is the duration difference between each work in terms of minutes.
        # Time_Interval_List is the list of "Time_Interval" from above.
        # Time_Interval_List_Ratio is finding the ratio of each "Time_Interval" comparing from the whole "Time_Interval_List" with help of HCF (Highest Common Factor) so to find the real value of each work.

        Time_Interval_List = []
        Time_Interval_List_Ratio = []

        for i in range(0, len(Start)):
            Time_Interval = End[i] - Start[i]
            Time_Interval_List.append(int(Time_Interval.total_seconds() / 60))
        print("Time Interval List: ", Time_Interval_List)
        # Output: [60, 60, 60,..]
        print("\n")

        # Here reduce plays role of iteration(ek ek karke dena because there is a whole list present)
        Hcf = reduce(math.gcd, Time_Interval_List)
        for i in Time_Interval_List:
            Ratio = i/Hcf
            Time_Interval_List_Ratio.append(int(Ratio))
        print("Time Interval List Ratio: ", Time_Interval_List_Ratio)
        # Output: [4, 4, 4,..]
        print("\n")

        # Complete_Fragments_Index vo saare kaam ka index hai jo ki left out hai karne ko (Hindi_Lang)
        Complete_Fragments_Index = []
        List_Work = list(Work)
        for i in Complete_Fragments:
            Complete_Fragments_Index.append(List_Work.index(i))
        print("Complete Fragments Index: ",Complete_Fragments_Index)
        # Output: [2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 18]
        print("\n")

        # Required_Ratio_List tells vo left out kaam jinka ratio jaanna hai, naki sabka (Hindi_Lang)
        Required_Ratio_List = []
        for i in Complete_Fragments_Index:
            Required_Ratio_List.append(Time_Interval_List_Ratio[i])
        print("Required Ratio List: ", Required_Ratio_List)
        # Output: [4,4,1..]
        print("\n")

        # Finding the sum of ratios
        Sum_Of_Ratios = 0
        for i in Required_Ratio_List:
            Sum_Of_Ratios += i
        print("Sum Of Ratios: ", Sum_Of_Ratios)
        print("\n")
        # Output: 54

        # Duration_According_Ratio tells what time should be given to each work in minutes according to ratio so that it get completed
        #  on time
        Duration_According_Ratio = []
        for i in Required_Ratio_List:
            Duration_According_Ratio.append(round(i/Sum_Of_Ratios * (Total_Fragment_Duration.total_seconds() / 60)))
        print("Duration According Ratio: ",Duration_According_Ratio)
        print("\n")
        # Output: [51, 51, 26...]

        # Sum_Dur_Acc_Rat is the sum of Duration_According_Ratio
        Sum_Dur_Acc_Rat = 0
        for i in Duration_According_Ratio:
            Sum_Dur_Acc_Rat += i
        print("Sum_Dur_Acc_Rat: ", Sum_Dur_Acc_Rat, "minutes")
        print("\n")
        # Output: 691

        # This part of code will ensure that the Sum of Ratios would not cross the line or say the "Proposed Left Time" or "Total Fragment Duration"
        if (Sum_Dur_Acc_Rat > (Total_Fragment_Duration.total_seconds() / 60)):
            Difference = int(Sum_Dur_Acc_Rat - (Total_Fragment_Duration.total_seconds() / 60))
            Duration_According_Ratio[-1] -= Difference

        # Creating a new DataFrame for Ratio Compressed Output
        TimeDelta_Minutes = []
        for i in range(0, len(Duration_According_Ratio)):
            TimeDelta_Minutes.append(timedelta(minutes=int(Duration_According_Ratio[i])))
        # print("TimeDelta_Minutes: ",TimeDelta_Minutes)
        # Output: [datetime.timedelta(seconds=3060), datetime.timedelta(seconds=3060),...]

        # Adding The Starting Time
        Compressed_Data = [[cur_time, cur_time + TimeDelta_Minutes[0], Prev_Work_List[0]]]  

        # Adding The Pinned Times
        for i in range(0, len(Pinned_Work_List)):  
            Compressed_Data.append([Pinned_Work_StartTiming[i], Pinned_Work_EndTiming[i], Pinned_Work_List[i]])

        # Making the DataFrame
        Compressed_DataFrame = pd.DataFrame(Compressed_Data, columns=['Start_', 'End_', 'Work_'])

        # Pinned_Timing_Reached Indicates till how many pinned timings have we compressed the schedule.
        Pinned_Timing_Reached = 0

        # New_Data_Created counts the newData which gets created by disintegrating a data in parts becasue of Pinned Timing overlapping.
        New_Data_Created = 0

        # Updated_Complete_Fragments is an updated list of Complete_Fragments list covering the changes made in the DataFrame including Pinned_Timings, new Timings and New_Data_Created which is also applicable for Updated_Dur_Acc_Rat and Updated_TimeDel_Min

        Updated_Complete_Fragments = Complete_Fragments[:]
        Updated_Dur_Acc_Rat = Duration_According_Ratio[:]

        Updated_LenTills_Dictionary = {}
        Updated_LenTills_List = []

        # Initially whole Updated_LenTills_Dictionary is made set to 0 and will make an increase as the schedule will start compressing with the loop
        for i in range(0, len(Nested_Fragments_List)):
            Updated_LenTills_Dictionary.update({"Updated_LenTillPin" + str(i+1) : 0})
        print("Updated_LenTills_Dictionary: ", Updated_LenTills_Dictionary)
        # Output: {'Updated_LenTillPin1': 0, 'Updated_LenTillPin2': 0, 'Updated_LenTillPin3': 0, 'Updated_LenTillPin4': 0}
        print("\n")

        # Below is function which updates the Updated_LenTills_List when Updated_LenTills_Dictionary gets updated
        def updateLenTillsList(Updated_LenTills_Dictionary, Updated_LenTills_List):
            Updated_LenTills_List.clear()
            for i in Updated_LenTills_Dictionary.values():
                Updated_LenTills_List.append(i)
                
        # Calling the function to execute
        updateLenTillsList(Updated_LenTills_Dictionary, Updated_LenTills_List)
        print("Updated_LenTills_List: ", Updated_LenTills_List)
        # Output: [0, 0, 0, 0]
        print("\n")

        # LenBtwUpdatedPins_Dic = {}
        # previous_value = None
        # differences = {}
        # for key, value in Updated_LenTills_Dictionary.items():
        #     if previous_value is not None:
        #         difference = value - previous_value
        #         differences[key] = difference
        #     previous_value = value

        newDuration = []

        for key1, key2, btwKey, LenKey in zip(LenTills_Dictionary.keys(), Updated_LenTills_Dictionary.keys(), LenBtwPins_Dictionary.keys(), range(0, len(Updated_LenTills_List))):
            
            # Adding the timings between Pinned_Timing 1 in a very wise way. Understand it Carefully. Thanks ChatGPT
            # We have used such type of range to cover the portion between start and First Pinned_work.

            # The if statement has been used with 1 in for loop because of which the else statement is used to remove that 1 value and make a standard for loop for rest of the works after Pinned work 1

            if (len(Updated_Complete_Fragments) == len(Complete_Fragments)):
                for i in range(1, LenTills_Dictionary[key1]):
                    newData = [[Compressed_DataFrame.End_[i-1], Compressed_DataFrame.End_[i-1] + TimeDelta_Minutes[i], Complete_Fragments[i]]]
                    upper_part = Compressed_DataFrame.loc[:i - 1]
                    lower_part = Compressed_DataFrame.loc[i:]
                    Compressed_DataFrame = pd.concat([upper_part, pd.DataFrame(newData, columns=['Start_', 'End_', 'Work_'], index=[i]), lower_part], ignore_index=True)
            else:
                for i in range(Updated_LenTills_List[LenKey-1], LenTills_List[LenKey] + Pinned_Timing_Reached + New_Data_Created):
                    newData = [[Compressed_DataFrame.End_[i-1], Compressed_DataFrame.End_[i-1] + Updated_TimDel_Min[i], Updated_Complete_Fragments[i]]]
                    upper_part = Compressed_DataFrame.loc[:i - 1]
                    lower_part = Compressed_DataFrame.loc[i:]
                    Compressed_DataFrame = pd.concat([upper_part, pd.DataFrame(newData, columns=['Start_', 'End_', 'Work_'], index=[i]), lower_part], ignore_index=True)


            #Sorting the rows on the basis of 'Start_' column with respect to time and resetting the index of dataframe.
            Compressed_DataFrame = Compressed_DataFrame.sort_values(by='Start_').reset_index(drop=True)

            # This function make the range of the loop according to the result of, if the Last Work has been pinned or not
            def LoopRangeDecide():
                if(FixedSelections != "" and len(dataframe) - 1 not in Pinned_Work_List):
                    return LenTills_Dictionary[key1] - 1
                else:
                    return LenTills_Dictionary[key1]

            # Rearranging the dataframe to make the timings continous in nature rather than broken apart.
            # We have used j for loop so to add those Pinned Time Diff without disturbing the break used in i's for loop.
            # We have used j for loop also because there will be 2 moments of overlapping, one is when the upper work overlapping the pinned work below it and second is when the pinned overlapping the work below it.

            for i in range(0, len(Compressed_DataFrame) - 1): 
                if(Compressed_DataFrame.End_[i] > Compressed_DataFrame.Start_[i+1]):
                    Pinned_Time_Diff = Compressed_DataFrame.End_[i+1] - Compressed_DataFrame.Start_[i+1]
                    Intersec_Diff = Compressed_DataFrame.End_[i] - Compressed_DataFrame.Start_[i+1]

                    # Used .loc[] here instead of (Compressed_DataFrame.End_[i] -= Intersec_Diff) because this beside method is called chain-indexing which may actually modify the copy of the dataframe instead of modifying the original. In Future, this rule will become strict

                    Compressed_DataFrame.loc[i, "End_"] -= Intersec_Diff
                    for j in range(0, len(Compressed_DataFrame['Start_'])-1):
                        if(Compressed_DataFrame.End_[j] > Compressed_DataFrame.Start_[j+1]):
                            Compressed_DataFrame.loc[j+1, "Start_"] += Pinned_Time_Diff
                            Compressed_DataFrame.loc[j+1, "End_"] += Pinned_Time_Diff
                            # Making a broken and adjusted copy of a work(Work 5) which was colliding with Pinned Work 2
                    newData = [[Compressed_DataFrame.End_[i+1], Compressed_DataFrame.End_[i+1] + Intersec_Diff, f"{Compressed_DataFrame.Work_[i]} (Part 2)"]]
                    upper_part = Compressed_DataFrame.loc[:i + 1]
                    lower_part = Compressed_DataFrame.loc[i + 2:]
                    Compressed_DataFrame = pd.concat([upper_part, pd.DataFrame(newData, columns=['Start_', 'End_', 'Work_']), lower_part], ignore_index=True)
                    New_Data_Created += 1
                    break


            if (len(Updated_Complete_Fragments) == len(Complete_Fragments)):
                # print("\n")
                print("Structured Code: ", "(", LenKey, ")")
                print(Compressed_DataFrame)
                print("\n")
                # print("len(Updated_Complete_Fragments) == len(Complete_Fragments)")
                Pinned_Timing_Reached += 1
                Updated_LenTills_Dictionary[key2] = LenTills_Dictionary[key1] + Pinned_Timing_Reached + New_Data_Created

                updateLenTillsList(Updated_LenTills_Dictionary, Updated_LenTills_List)

                # print("Updated_Fragments for debugging: ", Updated_Complete_Fragments[0: LenTills_Dictionary[key1]])
                Updated_Complete_Fragments[0: LenTills_Dictionary[key1]] = Compressed_DataFrame.Work_[0: LenTills_Dictionary[key1] + Pinned_Timing_Reached + New_Data_Created]

                # print("Updated_LenTills_Dictionary[key2]: ", Updated_LenTills_Dictionary[key2])
                # print("LenBtwPins_Dictionary[btwKey]: ", LenBtwPins_Dictionary[btwKey])
                print("Updated_LenTills_List: ", Updated_LenTills_List)
                print('\n')
                print("Updated Complete Fragments: ", Updated_Complete_Fragments)
                # Output: ['Work 1', 'Work 2', 'Work 2 Break',..]
                print('\n')

                for i in range(0, Updated_LenTills_Dictionary[key2]):
                    newDuration.append(int((Compressed_DataFrame.End_[i] - Compressed_DataFrame.Start_[i]).total_seconds()/60))
                Updated_Dur_Acc_Rat[0: LenTills_Dictionary[key1]] = newDuration[0: LenTills_Dictionary[key1] + Pinned_Timing_Reached + New_Data_Created]
                print("Updated_Dur_Acc_Rat: ", Updated_Dur_Acc_Rat)
                # Output: [51, 51, 13,...]
                print("\n")

                # Updated_TimeDel_Min is the updated version of TimeDelta_Minutes accompanying the change made in dataframe.
                Updated_TimDel_Min = []
                for i in range(0, len(Updated_Dur_Acc_Rat)):
                    Updated_TimDel_Min.append(timedelta(minutes=int(Updated_Dur_Acc_Rat[i])))
                # print("Updated_TimeDel_Min: ", Updated_TimDel_Min)
                # Output: [datetime.timedelta(seconds=3060), datetime.timedelta(seconds=3060),..]
                # print("\n")
            else:
                # print("\n")
                print("Structured Code: ", "(", LenKey, ")")
                print(Compressed_DataFrame)
                print("\n")
                print("len(Updated_Complete_Fragments) != len(Complete_Fragments)")

                if(FixedSelections != "" and len(dataframe) - 1 not in Pinned_Work_List and (LenKey == len(Updated_LenTills_Dictionary) - 1)):
                    Pinned_Timing_Reached += 0
                else:
                    Pinned_Timing_Reached += 1

                Updated_LenTills_Dictionary[key2] = LenTills_Dictionary[key1] + Pinned_Timing_Reached + New_Data_Created

                updateLenTillsList(Updated_LenTills_Dictionary, Updated_LenTills_List)

                # print("Updated_Fragments for debugging: ", Updated_Complete_Fragments[Updated_LenTills_List[LenKey-1]: Updated_LenTills_List[LenKey-1] + LenBtwPins_Dictionary[btwKey]])

                # print("Second Updated_Fragments for debugging: ", Compressed_DataFrame.Work_[Updated_LenTills_List[LenKey-1]: Updated_LenTills_List[LenKey]])

                Updated_Complete_Fragments[Updated_LenTills_List[LenKey-1]: Updated_LenTills_List[LenKey-1] + LenBtwPins_Dictionary[btwKey]] = Compressed_DataFrame.Work_[Updated_LenTills_List[LenKey-1]: Updated_LenTills_List[LenKey]]

                print("Updated_LenTills_List: ", Updated_LenTills_List)
                print("\n")
                print("Updated Complete Fragments: ", Updated_Complete_Fragments)

                # print("LenKey: ", LenKey)
                # print("LenBtwPins_Dictionary[btwKey]: ", LenBtwPins_Dictionary[btwKey])
                # print("Updated LenTills Dictionary: ", Updated_LenTills_Dictionary)
                # print("Updated Complete Fragments: ", Updated_Complete_Fragments)
                # Output: ['Work 1', 'Work 2', 'Work 2 Break',..]
                print('\n')

                for i in range(Updated_LenTills_List[LenKey-1], Updated_LenTills_List[LenKey]):
                    # print("Compressed_DataFrame.End: ", Compressed_DataFrame.End_)
                    newDuration.append(int((Compressed_DataFrame.End_[i] - Compressed_DataFrame.Start_[i]).total_seconds()/60))
                Updated_Dur_Acc_Rat[Updated_LenTills_List[LenKey-1]: Updated_LenTills_List[LenKey-1] + LenBtwPins_Dictionary[btwKey]] = newDuration[Updated_LenTills_List[LenKey-1]: Updated_LenTills_List[LenKey]]
                print("Updated_Dur_Acc_Rat: ", Updated_Dur_Acc_Rat)
                # Output: [51, 51, 13,...]
                # print("Len of Updated_Dur_Acc_Rat: ", len(Updated_Dur_Acc_Rat))
                print("\n")

                # Updated_TimeDel_Min is the updated version of TimeDelta_Minutes accompanying the change made in dataframe.
                Updated_TimDel_Min = []
                for i in range(0, len(Updated_Dur_Acc_Rat)):
                    Updated_TimDel_Min.append(timedelta(minutes=int(Updated_Dur_Acc_Rat[i])))
                # print("Updated_TimeDel_Min: ", Updated_TimDel_Min)
                # Output: [datetime.timedelta(seconds=3060), datetime.timedelta(seconds=3060),..]
                # print("Len of Updated_TimeDel_Min: ", len(Updated_TimDel_Min))
                print("\n")

    # print(Compressed_DataFrame)
    Start_Timing = []
    End_Timing = []
    Start_Angle = []
    End_Angle = []

    for i in range(len(Compressed_DataFrame["Start_"])):
        Start_Timing.append((str(Compressed_DataFrame["Start_"][i]).split(" ")[1])[:5])
        End_Timing.append((str(Compressed_DataFrame["End_"][i]).split(" ")[1])[:5])

    for i in range(0, len(Start_Timing)):
        Start_Hour = int(Start_Timing[i].split(":")[0])
        Start_Min = int(Start_Timing[i].split(":")[1])
        End_Hour = int(End_Timing[i].split(":")[0])
        End_Min = int(End_Timing[i].split(":")[1])
        Start_Angle.append(30*Start_Hour + 0.5*Start_Min)
        End_Angle.append(30*End_Hour + 0.5*End_Min)

    if(FixedSelections == ""):
        DataFrame_Dict = {
            "Start_Angle": Start_Angle,
            "End_Angle": End_Angle,
            "Start_Timing": Start_Timing,
            "End_Timing": End_Timing,
            "Work": Complete_Fragments,
            "Durations": Duration_According_Ratio
        }
    else:
        DataFrame_Dict = {
            "Start_Angle": Start_Angle,
            "End_Angle": End_Angle,
            "Start_Timing": Start_Timing,
            "End_Timing": End_Timing,
            "Work": Updated_Complete_Fragments,
            "Durations": Updated_Dur_Acc_Rat
        }
    print("DataFrame_Dict: ", DataFrame_Dict)
    print(Compressed_DataFrame)
    return DataFrame_Dict

# CompressionFunction("05/01/2025 10:00", "0,1", "5", "1")
# CompressionFunction("05/01/2025 10:00", "0,1,2", "5, 8", "")
# 0 - Physics
# 1 - Chemistry
# 2 - Maths
# 3 - Biology
# 4 - SST - Time
# 5 - Economics
# 6 - Sanskrit
# 7 - Business
# 8 - Art
# 9 - Sports
# 10 - Cooking
# 11 - Hindi
