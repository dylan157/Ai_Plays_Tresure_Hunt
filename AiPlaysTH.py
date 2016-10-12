from random import randint
from sys import platform
import os
import time

if platform == "linux" or platform == "linux2":
    clear = lambda: os.system('clear')
elif platform == "darwin":
    clear = lambda: os.system('clear')
elif platform == "win32":
    clear = lambda: os.system('cls')


def d3bug_bot(bot_speed, who):
    global bot_memory
    global print_board
    global max_step
    global Chests_Bandits
    global re_use

    # Targets/Avoids ----------------------------------------------------------------------------------------------------------------
    #The bot will prioritize targets in acending order (EG. if generated_move == targets[0]. Elif generated_move == targets[1] etc...)
    #The bot will never land on avoid items
    targets = [land_icon, chest_icon, used_land_icon, Bot_0_icon, Bot_1_icon] 
    avoid = [bandit_icon] 

    while True: 
        thoughts = []
        for generated_move in range((bot_memory)):
            #This for loop generates an interger amount of moves to later test
            def choice_gen():
                rand_udlr = randint(0, 3)
                rand_step = randint(1, max_step)
                mover = ""
                if rand_udlr == 0:
                    mover += 'u'
                elif rand_udlr == 1:
                    mover += 'd'
                elif rand_udlr == 2:
                    mover += 'l'
                elif rand_udlr == 3:
                    mover += 'r'
                mover += str(rand_step)
                if mover in thoughts:
                    return choice_gen()
                return mover
            thoughts.append(choice_gen())

        for target in targets:
            for out in thoughts:
                if len(thoughts) == 0:
                    pass

                elif out[0] == "u":
                    if who[0] - int(out[1]) >= 0: # UP (-X, 0)
                        if playerboard[(who[0] - int(out[1]))][who[1]]in (target):
                            if playerboard[(who[0] - int(out[1]))][who[1]] not in (avoid):
                                return out
                                break
                    else:
                        thoughts.remove(out)

                elif out[0] == "d":
                    if (who[0] + int(out[1])) < (len(object_board)): # DOWN (+X, 0)
                        if playerboard[(who[0] + int(out[1]))][who[1]] in (target):
                            if playerboard[(who[0] + int(out[1]))][who[1]] not in (avoid):
                                return out
                                break
                    else:
                        thoughts.remove(out)

                elif out[0] == "r":
                    if who[1] + int(out[1]) < (len(object_board)): # RIGHT (0, +X)
                        if playerboard[who[0]][(who[1] + int(out[1]))] in (target):
                            if playerboard[who[0]][(who[1] + int(out[1]))] not in (avoid):
                                return out
                                break
                    else:
                        thoughts.remove(out)

                elif out[0] == "l":
                    if who[1] - int(out[1]) >= 0: # LEFT (0, -X)
                        if playerboard[who[0]][(who[1] - int(out[1]))] in (target):
                            if playerboard[who[0]][(who[1] - int(out[1]))] not in (avoid):
                                return out
                                break
                    else:
                        thoughts.remove(out)

    else:
        em = "What?"


#------------------------------------------------------------------------------------------------------- Varibles
Chests_Bandits = {    
    "chests": 35,
    "bandit": 5
}
#boring varibles
player_score = 0
Used_coordinates = []

object_board = []
memory_board = []
playerboard = []
error_message = ""
Game_activation = False

#other varibles
win = 1500
Map_Size_X_Y = 8
re_use = "u1"

#bot varibles
d3bug = True
bot_speed = 0.1
bot_memory = 8
max_step = 2

#Icons
land_icon = ' '
used_land_icon = '~'
Bot_0_icon = '#'
Bot_1_icon = '@'
bandit_icon = 'X'
chest_icon = '$'

#------------------------------------------------------------------------------------------------------- Icon length
icon_length = len(Bot_0_icon)
bandit = bandit_icon*icon_length
chest = chest_icon*icon_length


#------------------------------------------------------------------------------------------------------- Map writer
for click in range(Map_Size_X_Y):
    object_board.append([used_land_icon*icon_length] * Map_Size_X_Y)
    playerboard.append([land_icon*icon_length] * Map_Size_X_Y)
    memory_board.append([0*icon_length] * Map_Size_X_Y)

#------------------------------------------------------------------------------------------------------- Menu
def menu():
    global Game_activation
    global error_message
    global timer0
    while Game_activation != True:       
        clear()
        print error_message
        error_message = ""
        print "Welcome to Bandits & Gold!"
        print "Enter navigation number:"
        print "Start = '1'"
        start = raw_input('Enter: ')
        if start == '1':
            Game_activation = True
            print Game_activation
            break
        else:
            print 'What?'
menu()

