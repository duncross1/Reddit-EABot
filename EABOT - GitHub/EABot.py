import praw
import config
import time
import os

def bot_login():#this code is executed upon the bots initial launch and is responsible for logging the bot into its reddit account
    print("logging in...") #prints a message to the console alerting the user that the bot is logging in
    r = praw.Reddit(username = config.username, #uses the details entered into the config file to login into the reddit account
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "EAMoneyBagsBOT v1.0")
    print("login finshed") #prints a message to the console alerting the user that the bot has finished logging in
    return r #returns the login session


def getSavedComments(): #this code is executed upon the bots initial launch and is responsible for loading the replied comment ID's in the comment ID's log (text document) into and array the bot uses to track comments already replied to, also creates the array if the comments log doesn't already exist
    if not os.path.isfile("commentIdsRepliedToLog.txt"):# checks to see if the replied comments ID log exists
        commentIdsRepliedTo = [] #creates the commentIdsRepliedTo array
    else: #if the replied comments ID log exists
        with open("commentIdsRepliedToLog.txt", "r") as bot: #open commentIdsRepliedToLog.txt
            commentIdsRepliedTo = bot.read() #reads comment ids from commentIdsRepliedToLog.txt into commentIdsRepliedTo array
            commentIdsRepliedTo = commentIdsRepliedTo.split("\n")#seperates the commentIdsRepliedTo entries into a new array entry at every new line

    return commentIdsRepliedTo #returns the commentIdsRepliedTo array


