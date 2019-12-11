import os
import shutil
from cmd import Cmd
from subprocess import call

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

script_list = [
    'update_system',
    'example'
]


class MyPrompt(Cmd):

    prompt = 'ITsm> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Happy computing!")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_install(self, inp):
        global ROOT_DIR
        global script_list
        print('Very well, installing personal system management script suite')
        print(ROOT_DIR)
        # os.mkdir(ROOT_DIR + '/happy')
        home = os.path.expanduser("~")
        print(home)
        if os.path.exists(home + '/.bin'):
            print('Found binary directory for user.')
            source = ROOT_DIR + '/scripts/'
            dest = home + '/.bin/itsm'
            if os.path.exists(dest):
                print('Found ITsm directory from previous install')
            else:
                os.mkdir(dest)
            for script in script_list:
                file = source + script + '.sh'
                dest_file = dest + '/' + script
                print('Copying %s to %s' % (file, dest_file))
                shutil.copyfile(file, dest_file)
                print('File copied.')
                print('Making executable')
                call(['chmod', '+x', dest_file])
                print('Done!')


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