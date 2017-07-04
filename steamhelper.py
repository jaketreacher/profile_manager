import binascii
import re
import time
import pdb

def splitn(string, n):
	if not isinstance(string, str):
		raise TypeError('string must be str, not ' + type(n).__name__)
	if not isinstance(n, int):
		raise TypeError('n must be int, not ' + type(n).__name__)
	if len(string) % n:
		raise ValueError('invalid string length (%d), must be multiple of %d' % (len(string), n))
	return [string[i: i+n] for i in range(0, len(string), n)]

class Game:
	def __init__(self):
		pass

	def __init__(self, data):
		self.data = data

		self.appname = self.get_string('AppName')
		self.exe = self.get_string('exe')
		self.startdir = self.get_string('StartDir')
		self.icon = self.get_string('icon')
		self.shortcutpath = self.get_string('ShortcutPath')
		self.ishidden = self.get_bool('IsHidden')
		self.allowdesktopconfig = self.get_bool('AllowDesktopConfig')
		self.openvr = self.get_bool('OpenVR')
		self.lastplaytime = self.get_timestamp()
		self.appid = self.get_appid()
		
		taglist = re.findall('\\x00tags\\x00(.*?)(?:\\x08){2}', data)[0]
		self.tags = re.findall('\\x01(?:[0-9].*?)\\x00(.*?)\\x00', taglist)

	def get_string(self, key):
		return re.search('\\x01%s\\x00(.*?)\\x00' % key, self.data).group(1)

	def get_bool(self, key):
		value = re.search('\\x02%s\\x00(\\x00|\\x01)(?:\\x00){3}' % key, self.data).group(1)
		return bool(ord(value))

	def get_timestamp(self):
		timestamp = re.search('\\x02LastPlayTime\\x00(.*?)\\x00tags', self.data).group(1)
		return Game.timestamp_decode(timestamp)

	def timestamp_encode(timestamp):
		timestamp = format(int(timestamp), '032b')
		timestamp = splitn(timestamp, 8)
		timestamp.reverse()
		timestamp = ''.join(timestamp)
		timestamp = format(int(timestamp, 2), '08x')
		timestamp = binascii.unhexlify(timestamp).decode('latin_1')
		return timestamp

	def timestamp_decode(timestamp):
		timestamp = [format(ord(c), '02x') for c in timestamp]
		timestamp.reverse()
		timestamp = ''.join(timestamp)
		timestamp = int(timestamp, 16)
		return timestamp

	def get_appid(self):
		key = self.exe + self.appname
		top_32 = binascii.crc32(key.encode('latin_1')) | 0x80000000
		full_64 = top_32 << 32 | 0x02000000
		return full_64

	def __str__(self):
		return self.appname

class Shortcuts:
	def __init__(self, data):
		games = re.findall('\\x00([0-9].*?)\\x00(.*)(?:\\x08){2}', data)
		self.games = [Game(data) for idx, data in games]

if __name__ == '__main__':
	data = b'\x00shortcuts\x00\x000\x00\x01AppName\x00Google Chrome\x00\x01exe\x00"/Applications/Google Chrome.app"\x00\x01StartDir\x00"/Applications/"\x00\x01icon\x00\x00\x01ShortcutPath\x00\x00\x01LaunchOptions\x00\x00\x02IsHidden\x00\x00\x00\x00\x00\x02AllowDesktopConfig\x00\x01\x00\x00\x00\x02OpenVR\x00\x00\x00\x00\x00\x02LastPlayTime\x00(\xfajY\x00tags\x00\x010\x00favorite\x00\x011\x00testcat\x00\x08\x08\x08\x08'

	shortcuts = Shortcuts(data.decode('latin_1'))
	pdb.set_trace()

























