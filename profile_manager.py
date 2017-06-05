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
        game: the exe for the game, can launch
        save: the save directory for the game
        profile: the profile directory
        user: the user specified in the arguments
        lock: the lock file - to ensure only one instance is running
    """
    def __init__(self, manager, settings, game, save, profile, user, lock):
        self.manager = manager
        self.settings = settings
        self.game = game
        self.save = save
        self.profile = profile
        self.user = user
        self.lock = lock


def get_files():
    """Prepares the files for easy use in the rest of the program

    returns:
        Files object
    """
    manager = Filepath(os.path.abspath(__file__))
    settings = find_settings(manager)
    print('Loading settings from: {}'.format(settings.basename))
    game, save, profile = load_settings(settings)
    user = find_user(profile)
    # Lock file will be game.exe.txt, in the same directory
    # as this program
    lock = Filepath(
            os.path.join(manager.dirname,
                         game.basename + '.txt')
            )
    kwargs = {'manager': manager,
              'settings': settings,
              'game': game,
              'save': save,
              'profile': profile,
              'user': user,
              'lock': lock}
    return Files(**kwargs)


def find_settings(manager):
    """Finds settings in sys.argv

    Finds the settings value provided in the command line
    If none specified, defaults to 'settings.txt'

    args:
        manager - the Filepath of this program. The settings
            will be placed in the same directory.

    raises:
        ValueError - manager must be a Filepath
    """
    if not isinstance(manager, Filepath):
        raise ValueError('manager must be of type Filepath')

    settings_value = extract_argv('-settings')
    if settings_value is not None:
        settings_path = os.path.join(manager.dirname, settings_value)
    else:
        settings_path = os.path.join(manager.dirname, 'settings.txt')
    
    return Filepath(settings_path)

def load_settings(settings):
    """Extract paths from the settings file and assigns them to variables

    Reads the settings file in the same directory as the program.
    If not found, it will create a template then exist.

    args:
        settings - the Filepath of the settings file

    raises:
        ValueError - settings must be a Filepath

    return:
        tuple(game,save,profile) of type Filepath
        game - where the exe is location
        save - where the game looks for saves
        profile - where the user is storing their profiles
    """
    if not isinstance(settings, Filepath):
        raise ValueError('settings must be of type Filepath')
    
    if os.path.exists(settings.path):
        values = {}
        with open(settings.path, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                args = line.split('=')
                values[args[0]] = args[1]

        game = Filepath(values['GAME'], True)
        save = Filepath(values['SAVE'])
        profile = Filepath(values['PROFILE'])
        return (game, save, profile)
    else:
        create_settings(settings)
        message = "Settings not found. Template created at {}".format(settings.path)   
        delay_exit(message)

def create_settings(settings):
    """Creates the settings file using a default template
    
    args:
        settings - the Filepath of the settings file

    raises:
        ValueError - settings must be a Filepath
    """
    if not isinstance(settings, Filepath):
        raise ValueError("settings must of of type Filepath")

    with open(settings.path, 'w') as file:
        template = ('SAVE=/absolute/path/to/save/folder\n'
                    'GAME=/absolute/path/to/game.exe\n'
                    'PROFILE=/absolute/path/to/profile/root/dir\n')
        file.write(template)

def find_user(profile):
    """Finds the user in sys.argv

    args:
        profile - the Filepath of where the profiles are stored

    raises:
        ValueError - profile must be a Filepath

    return:
        Filepath of the user
        If user not found, returns None
    """
    if not isinstance(profile, Filepath):
        raise ValueError('profile must be of type Filepath')

    user_value = extract_argv('-user')
    if user_value is not None:
        user_path = os.path.join(profile.path, user_value)
        return Filepath(user_path)

def extract_argv(key):
    """Extract the value from sys.argv correlating with key 

    Example:
        program -user <user> -settings <settings>
    
    Searches through sys.argv for key and gets the index.
    The next index is the value.
    
    args:
        key (str) - the key to search for

    return:
        if found: value - the value of the key
        if not found: None
    """
    try:
        index = sys.argv.index(key)
        index += 1
        value = sys.argv[index]
        return value
    except ValueError:
        pass
    except IndexError:
        pass

def delay_exit(message, duration=5):
    """Delays sys.exit with a fancy countdown

    Args:
        message (str): the message to print to the screen
        duration (int): the delay, in seconds
    """
    print(message)
    for remaining in range(duration, 0, -1):
        print('Quitting in {}...'.format(remaining), end='\r')
        time.sleep(1)
    sys.exit()

if __name__ == '__main__':

    files = get_files()

    # If files.user is not Filepath, that means a user could not be
    # extracted from the arguments
    if isinstance(files.user, Filepath):
        if not os.path.exists(files.user.path):
            delay_exit("User doesn't exist")
    else:
        delay_exit("User not specified")

    # Create a lock file to ensure only one instance is running.
    # If the file can't be removed, another instance of the manager
    # is still running, which likely means the game is still active.
    if os.path.exists(files.lock.path):
        try:
            os.remove(files.lock.path)
        except PermissionError:
            delay_exit("It appears this game is still active.")

    with open(files.lock.path, 'w'):
        # Check if current save folder is directory or link
        if os.path.isdir(files.save.path) and not os.path.islink(files.save.path):
            # Backup old files
            now = int(time.time())
            backup_dir = "{}_{}_backup".format(files.save.basename, now)
            backup_dir = os.path.join(files.save.dirname, backup_dir)

            os.rename(files.save.path, backup_dir)
            print("Backup current profiles to: {}".format(os.path.basename(backup_dir)))

        # If files.save.path is a link and it's currently pointing
        # to the same user folder, then there's no need to do anything
        swap_required = True
        if os.path.exists(files.save.path) and os.path.islink(files.save.path):
            if os.readlink(files.save.path) == files.user.path:
                print("Profile '{}' already configured".format(files.user.basename))
                swap_required = False

        # Previous test failed, so we need to make a link
        if swap_required:
            if os.path.exists(files.save.path):
                os.remove(files.save.path)
                print("Removed previous symbolic link")
            os.symlink(files.user.path, files.save.path)
            print("Swapped to profile '{}'".format(files.user.basename))
        
        print("Launching {}".format(files.game.basename))
        files.game.launch()

    os.remove(files.lock.path)