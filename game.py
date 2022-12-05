import info
import Controller

lives = 3
num_correct = 0
round_count = 1

#name of the wiki pages:
page1 = "Cat"
page2 = "Dog"
game_over = False

wiki1 = info.Wikipedia(page1)
wiki2 = info.Wikipedia(page2)

game = Controller.Controller(page1 + "\n" + wiki1.summary(), page2 + "\n" + wiki2.summary())

game.start_menu_loop()

answer = 1
iteration = 0
if game.STATE == "game":
    while not game_over:
        iteration+=1

        #updates/changes the wikipedia page name every round:
        if (round_count != 1):
            page1 = rand_links1
            page2 = rand_links2
        

        #wikipedia object (from class made in the info python file)
        wiki1 = info.Wikipedia(page1)
        wiki2 = info.Wikipedia(page2)
        
        print("\n\n\n SUMMARY:\n")
        #print(wiki2.summary()[0:30])
        #game.set_text_right("cupcakes and waffles are very good foods to eat")
        if round_count > 3:
            game.set_text_right(wiki2.summary())
            game.set_text_left(wiki1.summary())
        game.game_screen_loop(answer)
        #game.end_screen_loop()
        print(game.health)
        print(game.correct)

        if iteration >= 3:
            exit = input("exit?")
            if exit == "y":
                game_over = True

        #Number of links on each respective page:
        links1 = wiki1.links()[1]
        links2 = wiki2.links()[1]

        #Selects a random link from one of the pages:
        rand_links1 = wiki1.randomlinks(1)[0][0]
        rand_links2 = wiki2.randomlinks(1)[0][0]

        #produces what the correct answer is:
        answer = None
        if (links1 > links2):
            answer = 1
        else:
            answer = 2

        #gets rid of the '/wiki/' text from the rand_links variables so it can 
        #be used in the Wikipedia class again for the next iteration of the loop
        rand_links1 = rand_links1[6:]
        rand_links2 = rand_links2[6:]

        #Lose condition:
        if (game.health <= 0):
            game_over = True
            print("You ran out of lives! You lose!")
        #Win condition:
        elif (game.correct >= 5): 
            game_over = True
            print("You guessed 5 articles correctly! You Win!")

        round_count += 1
        print("\n\n")