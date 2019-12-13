# !/usr/bin/python3
from github import Github
import getpass
import sys
import keyring
import requests
import os
from tqdm import tqdm


# A function to be used to confirm action with the user
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Service ID for the keyring
service_id = 'it_github'

user = input('What is your Github username? ')

password = keyring.get_password(service_id, user)

# Set up empty lists to be populated while program
# is running.

url_list = []

valid_urls = []

invalid_urls = []

already_present = []

# If there's not already a password in the keyring
# for the given username, then ask the user for
# the Github password and ask if it should be stored
if password is None:
    password = getpass.getpass('Github password? ')
    if query_yes_no('Should I store your password?', default='yes'):
        keyring.set_password(service_id, user, password)

# Create an authed Github object to fetch repos
gh = Github(user, password)

# Iterate through user's repositories check the
# current working directory for the presence of
# directories that match the repository name
#
# If a match is found, the program will not 
# concatenate a URL for the repo as there's
# no sense in doing so
for repo in gh.get_user().get_repos():
    if os.path.isdir(repo.name):
        already_present.append(repo.name)
    else:
        print(repo.name)
        url = 'https://%s:%s@github.com/%s/%s.git' % (user, password, user, repo.name)
        url_list.append(url)
        
        
if (len(url_list) == 0):
    print('%s does not have any remote repositories that are not missing from this system' % user)
    if (len(already_present) >= 1):
        print('(%s already present)'% str(len(already_present)))
    else:
        pass
              
              
elif len(url_list) == 1:
    print('%s may have one repository missing from this system. (not cloned)' % user)
    if (len(already_present) >= 1):
        print('(%s already present)' % str(len(already_present)))
              
    print('Following up')
    
    
else:
    print('Found %s possible repositories that are not present on this system.' % str(len(url_list)))
    if (len(already_present) >= 1):
        print('(%s already present)' % str(len(already_present)))


p_bar = tqdm(url_list)

for url_test in p_bar:
    p_bar.set_description('Testing ...%s...' % url_test.split('@github.com/')[1])
    try:
        req = requests.get(url_test)
        if req.status_code == 200:
            p_bar.set_description('Found %s!' % url_test.split('@github.com/')[1])
            valid_urls.append(url_test)
        else:
            invalid_urls.append(url_test)

    except:

        print('Does not exist!')

print()

if len(valid_urls) == 0:
    print('All valid repos were found locally')
else:
    print('Found %s out of %s valid URLs' % (len(valid_urls), len(url_list)))
    if query_yes_no('Would you like me to clone all valid repos? ', default='yes'):
        for url in valid_urls:
            safe_name = url.split('@github.com/%s/' % user)[1]
            print('Cloning %s' % safe_name)
            os.system('git clone %s' % url)
            print('Cloned %s' % safe_name)

 
