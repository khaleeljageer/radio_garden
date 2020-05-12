import requests
import json
import subprocess
import constants
import credential

git_username = credential.USER_NAME
git_password = credential.ACCESS_TOKEN


git_clone = "git clone https://" + git_username +":" + git_password + "@github.com/khaleeljageer/RadioGarden.git radio_garden"

def push():
    print('Executing push')
    subprocess.call('git commit -am list_update', shell=True, cwd='radio_garden/')
    subprocess.call('git push origin master', shell=True, cwd='radio_garden/')
    return


def update_file(arg):
    file = open('radio_garden/radio_list.json', "w")
    file.write(arg)
    file.close
    print('File updated')
    return


def clone():
    try:
        subprocess.call('rm -rf radio_garden', shell=True)
    except:
        print('No such directory')
    subprocess.call(git_clone, shell=True)
    return

class UpdateGithub:
    def update_github(self, arg):
        clone()
        update_file(arg)
        push()
        return


if __name__ == "__main__":
    print("Try running radio_list.py first")
