from bs4 import BeautifulSoup
import requests
import os

#Gets Team Conference for that Year


#Caching Team Info for the year
def save_html_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to load HTML content from a local file
def load_html_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()





def get_team_conference(teamCode,seasonYear):
    #outputs team_id, team_name
    teamURL = "http://onlinecollegebasketball.org/team/" + str(teamCode)

    cache_folder = "backend/TeamConferencePage"
    
    cache_filename = os.path.join(cache_folder, f"{teamCode}-{seasonYear}.html")
    
    
    try:
        # Try to load HTML content from the local cache
        page = load_html_from_file(cache_filename)
        
        
    except FileNotFoundError:
        # If not found, fetch the content from the URL
        page = requests.get(teamURL)

        # Save HTML content to the local cache
        save_html_to_file(page.text, cache_filename)
        page = page.text 


    soup = BeautifulSoup(page, "html.parser")

    conference_id = int(soup.find("div", {"id":"Main"}).find_all("a")[1]["href"].split("/")[-1])

    return conference_id

#print(get_team_conference(1,2044))

