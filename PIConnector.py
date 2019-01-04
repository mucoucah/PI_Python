import PIthon as PIConnect

#uncomment lines to execute commands. 
#suggested usage: run the tag names function to extrac names to csv. 
#select tagnames to pull data (just delete the ones not required)
#run the values from a list function and the results will be in a csv file.

## connect to server (connection is read-only)
PIConnect.connect_to_Server("server_name", "username")  


## snapshot data
# INPUT
# single tag name e.g: 'SINUSOID'
# OUTPUT
# print the tag name and most recent recorded value to screen

PIConnect.get_tag_snapshot('SINUSOID')


## recorded values
# INPUT
# single tag name e.g: 'SINUSOID'
# start time
# end time
# OUTPUT
# pandas dataframe with *recorded* values over the interval for all tags in csv format

#df = PIConnect.get_tag_values('SINUSOID','1/19/2018 11:00:00 AM','1/20/2018 11:30:00 AM')


## summary data (such as averages over an interval)
# INPUT
# single tag name e.g: 'SINUSOID'
# start time
# end time
# time span for calculation
# save to csv file (true) or not (false)
# OUTPUT
# pandas dataframe with average values over the interval for all tags in csv format

#df = PIConnect.get_summary_values('SINUSOID','1/19/2018 11:00:00 AM','1/20/2018 11:30:00 AM','60s',True)


## tag names
# INPUT
# mask for tag search on server. Use '*' to return ALL tags
# OUTPUT
# pandas dataframe with tag name, unit of measure and descripton in csv format

df = PIConnect.find_tags('PIC*.*')    


## values from a list of tags
# INPUT
# list of tags in CSV format
# start time
# end time
# time span for calculation
# gzip file (true) or csv (false)
# OUTPUT
# pandas dataframe with average values over the interval for all tags in csv format

#df = PIConnect.list_of_points("tags_list.csv",'1/19/2018 11:00:00 AM','1/20/2018 11:30:00 AM','60s',False)


## disconnect from server
#PIConnect.Disconnect() AF SDFK takes care of disconnecting.

## output data to screen
#print (df[:10])