def run_bot(session, commentIdsRepliedTo): #this is the code executed when the bot runs after sleeping (or after logging in if this is the first cycle), this method makes use of the session and commentIdsRepliedTo parameters

    global minutesSlept #allows this method to make use of the minutesSlept global variable
    global totalRepliesThisSession #allows this method to make use of the totalRepliesThisSession global variable

    numberOfRepliesThisSearch = 0 #sets numberOfRepliesThisSearch to 0
    commentRepliedTo = 0 #sets commentRepliedTo to 0

    if minutesSlept > 9: #checks to see if the bot has been asleep for atleast 10 minutes
        print("Searching Comments...") #prints a message to the console alerting the user that the bot is searching for comments
    else: #if the bot has NOT been asleep for atleast 10 minutes
        print("Minutes till next search: " + str(10 - minutesSlept)) #prints a message to the console alerting the user as to how many minutes till the bot activates again
    for comment in session.subreddit('test+test3+StarWarsBattlefront+starwars+PrequelMemes').comments(limit=config.numberOfCommentsToSearch): #tells the bot to search through a number (amount specified in config file) of the newest comments on select subreddits

        if "sense of pride and accomplishment" in comment.body and comment.id not in commentIdsRepliedTo and not comment.author == session.user.me() and numberOfRepliesThisSearch < 1 and minutesSlept > 9: #checks to see if the bot finds a comment containing a string matching
                                                                                                                                                                                                                # the one specefied to search for that is also not a comment that has already been replied to or a comment by this bot
                                                                                                                                                                                                                # this line of code also checks to make sure the bot has not already replied to a comment this cycle (avoids reddit post limiting)
                                                                                                                                                                                                                # and that the bot has been asleep for 10 minutes
            print ("matching comment found, commentID: " + comment.id) #prints a message to the console alerting the user that the bot has found a matching comment, and shows the commentID of that comment
            numberOfRepliesThisSearch = numberOfRepliesThisSearch + 1  # increases numberOfRepliesThisSearch by 1
            comment.reply("The 💰 intent 💰 is 💰 to 💰 provide 💰 players 💰 with 💰 a 💰 sense 💰 of 💰" #tells the bot to reply to that comment with a specefied comment
                            " pride 💰 and 💰 accomplishment 💰 for 💰 unlocking 💰 different 💰 heroes. 💰"
                            " As 💰 for 💰 cost, 💰 we 💰 selected 💰 initial 💰 values 💰 based 💰 upon 💰 "
                            "data 💰 from 💰 the 💰 Open 💰 Beta 💰 and 💰 other 💰 adjustments 💰 made 💰 "
                            "to 💰 milestone 💰 rewards 💰 before 💰 launch. 💰 Among 💰 other 💰 things,"
                            " 💰 we're 💰 looking 💰 at 💰 average 💰 per-player 💰 credit 💰 earn 💰 rates "
                            "💰 on 💰 a 💰 daily 💰 basis, 💰 and 💰 we'll 💰 be 💰 making 💰 constant 💰 "
                            "adjustments 💰 to 💰 ensure 💰 that 💰 players 💰 have 💰 challenges 💰 that "
                            "💰 are 💰 compelling, 💰 rewarding, 💰 and 💰 of 💰 course 💰 attainable 💰 "
                            "via 💰 gameplay. We 💰 appreciate 💰 the 💰 candid 💰 feedback, 💰 and 💰 the"
                            " 💰 passion 💰 the 💰 community 💰 has 💰 put 💰 forth 💰 around 💰 the 💰 "
                            "current 💰 topics 💰 here 💰 on 💰 Reddit, 💰 our 💰 forums 💰 and 💰 across "
                            "💰 numerous 💰 social 💰 media 💰 outlets. Our 💰 team 💰 will 💰 continue 💰 "
                            "to 💰 make 💰 changes 💰 and 💰 monitor 💰 community 💰 feedback 💰 and 💰 "
                            "update 💰 everyone 💰 as 💰 soon 💰 and 💰 as 💰 often 💰 as 💰 we 💰 can. "
                            "💰 💰")

            commentRepliedTo = 1 #sets commentRepliedTo to 1, commentRepliedTo acts as a true or false statement

            totalRepliesThisSession = totalRepliesThisSession + 1 #increases totalRepliesThisSession by 1
            print ("Comment '" + comment.id + "' replied to")  #prints a message to the console alerting the user that the bot has replied to the comment, and shows the commentID of that comment

            commentIdsRepliedTo.append(comment.id) #adds that comment to an array of comments that have already been replied to
            with open("commentIdsRepliedToLog.txt", "a") as bot: #either opens or creates then open (depending on if it exists) a text document for storing comment ID's that have been replied to
                bot.write(comment.id + "\n") #writes the comment ID to the text document ensuring that it wont be replied to again on later passes


    if minutesSlept > 9:#checks to see if the bot has been asleep for atleast 10 minutes
        if commentRepliedTo == 1:#checks to see if commentRepliedTo is equal to 1 (1 =true, 0 = false)
            print("NOT replying to another comment till next search")#prints a message to the console alerting the user that the bot will not reply to another comment this cycle (as to avoid the reddit post limit)
        else: #if commentRepliedTo is equal to 0 (1 =true, 0 = false)
            print("NO matching comments found") #prints a message to the console alerting the user that the bot did not find a matching comment this cycle
        print("Total comments replied to this session: " + str(totalRepliesThisSession))#prints a message to the console telling the user how many comments the bot has replied to in total this session
        print("Bot sleeping for 10 minutes...")#prints a message to the console alerting the user that the bot is going to sleep for 10 minutes
        minutesSlept = 0#sets minutesSlept to 0


    time.sleep(121)#Cause the bot to sleep(pause/not run) for 2 minutes (and 1 second to be safe)
                    #  (the bot does multiple 2 minute sleep cycles instead of 1 10 minute sleep cycle to: (a)keep the user updated on how long is left till the bot runs again, (b)solve a problem where the reddit (PRAW) api would
                    # cause a crash if left idle long enough
    minutesSlept = minutesSlept + 2 #increases minutesSlept by 2




totalRepliesThisSession = 0 #Sets totalRepliesThisSession to equal 0
minutesSlept = 10 #Sets minutesSlept to equal 10


commentIdsRepliedTo = getSavedComments() #Runs the getSavedComments method, also Sets commentIdsRepliedTo to equal the return of the getSavedComments method
session = bot_login() #Runs the bot_login method, also Sets session to equal the return of the bot_login method
while True: #effectively an infinite loop
    run_bot(session, commentIdsRepliedTo) #Runs the run_bot method