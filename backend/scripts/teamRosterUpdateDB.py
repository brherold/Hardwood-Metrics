from models import *
from sqlalchemy import *
from datetime import *
import os


#Should Clear TeamRosterPage and get new for Development Days and update the new playerskills to DB
#Make POST request for Updating Team Roster and call on all teams    

#For not only updating TeamRosterInfo (checking in TeamRosterPage Folder) when its Thursday or Sunday (Development Days)

today = date.today()

# Get weekday as an integer (Monday is 0, Sunday is 6) (3 or 6)
weekday_number = today.weekday()

    
if weekday_number in [3,6]: #If the day is Thursday or Sunday (Dev Days) 
    #delete_file(cache_filename)