#------------------------------------------------------------------------------------------------------- Random object to map placer
def Object_Placement(ran_len, WHO):
    spot = []
    for x in range(ran_len): # How many random numbers?
        x, z = 0, 0        
        def baker():
            global x
            global z
            x, z = randint(0, (len(object_board)-1)), randint(0, (len(object_board)-1))            
            if (str(x) + str(z)) in Used_coordinates: # or (str(x) + str(z)) in Used_coordinates:
                #print "XZ FOUND IN SPOT", (str(x) + str(z))
                baker()
            elif (str(x) + str(z)) in spot:
                #print "XZ FOUND IN USED COORDINATES", (str(x) + str(z))
                baker()
            else:
                object_board[x][z] = WHO
                Used_coordinates.append(str(x) + str(z))
                spot.append(str(x) + str(z))
                           
        baker()

    if len(spot) > ran_len:
        print "OVERFLOW!"
    return spot
    Used_coordinates.append(spot)
Chests_Bandits['chests'] = Object_Placement(Chests_Bandits['chests'], chest)
Chests_Bandits['bandit'] = Object_Placement(Chests_Bandits['bandit'], bandit)
#------------------------------------------------------------------------------------------------------- Print board
def print_board(board):
    for row in board:
        for x in range(icon_length):
            print "  ".join(row)
        print ""

#------------------------------------------------------------------------------------------------------- Player start location
Bot_0 = [(len(object_board)-1), 0, 0]
Used_coordinates.append(str(Bot_0[0]) + str(Bot_0[1]))


Bot_1 = [(len(object_board)-1), (len(object_board)-1), 1]
Used_coordinates.append(str(Bot_1[0]) + str(Bot_1[1]))


active_bots = [Bot_0, Bot_1]

bot_0_score = 0
bot_1_score = 0

#------------------------------------------------------------------------------------------------------- Board transport
def board_transport(move_choice, em, who):
    #Board transport determins if the move it has been ordered to process is legal or not (valid input and on-map) 
    #Once the move has been validated, the players current location is re-written and returned to be further processed by the game loop.
    global error_message
    global player_score
    global clear


    if move_choice == "d3bug":
        player_score = 15766
    em = move_choice
    if move_choice == "RESET":
        who[0] = 0
        who[1] = 0

    if len(move_choice) == 2 and move_choice[0] in ('u', 'd', 'l', 'r') and move_choice[1] in str(range(0, len(object_board))): 
        if move_choice[0] == "u":
            if who[0] - int(move_choice[1]) < 0: #UP
                em = "You can't move there!"
            else:
                who[0] -= int(move_choice[1]) 

        elif move_choice[0] == "d":
            if (who[0] + int(move_choice[1])) > (len(object_board)-1): #DOWN

                em = "You can't move there!"
            else:
                who[0] += int(move_choice[1])
        elif move_choice[0] == "r":
            if who[1] + int(move_choice[1]) > (len(object_board)-1): #RIGHT

                em = "You can't move there!"
            else:
                who[1] += int(move_choice[1])
        elif move_choice[0] == "l":
            if who[1] - int(move_choice[1]) < 0: #LEFT

                em = "You can't move there!"
            else:
                who[1] -= int(move_choice[1])
        else:
            em = "What?"
    else:
        em = "Unreadable input"
    error_message = em
    return who


#------------------------------------------------------------------------------------------------------- Game Loop
while bot_0_score < win or bot_1_score < win:
    while Game_activation:
        if bot_0_score >= win:
            print "bot # won!"
            Game_activation = False
            break
        elif bot_1_score >= win:
            print "bot @ won!"
            Game_activation = False
            break
        def turn(BOT):
            global error_message
            global bot_0_score
            global bot_1_score
            player_score = 0
            #Move choice
            if d3bug == False:
                desired_move = raw_input("Where to move?")
            else:
                desired_move = d3bug_bot(bot_speed, BOT)
            board_transport(desired_move, error_message, BOT)

            if object_board[BOT[0]][BOT[1]] == bandit: #Object logic
                player_score = 666
            if object_board[BOT[0]][BOT[1]] == chest:
                if memory_board[BOT[0]][BOT[1]] == 3:
                    player_score += 10
                    playerboard[BOT[0]][BOT[1]], object_board[BOT[0]][BOT[1]] = bandit, bandit # Make chest into bandit
                else:
                    player_score += 10

            if BOT == Bot_0:
                if player_score == 666:
                    bot_0_score = 0
                    player_score = 0
                bot_0_score += player_score
            elif BOT == Bot_1:
                if player_score == 666:
                    bot_1_score = 0
                    player_score = 0
                bot_1_score += player_score

        for BOT in active_bots: # Move + Player icon write
            turn(BOT)
            if BOT == Bot_0:
                Bot_icon = Bot_0_icon
            elif BOT == Bot_1:
                Bot_icon = Bot_1_icon
            playerboard[BOT[0]][BOT[1]] = Bot_icon # BOT to playerboard Icon writer
        clear()

        # GUI
        print error_message
        print_board(playerboard)
        print "Bot-# = has", bot_0_score, "points"
        print "Bot-@ = has", bot_1_score, "points"
        time.sleep(float(bot_speed))


        for BOT in active_bots: # Make current posistion object icon + posistion count += 1
            playerboard[BOT[0]][BOT[1]] = object_board[BOT[0]][BOT[1]] # Make bots current posision == object
            memory_board[BOT[0]][BOT[1]] += 1 #Block usage counter (You have stepped on this square x times)

        break
    

raw_input("")
print_board(object_board)
menu()

# 330L AI battle bots. (Neater)