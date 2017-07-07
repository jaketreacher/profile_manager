import binascii
import re
import time

class Shortcuts:
    """Handles all the games stored in shortcuts.vdf
    """ 
    def __init__(self, data=None):
        if not data:
            self.games = []
        else:
            games = re.findall('\x00([0-9].*?)\x00(.*?(?:\x08){2})', data)
            self.games = [Game(data) for idx, data in games]

    def __eq__(self, other):
        if type(other) is type(self):
            return other.__dict__ == self.__dict__
        return False

    def __repr__(self):
        return 'Shortcuts(%d)' % len(self.games)

    def __str__(self):
        return str(self.__dict__)


class Game:
    """A single game stored in shortcuts.vdf
    """
    def __init__(self, data=None):
        if not data:
            self.appname = ''
            self.exe = ''
            self.startdir = ''
            self.icon = ''
            self.shortcutpath = ''
            self.launchoptions = ''
            self.ishidden = False
            self.allowdesktopconfig = True
            self.openvr = ''
            self.lastplaytime = 0
            self.appid = Game.generate_appid(self.exe, self.appname)
            self.tags = []
        else:
            self.appname = Game.extract_string('AppName', data)
            self.exe = Game.extract_string('exe', data)
            self.startdir = Game.extract_string('StartDir', data)
            self.icon = Game.extract_string('icon', data)
            self.shortcutpath = Game.extract_string('ShortcutPath', data)
            self.launchoptions = Game.extract_string('LaunchOptions', data)
            self.ishidden = Game.extract_bool('IsHidden', data)
            self.allowdesktopconfig = Game.extract_bool('AllowDesktopConfig',
                data)
            self.openvr = Game.extract_bool('OpenVR', data)
            self.lastplaytime = Game.extract_timestamp(data)
            self.appid = Game.generate_appid(self.exe, self.appname)
            self.tags = Game.extract_tags(data)

    def extract_string(key, data):
        """Extract a string value

        Format:
            \x01(Key)\x00(string)\x00

        args:
            key(str): the key to match.
                Possible values: AppName, exe, StartDir, icon, ShortcutPath
            data(str): the data to search through
        returns:
            (str): the value matching the key. Can be ''
        """
        return re.search('\x01%s\x00(.*?)\x00' % key, data).group(1)

    def extract_bool(key, data):
        """Extract a boolean value

        Format:
            \x02(Key)\x00(\x00|\x01)\x00\x00\x00

        args:
            key(str): the key to match.
                Possible values: IsHidden, AllowDesktopConfig, OpenVR
            data(str): the data to search through

        return:
            (bool)
        """
        value = re.search('\x02%s\x00(\x00|\x01)(?:\x00){3}' % key,
                          data).group(1)
        return bool(ord(value))

    def extract_timestamp(data):
        """Extract the timestamp value

        Format:
            \x02LastPlayTime\x00(HH HH HH HH)
                where HH is any hex value
            
            Similiar to extract_bool, except we want all four end chars,
            and we also  want to convert it into a timestamp as it may
            require manipulation.

        args:
            data(str): the data to search through

        return:
            (int): timestamp, seconds since epoch
        """
        timestamp = re.search('\x02LastPlayTime\x00(.{4})\x00tags',
                              data).group(1)
        return Game.decode_timestamp(timestamp)

    def encode_timestamp(timestamp):
        """Convert the timestamp into the format used in shortcuts.vdf

        Example:
            timestamp:
                1496081616

            convert to binary, and split into octects:
                01011001 00101100 01100100 11010000

            reverse order:
                11010000 01100100 00101100 01011001

            join and convert to hex:
                d0642c59

            unhexlify - this is how Steam stores the timestamp
                \xd0d,Y

        args:
            timestamp(int): seconds since epoch

        returns:
            (str): Steam timestamp value
                (four char hex in reverse order)
        """
        timestamp = format(int(timestamp), '032b')
        timestamp = splitn(timestamp, 8)
        timestamp.reverse()
        timestamp = ''.join(timestamp)
        timestamp = format(int(timestamp, 2), '08x')
        timestamp = binascii.unhexlify(timestamp).decode('latin_1')
        return timestamp

    def decode_timestamp(timestamp):
        """Convert the timestamp from the shortcuts.vdf format into an int

        Example:
            timestamp:
                \xd0d,Y

            convert to hex and split:
                d0 64 2c 59

            reverse order and join:
                592c64d0

            convert to int:
                1496081616

        args:
            timestamp(str): the timestamp format used in shortcuts.vdf
                (four char hex in reverse order)

        returns:
            (int): seconds since epoch
        """
        timestamp = [format(ord(c), '02x') for c in timestamp]
        timestamp.reverse()
        timestamp = ''.join(timestamp)
        timestamp = int(timestamp, 16)
        return timestamp

    def extract_tags(data):
        """Extracts all tag values

        Format:
            \x00(number)\x00(tag)\x00

        args:
            data(str): the data to search through

        returns:
            list[str]: all tags found
        """
        taglist = taglist = re.findall('\x00tags\x00(.*?)(?:\x08){2}',
                                       data)[0]
        tags = re.findall('\x01(?:[0-9].*?)\x00(.*?)\x00', taglist)
        return tags

    def generate_appid(exe, appname):
        """Generate an appid

        This is what Steam does.

        The top half is a 32-bit CRC of the args
        The bottom half is 0x02000000 for whatever reason.

        args:
            exe(str): the exe path
            appname(str): the name of the app
        """
        key = exe + appname
        top_32 = binascii.crc32(key.encode('latin_1')) | 0x80000000
        full_64 = top_32 << 32 | 0x02000000
        return full_64

    def __eq__(self, other):
        if type(other) is type(self):
            return other.__dict__ == self.__dict__
        return False

    def __repr__(self):
        return 'Game(%s)' % self.appname

    def __str__(self):
        return str(self.__dict__)


def splitn(string, n):
    """Split a string every N segments
    
    example:
        splitn('123456', 2) => ['12', '34', '56']

    args:
        string (str): the string to split
        n (int): the size of each segment

    return:
        list[str]

    raises:
        TypeError:
            string is not str
            n is not int
        ValueError: 
            n <= 0
            string length not multiple of n
    """
    if not isinstance(string, str):
        raise TypeError('string must be str, not ' + type(n).__name__)

    if not isinstance(n, int):
        raise TypeError('n must be int, not ' + type(n).__name__)

    if n <= 0:
        raise ValueError('n must be greater than 0')

    if len(string) % n:
        raise ValueError('invalid string length (%d),'
                         ' must be multiple of %d'
                         % (len(string), n))
        
    return [string[i: i+n] for i in range(0, len(string), n)]
