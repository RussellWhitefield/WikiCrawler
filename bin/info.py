from bs4 import BeautifulSoup
import requests
from random import randint

undesirable = [
    '/wiki/Wikipedia:Please_clarify',
    '/wiki/Wikipedia:Citation_needed',
    '/w/',
    'disambiguation',
    'wiktionary',
    '/wiki/Wikipedia:Manual_of_Style/Dates_and_numbers#Chronological_items',
    '/wiki/Help:IPA/English',
    '/wiki/Wikipedia:Citing_sources'
]

class Wikipedia:
    def __init__(self, search_term):
        self.search_term = search_term
        
    def test(self):
        print(self.search_term)
        address = f"/wiki/{self.search_term}"
        print(address)
        
    def titles(self):
        address = f"/wiki/{self.search_term}"
        ## This converts the search term to a format Wikipedia will recognise.
        site = requests.get(f"https://en.wikipedia.org/{address}").text
        soupsite = BeautifulSoup(site, "lxml")
        ## Requesting website.
        
        paragraphs = soupsite.find_all("p")
        ## Generating a list of every paragraph.

        a_tags = []
        for i in paragraphs:
            try:
                a_tags.append(i.find_all("a"))
                ## Generating a list of every  tag.
            except:
                ## The try-except condition is a failsafe for any paragraph not containing any  tags.
                ## To be honest I forgot what this did, but it works. 
                pass
            
            a_titles = []
            for i in a_tags:
                for j in i:
                    if j.get("title") == None:
                        ## Some  tags contain no titles whatsoever, so I'm filtering them out to prevent issues later on.
                        pass
                    else:
                        a_titles.append(j.get("title"))
                        ## Grabbing the titles from every  tag.
                                
        print(a_titles)
        
    def links(self):
        ## Same as titles(self)
        address = f"/wiki/{self.search_term}"
        site = requests.get(f"https://en.wikipedia.org{address}").text
        soupsite = BeautifulSoup(site, "lxml")

        paragraphs = soupsite.find_all("p")
        
        a_tags = []
        for i in paragraphs:
            try:
                a_tags.append(i.find_all("a"))
            except:
                pass
            
            a_links = []
            ## Different variable name in case I want to make both above's and this one's global.
            for i in a_tags:
                for j in i:
                    if j.get("title") == None:
                        pass
                    else:
                        a_links.append(j.get("href"))
                        ## Grabbing the links from every  tag.
        #return (a_links, len(a_links))
        return a_links
        #print(a_links)
        #print(len(a_links))
        
    def summary(self):
        address = f"/wiki/{self.search_term}"
        site = requests.get(f"https://en.wikipedia.org{address}").text
        soupsite = BeautifulSoup(site, "lxml")
        

        #div = soupsite.find("div", class_="toc")

        #if div == None:
        div = soupsite.find("div", class_="vector-body")
            #print("THIS IF STATEMENT HAPPENED")
        summary = div.find("p", class_="").text.strip()
        #print(summary)
        #else:
         #   summary = div.find_previous_siblings("p")
          #  print("All is good")



        ## Wikipedia universally structures its webpages so that a "div" or section with the class "toc" represents the Table of Contents.
        ## Naturally, everything paragraph above the Table of Contents should be the summary.
        
        
        #summary = div.find_previous_siblings("p")


        #sum = ""
        #for i in list(reversed(summary)):
            ## I use "reversed()" because the ".find_previous_siblings()" method reads bottom to top,
            ## which returns the summary backwards.
            #print(i.text.strip())
         #   sum += i.text.strip()
        return summary
        
    def randomlinks(self, iterations):
        address = f"/wiki/{self.search_term}"
        site = requests.get(f"https://en.wikipedia.org{address}").text
        soupsite = BeautifulSoup(site, "lxml")

        paragraphs = soupsite.find_all("p")
        
        a_tags = []
        for i in paragraphs:
            try:
                a_tags.append(i.find_all("a"))
            except:
                pass
            
            a_links = []
            for i in a_tags:
                for j in i:
                    if j.get("title") == None:
                        pass
                    else:
                        a_links.append(j.get("href"))
        
        ## This plays out the same way as all previous executions.
                        
        x = 0
        global random_links
        ## Setting this list as a global variable allows me access to it any time.
        random_links = []
        random_places = []
        while x != iterations:
            random_place = randint(1,(len(a_links)-1))
            #print(random_place)
            random_places.append(random_place)
            if any(i in a_links[random_place] for i in undesirable):
                random_links.append(a_links[random_place+1])
            else:
                random_links.append(a_links[random_place])
            x += 1
        #print(random_links)
        return (random_links, random_places)
        ## I just need a readout of some number of randomly generated links to create the web. 
        
    def dungeonlinks(self, iterations):
        site = requests.get(f"https://en.wikipedia.org{self.search_term}").text
        soupsite = BeautifulSoup(site, "lxml")

        paragraphs = soupsite.find_all("p")
        
        a_tags = []
        for i in paragraphs:
            try:
                a_tags.append(i.find_all("a"))
            except:
                pass
            
            a_links = []
            for i in a_tags:
                for j in i:
                    if j.get("title") == None:
                        pass
                    else:
                        a_links.append(j.get("href"))
        
        ## This plays out the same way as all previous executions.
                        
        x = 0
        global random_links
        ## Setting this list as a global variable allows me access to it any time.
        random_links = []
        while x != iterations:
            random_place = randint(1,(len(a_links)-1))
            print(random_place)
            if any(i in a_links[random_place] for i in undesirable):
                ## The any() function will actually search strings iteratively for strings in a list.
                random_links.append(a_links[random_place+1])
            else:
                random_links.append(a_links[random_place])
            x += 1
        print(random_links)
        ## I just need a readout of some number of randomly generated links to create the web. 
                
    def rand_summary(self):
        for i in random_links:
            site = requests.get(f"https://en.wikipedia.org{i}").text
            soupsite = BeautifulSoup(site, "lxml")
            
            div = soupsite.find("div", class_="toc")
            summary = div.find_previous_siblings("p")
            for j in list(reversed(summary)):
                print(j.text)

wiki = Wikipedia("Cats")
links = wiki.links()[1]

#print(wiki.randomlinks(3))


def wiki_page(page):
    wiki_ = Wikipedia(page)
    return wiki_

def getLinks(wiki):
    wiki.links()[1]

def common_links(search_term1, search_term2):
    room_one = Wikipedia(search_term1)
    room_two = Wikipedia(search_term2)
    
    links_one = room_one.links()
    links_two = room_two.links()
    
    if len(links_one) > len(links_two):
        for i in links_one:
            if i in links_two:
                print(i)
    else:
        for i in links_two:
            if i in links_one:
                print(i) 

"""       
def dungeon_crawler(search_term, seed):
    print(search_term)
    room_one = Wikipedia(search_term)
    try:
        room_one.randomlinks(seed)
        ## For first run
    except:
        room_one.dungeonlinks(seed)
        ## For iteration
    global new_rooms
    new_rooms = []
    for i in random_links:
        print(i)
        next_room = Wikipedia(i)
        number = randint(1, seed+1)
        ## Variables for the following methods.
        next_room.dungeonlinks(number)
        new_rooms.append(random_links)
        ## random_links gets reassigned each loop and folded into new_rooms
    print(new_rooms)

dungeon_crawler("Math",3)
"""