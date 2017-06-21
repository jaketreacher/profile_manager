# Profile Manager

## Synopsis

A basic program that provide a way to manage profiles in games that don't have this feature.

It works by creating a symbolic link at the location the game looks for save files and points to the specified save folder. The link changes location depending on the profile selected.

## Code Example

python3 profile_manager.py -user [user] -settings [settings]

The settings file requires the following:  
SAVE=/absolute/path/to/save/folder  
GAME=/absolute/path/to/game.exe  
PROFILE=/absolute/path/to/profile/root/dir  

A symbolic link is created at SAVE and will point to the specified -user folder in PROFILE.

The program will search for settings.txt by default, unless another option is specified by -settings.

## Motivation

I stream games from my computer to Nvidia Shield. As such, there is one computer with all the games, and some games, in particular the Witcher 3, don't have support for profiles. Because of this, all saves files are stored together and it's hard to determine which save belongs to which player.

Therefore, I sought to create the program to separate save files and make it easy to manage profiles.

## Installation

### Requirements
Python3 (if using source code)

### Non-Windows
Untested

### Windows
The best way is to add the profile manager to steam as a non-steam game. But first, it must be compiled. A pre-compiled version is provided in the dist/ directory.

If you want to compile it yourself, I used [PyInstaller](http://www.pyinstaller.org).

#### Steam
1. Add profile_manager.exe to steam as a non-steam game
2. Library -> Right-click profile_manager -> Properties
3. Set Launch Options: specify '-user [user] -settings [settings]'
4. (Optional) Add an icon so it's easy to distinguish

#### Example
I created a folder 'C:\Profile Manager' to store everything.
It contains the following:
* profile_manager.exe
* Profiles/
	* witcher3/
		* Jake/
		* Yasmin/
		* jake.png
		* yasmin.png
* witcher3.txt

witcher.txt contains:  
SAVE=C:\Users\Jake\Documents\The Witcher 3  
GAME=C:\Games\The Witcher 3 - Wild Hunt\bin\x64\witcher3.exe  
PROFILE=C:\Profile Manager\Profiles\witcher3  

I added profile_manager.exe to steam *twice*.  
Witcher 3 - Jake	| Launch Options: -user Jake -settings witcher3.txt  
Witcher 3 - Yasmin	| Launch Options: -user Yasmin -settings witcher3.txt  

## License

[MIT](https://github.com/jaketreacher/profile_manager/blob/master/LICENSE.md)