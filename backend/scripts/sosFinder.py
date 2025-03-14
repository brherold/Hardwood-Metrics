from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
import glob

#USE PYTHON ANACADONA 3.8.5 to RUN

#Returns Dictionary key(teamID): value (sos) of all teams and their sos (Strenghth of Schedule)

def save_html_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to load HTML content from a local file
def load_html_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def sos_holder():

    url= "http://onlinecollegebasketball.org/rankings/1/2/0"
    
    #Caches for day
    cache_folder = "backend"
    month_day = datetime.now().strftime("%m-%d")
    
    cache_filename = os.path.join(cache_folder, f"TeamRankings{month_day}.html")

    
    try:
        # Try to load HTML content from the local cache
        page = load_html_from_file(cache_filename)
        
        
    except FileNotFoundError:
        # Get all files that contain "TeamRankings" in their name
        files = glob.glob("*TeamRankings*")

        # Delete each file
        for file in files:
            os.remove(file)
            print(f"Deleted: {file}")

        # If not found, fetch the content from the URL
        page = requests.get(url)

        # Save HTML content to the local cache
        save_html_to_file(page.text, cache_filename)
        page = page.text #to fit in with variable names for soup 


        


    soup = BeautifulSoup(page,"html")




    teamsTrArr = soup.find("table").find_all("tr")[1:]

    teamSOSDic = {}
    for teamTr in teamsTrArr:
        teamID = teamTr.find_all("td")[1].find("a")["href"].split("/")[-1]
        teamSOS = float(teamTr.find_all("td")[8].text)
        teamSOSDic[teamID] = teamSOS
        
    return teamSOSDic

