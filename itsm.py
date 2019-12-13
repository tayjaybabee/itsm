import os
import shutil
import inquirer
from cmd import Cmd
from subprocess import call
from tqdm import trange, tqdm

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

script_list = [
    'update_system',
    'example'
]


class MyPrompt(Cmd):

    prompt = 'ITsm> '
    intro = "Welcome! Type ? (or help) to list commands"
    
    
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

    

    def do_exit(self, inp):
        print("Happy computing!")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_install(self, inp):
        global ROOT_DIR
        global script_list
        print('Very well, installing personal system management script suite')
        home = os.path.expanduser("~")
        p_bar = tqdm(script_list)
        if os.path.exists(home + '/.bin'):
            print('Found binary directory for user.')
            source = ROOT_DIR + '/scripts/'
            dest = home + '/.bin/itsm'
            if os.path.exists(dest):
                print('Found ITsm directory from previous install')
            else:
                os.mkdir(dest)
            for script in p_bar:
                file = source + script + '.sh'
                dest_file = dest + '/' + script
                p_bar.set_description('Copying %s to %s' % (file, dest_file))
                shutil.copyfile(file, dest_file)
                p_bar.set_description('File copied')
                p_bar.set_description('Making %s executable...' % dest_file)
                call(['chmod', '+x', dest_file])
        else:



    def do_uninstall(self, inp):
        user_dir = os.path.expanduser("~")
        user_bin = user_dir + '/.bin'
        target_dir = user_bin + '/itsm'
        if os.path.exists(user_bin):
            if os.path.exists(target_dir):
                print("Removing %s" % target_dir)
                shutil.rmtree(target_dir)
                print("Removed %s" % target_dir)
            else:
                print("There is no install in the designated directory")
        else:
            print("There's no .bin directory in %s" % user_dir)


    def help_install(self):
        print('Installs personal system management script suite')


    def help_uninstall(self):
        print('Uninstalls personal system management script suite')


    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    MyPrompt().cmdloop()
