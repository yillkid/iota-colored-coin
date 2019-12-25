PATH_ACCOUNT = "outputs/"

def get_seed(username):
    f = open(PATH_ACCOUNT + username + "/seed.txt", "r")
    contents =f.read()
    f.close()

    return contents
