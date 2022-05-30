



with open(r"klikacka/leaderboard.ini", 'a') as config:
    config.write(username + ":" + "0" +"\n")
with open(r"klikacka/leaderboard.ini", 'r+') as config:
    config.write("maxScore" + ":" + "583\n")
    config.seek(0)