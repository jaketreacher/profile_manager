#!/usr/bin/python3

import os
import sys
import time

class Filepath:
    """A wrapper to easily grab filepath information

    Args:
        path (str): a path to the file
        canLaunch (bool, optional): specify if the
            file should be allowed to launch

    Attributes:
        path (str): the path to th file
        basename (str): the file name
        dirname (str): the directory of the file
        canLaunch (bool): specifies whether the
            file should be allowed to launch.
    """
    def __init__(self, path, canLaunch = False):
        self.path = os.path.dirname(os.path.join(path, ''))
        self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)
        self.canLaunch = canLaunch

    def launch(self):
        """Launch the program

        Unable to launch the full string from with just
        os.system, therefore it was necessary to
        os.chdir to the dirname and os.system on the
        basename of the file.
        """
        if self.canLaunch:
            os.chdir(self.dirname)
            os.system(self.basename)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Filepath({})".format(self.path)


class Files:
    """A wrapper for easily managing the various files.

    Attributes:
        manager: this program
        settings: the settings file
        lock: the lock file - to ensure only one instance is running

        __load_settings:
        game: the exe for the game, can launch
        save: the save directory for the game
        profile: the profile directory

        __extract_user:
        user: the user specified in the arguments
    """
    def __init__(self):
        self.manager = Filepath(os.path.abspath(__file__))
        self.settings = Filepath(
            os.path.join(self.manager.dirname, 'settings.txt')
            )
        self.lock = Filepath(
            os.path.join(self.manager.dirname, 'lock.xyz')
            )
        self.__load_settings()
        self.__extract_user()
    
    def __load_settings(self):
        """Extract paths from settings.txt and assigns them to variables

        Reads the settings.txt file in the same directory as the program.
        If not found, it will create a template then exist.
        """
        if os.path.exists(self.settings.path):
            settings = {}
            with open(self.settings.path, 'r') as file:
                for line in file:
                    line = line.replace('\n', '')
                    args = line.split('=')
                    settings[args[0]] = args[1]

            self.game = Filepath(settings['GAME'], True)
            self.save = Filepath(settings['SAVE'])
            self.profile = Filepath(settings['PROFILE'])
        else:
            self.__create_settings()
            print("Settings not found. Template created at {}".format(self.settings.path))
            sys.exit()

    def __create_settings(self):
        with open(self.settings.path, 'w') as file:
            template = ('SAVE=/absolute/path/to/save/folder\n'
                        'GAME=/absolute/path/to/game.exe\n'
                        'PROFILE=/absolute/path/to/profile/root/dir\n')
            file.write(template)
    
    def __extract_user(self):
        """Set the user based on command line arguments

        Example:
            program -user <user>
        
        Searches through sys.argv for '-user' and gets the index.
        The next index is the user.

        If no user specified, it is set to None.
        """
        try:
            index = sys.argv.index('-user')
            index += 1
            name = sys.argv[index]
            user_path = os.path.join(self.profile.path, name)
            self.user = Filepath(user_path)
        except ValueError:
            self.user = None
        except IndexError:
            self.user = None


if __name__ == '__main__':
    files = Files()

    # If files.user is not Filepath, that means a user could not be
    # extracted from the arguments
    if isinstance(files.user, Filepath):
        if not os.path.exists(files.user.path):
            print("User doesn't exist")
            sys.exit()
    else:
        print("User not specified")
        sys.exit()

    # Create a lock file to ensure only one instance is running
    if os.path.exists(files.lock.path):
        try:
            os.remove(files.lock.path)
        except PermissionError:
            print("It appears the game is still active.")
            sys.exit()

    with open(files.lock.path, 'w') as lockx:
        # Check if current save folder is directory or link
        if os.path.isdir(files.save.path) and not os.path.islink(files.save.path):
            # Backup old files
            now = int(time.time())
            backup_dir = "{}_{}_backup".format(files.save.basename, now)
            backup_dir = os.path.join(files.save.dirname, backup_dir)

            os.rename(files.save.path, backup_dir)
            print("Backup current profiles to: {}".format(os.path.basename(backup_dir)))

        if os.path.islink(files.save.path):
            os.remove(files.save.path)
            print("Removed previous save link")

        # Create Link
        os.symlink(files.user.path, files.save.path)
        print("Swapped to profile '{}'".format(files.user.basename))

        print("Launching {}".format(files.game.basename))
        files.game.launch()
    
    os.remove(files.lock.path)