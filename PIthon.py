#based on the information from blog https://pisquare.osisoft.com/community/developers-club/pi-net-framework-pi-af-sdk/blog/2017/03/30/python-36-and-afsdk-example
# and various internet sources

import sys  
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')  
import clr 
import pandas as pd
import csv

# import libraries from pythonnet
clr.AddReference('OSIsoft.AFSDK') 
from OSIsoft.AF import *
from OSIsoft.AF.PI import *  
from OSIsoft.AF.Search import *  
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import * 
from System.Net import NetworkCredential

#from System.Collections.Generic import Dictionary

#connect to the server using a generic name
def connect_to_Server(serverName, username):  
    piServers = PIServers()  
    #piServers = PISystems()  
    global piServer  
    netcred = NetworkCredential(username,None)
    piServer = piServers[serverName]  
    piServer.Connect(netcred)  

#get a snapshot of a tag with most recent values  
def get_tag_snapshot(tagname): 
    print("tag snapshot")
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    lastData = tag.Snapshot()  
    return print(lastData.Value, lastData.Timestamp)  

#get the recorded values (events) of a tag within a specific time span
#return "point_values_list.csv"
def get_tag_values(tagname,timestart,timeend):
    tag = PIPoint.FindPIPoint(piServer, tagname)
    timeRange = AFTimeRange(timestart,timeend)
    boundary = AFBoundaryType.Inside
    data = tag.RecordedValues(timeRange,boundary,'',False,0)
    dataList = list(data)
    df=pd.DataFrame(columns=['Date',tagname]) 
    for i, sample in enumerate(data):
        df.loc[i] = str(sample.Timestamp), sample
    #df.set_index('Date')
    df.to_csv("point_values_list.csv")
    return df

#get the time weighted averaged values of a tag within aspecific time span
#return a concatenated dataframe
def get_summary_values(tagname,timestart,timeend,interval='1h', save_to_file = False):
    tag = PIPoint.FindPIPoint(piServer, tagname)
    name = tag.Name.lower()  
    timeRange = AFTimeRange(timestart,timeend)
    summary_type = AFSummaryTypes.Average
    calc_basis = AFCalculationBasis.TimeWeighted
    span = AFTimeSpan.Parse(interval) 
    df = pd.DataFrame(columns=('Date', tagname) )
    try:
        summaries = tag.Summaries(timeRange, span, summary_type, calc_basis, AFTimestampCalculation.Auto)  
    except:
        return df
    for summary in summaries:  
        i=0
        for event in summary.Value:  
            df.loc[i] =  event.Timestamp.LocalTime, event.Value
            i=i+1            
    if (save_to_file): df.to_csv("summary_values_list.csv")
    return df

#get all tag names from server using a mask (or use * for all)
#return  "tags_list.csv"
def find_tags(mask="none.*"):
    points = PIPoint.FindPIPoints(piServer, mask, None, None)
    df= pd.DataFrame(columns=('Tag', "engunits", "Descriptor"))
    i=0
    for point in list(points):
        attr = point.GetAttributes("engunits", "Descriptor")
        df.loc[i] =  point.get_Name(), attr["engunits"] ,attr["Descriptor"]
        i=i+1            
    df.to_csv("tags_list.csv")
    return df

 
#using the tag list from the csv and build a table of time vs tag values for all
#return a csv or compressed gzip file with all the data "merged_list.csv"
def list_of_points(filename, timestart,timeend,interval='1h', compression=False):
    df3 = pd.DataFrame(columns=('Tag', "engunits", "Descriptor"))
    df3 = pd.read_csv('tags_list.csv', skipinitialspace=True)
    tag_list = list(df3['Tag'])
    df = pd.DataFrame()
    for tagname in tag_list:
        df2 = pd.DataFrame()
        df2 = get_summary_values(tagname,timestart,timeend,interval,False)
        print(df2[:5])
        if df.size <1:
            df = df2
        else:
            df = pd.merge(df,df2[['Date',tagname]],on='Date', how='left')
    if compression:
        df.to_csv("merged_list.gz", compression='gzip')
    else:
        df.to_csv("merged_list.csv")
            
    return df

