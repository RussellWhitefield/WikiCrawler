# WikiCrawler
Respository for the HARP151 Group Project with Kaitlyn Matthews,  Russell Whitefield, Dion Cenalia, Nashara Marrow, Preston Muirhead, Samuel Ramos (Fall 2022)

We want to create a research tool that can gamify research and can map out topics of interest in an interesting way. 

The prototype we are working on this semester would specifically allow you to explore wikipedia like one would a pixelated dungeon crawler. Here is the interaction we are trying to create:

At the start menu, a user would type in the url of an article
The program would visualize that article in the form of a room 
All of the links in the article would be represented as doors to other rooms
The player would be able to move an avatar to other rooms, and therefore navigate through articles like one would a dungeon crawler. 
	
Parts of the game
All buttons and sprites are done with 2dAnimatable Class
Start Menu - 
    Clicking start button leads to prompt for user input, searches wikipedia, uses WikiDungeonCrawler to generate 3 links, and puts them into an array.
    Sends the player to the game screen.
Game Loop - 
Exit loop
    Quits the game with pygame functions
