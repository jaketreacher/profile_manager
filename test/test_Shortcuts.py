import pytest

from steamprof.steamhelper import Shortcuts, Game

# data with one game, all default, never launched
data_simple = '\x00shortcuts\x00' \
    '\x000\x00' \
    '\x01AppName\x00Google Chrome\x00' \
    '\x01exe\x00"/Applications/Google Chrome.app"\x00' \
    '\x01StartDir\x00"/Applications/"\x00' \
    '\x01icon\x00\x00' \
    '\x01ShortcutPath\x00\x00' \
    '\x01LaunchOptions\x00\x00' \
    '\x02IsHidden\x00\x00\x00\x00\x00' \
    '\x02AllowDesktopConfig\x00\x01\x00\x00\x00' \
    '\x02OpenVR\x00\x00\x00\x00\x00' \
    '\x02LastPlayTime\x00\x00\x00\x00\x00' \
    '\x00tags\x00' \
    '\x08\x08' \
    '\x08\x08'

# data with two games, first same as data_simple, second with
# everything change (that's possible) and a LastPlayTime
data_complex = '\x00shortcuts\x00' \
    '\x000\x00' \
    '\x01AppName\x00Google Chrome\x00' \
    '\x01exe\x00"/Applications/Google Chrome.app"\x00' \
    '\x01StartDir\x00"/Applications/"\x00' \
    '\x01icon\x00\x00' \
    '\x01ShortcutPath\x00\x00' \
    '\x01LaunchOptions\x00\x00' \
    '\x02IsHidden\x00\x00\x00\x00\x00' \
    '\x02AllowDesktopConfig\x00\x01\x00\x00\x00' \
    '\x02OpenVR\x00\x00\x00\x00\x00' \
    '\x02LastPlayTime\x00\x00\x00\x00\x00' \
    '\x00tags\x00' \
    '\x08\x08' \
    '\x001\x00' \
    '\x01AppName\x00FaceTime\x00' \
    '\x01exe\x00"/Applications/FaceTime.app"\x00' \
    '\x01StartDir\x00"/Applications/"\x00' \
    '\x01icon\x00\x00' \
    '\x01ShortcutPath\x00\x00' \
    '\x01LaunchOptions\x00-launch LOL\x00' \
    '\x02IsHidden\x00\x00\x00\x00\x00' \
    '\x02AllowDesktopConfig\x00\x01\x00\x00\x00' \
    '\x02OpenVR\x00\x01\x00\x00\x00' \
    '\x02LastPlayTime\x00(\xfajY' \
    '\x00tags\x00' \
    '\x010\x00Video\x00' \
    '\x011\x00favorite\x00' \
    '\x08\x08' \
    '\x08\x08'

class TestReadShortcuts:
    @pytest.mark.parametrize('data, expected', [
        (data_simple, ['Google Chrome']),
        (data_complex, ['Google Chrome', 'FaceTime'])
    ])
    def test_read_appname_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.appname for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, ['"/Applications/Google Chrome.app"']),
        (data_complex, ['"/Applications/Google Chrome.app"',
                        '"/Applications/FaceTime.app"']),
    ])
    def test_read_exe_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.exe for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, ['"/Applications/"']),
        (data_complex, ['"/Applications/"', '"/Applications/"'])
    ])    
    def test_read_startdir_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.startdir for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, ['']),
        (data_complex, ['', ''])
    ])    
    def test_read_icon_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.icon for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, ['']),
        (data_complex, ['', ''])
    ])    
    def test_read_shortcutpath_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.shortcutpath for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, ['']),
        (data_complex, ['', '-launch LOL'])
    ])    
    def test_read_launchoptions_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.launchoptions for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, [False]),
        (data_complex, [False, False])
    ])    
    def test_read_ishidden_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.ishidden for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, [True]),
        (data_complex, [True, True])
    ])    
    def test_read_allowdesktopconfig_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.allowdesktopconfig for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, [False]),
        (data_complex, [False, True])
    ])    
    def test_read_openvr_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.openvr for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, [0]),
        (data_complex, [0, 1500183080])
    ])    
    def test_read_lastplaytime_correct(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.lastplaytime for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, [[]]),
        (data_complex, [[], ['Video', 'favorite']])
    ])    
    def test_read_tags_correctself(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.tags for game in shortcut.games]
        assert result == expected

    @pytest.mark.parametrize('data, expected', [
        (data_simple, [11790138724560404480]),
        (data_complex, [11790138724560404480, 15620899018836541440])
    ])    
    def test_read_appid_correctself(self, data, expected):
        shortcut = Shortcuts(data)

        result = [game.appid for game in shortcut.games]
        assert result == expected

class TestWriteShortcuts:
    pass

@pytest.mark.parametrize('timestamp, expected', [
    ('\xcaz\xe85', 904428234),
    (';\xe9\xa56', 916842811),
    ('\xc38_7', 928987331),
    ('Qw\x038', 939751249),
    ('\x15\x1b|8', 947657493),
    ('\x9c*\xc78', 952576668),
    ('\xc6P\xcc9', 969691334),
    ('\nu\x12:', 974288138),
    ('\x9c\x91w:', 980914588),
    ('\xf2\x9f_;', 996122610),
    ('\xe4A\xf0;', 1005601252),
    ('\xc9\xedW<', 1012395465),
    ('\\*B=', 1027746396),
    ('\xf2~u=', 1031110386),
    ('\xa0\xb5G>', 1044886944),
    ('\xcd\xa5\x96>', 1050060237),
    ('\x96:\x97?', 1066875542),
    ('^7\x00@', 1073755998),
    ('\x83\xc9u@', 1081461123),
    ('\x1d\x87`A', 1096845085),
    ('\xd5J$B', 1109674709),
    ('\xc9\x84KB', 1112245449),
    ('$\xaa\xcbB', 1120643620),
    (']\xaf`C', 1130409821),
    ('\xed\xb1\x86D', 1149678061),
    ('\xe8\xac\x1fE', 1159703784),
    ("a'}E", 1165829985),
    ('ErKF', 1179349573),
    ('\x92g\xedF', 1189963666),
    ('\xd2\xf5\x13G', 1192490450),
    ('Y\xf5\xe9G', 1206515033),
    ('\x8cK\xa1H', 1218530188),
    ('6i\xcaH', 1221224758),
    ('\xea\xab\xcbI', 1238084586),
    ('\xf1\x97\tJ', 1242142705),
    ('[m\xd3J', 1255370075),
    ('A\x00sK', 1265827905),
    ('\xaf,\xfcK', 1274817711),
    (')&\x87L', 1283925545),
    ("'\xf6\xe9L", 1290401319),
    ('}\x8e\xe4M', 1306824317),
    ('\x06\xe7lN', 1315759878),
    ('\x9cv\xc0N', 1321236124),
    ('\x12\xd4\xceO', 1338954770),
    ('\xb9\xc65P', 1345701561),
    ('\xaf\xb3\xd7P', 1356313519),
    ('\xfc\xefmQ', 1366159356),
    ('\xd2\xec\x03R', 1375988946),
    ('\xe4A\x9dR', 1386037732),
    ('\x17\x15:S', 1396315415),
    ('\x03(\xc9S', 1405691907),
    ('\x13wVT', 1414952723),
    ('n@\xedT', 1424834670),
    ('o\x80gU', 1432846447),
    ('[\xe5\xf6U', 1442243931),
    ('EP\x02W', 1459769413),
    ('\xcd\xfb\x11W', 1460796365),
    ('\x95\x03\xaeW', 1471021973),
    ('\xc8\xfc\x84X', 1485110472),
    ('\xdao\xf7X', 1492611034),
    ('\x9aI\x8fY', 1502562714)
])
def test_decode_timestamp(timestamp, expected):
    assert Game.decode_timestamp(timestamp) == expected

@pytest.mark.parametrize('timestamp, expected', [
    (904428234, '\xcaz\xe85'),
    (916842811, ';\xe9\xa56'),
    (928987331, '\xc38_7'),
    (939751249, 'Qw\x038'),
    (947657493, '\x15\x1b|8'),
    (952576668, '\x9c*\xc78'),
    (969691334, '\xc6P\xcc9'),
    (974288138, '\nu\x12:'),
    (980914588, '\x9c\x91w:'),
    (996122610, '\xf2\x9f_;'),
    (1005601252, '\xe4A\xf0;'),
    (1012395465, '\xc9\xedW<'),
    (1027746396, '\\*B='),
    (1031110386, '\xf2~u='),
    (1044886944, '\xa0\xb5G>'),
    (1050060237, '\xcd\xa5\x96>'),
    (1066875542, '\x96:\x97?'),
    (1073755998, '^7\x00@'),
    (1081461123, '\x83\xc9u@'),
    (1096845085, '\x1d\x87`A'),
    (1109674709, '\xd5J$B'),
    (1112245449, '\xc9\x84KB'),
    (1120643620, '$\xaa\xcbB'),
    (1130409821, ']\xaf`C'),
    (1149678061, '\xed\xb1\x86D'),
    (1159703784, '\xe8\xac\x1fE'),
    (1165829985, "a'}E"),
    (1179349573, 'ErKF'),
    (1189963666, '\x92g\xedF'),
    (1192490450, '\xd2\xf5\x13G'),
    (1206515033, 'Y\xf5\xe9G'),
    (1218530188, '\x8cK\xa1H'),
    (1221224758, '6i\xcaH'),
    (1238084586, '\xea\xab\xcbI'),
    (1242142705, '\xf1\x97\tJ'),
    (1255370075, '[m\xd3J'),
    (1265827905, 'A\x00sK'),
    (1274817711, '\xaf,\xfcK'),
    (1283925545, ')&\x87L'),
    (1290401319, "'\xf6\xe9L"),
    (1306824317, '}\x8e\xe4M'),
    (1315759878, '\x06\xe7lN'),
    (1321236124, '\x9cv\xc0N'),
    (1338954770, '\x12\xd4\xceO'),
    (1345701561, '\xb9\xc65P'),
    (1356313519, '\xaf\xb3\xd7P'),
    (1366159356, '\xfc\xefmQ'),
    (1375988946, '\xd2\xec\x03R'),
    (1386037732, '\xe4A\x9dR'),
    (1396315415, '\x17\x15:S'),
    (1405691907, '\x03(\xc9S'),
    (1414952723, '\x13wVT'),
    (1424834670, 'n@\xedT'),
    (1432846447, 'o\x80gU'),
    (1442243931, '[\xe5\xf6U'),
    (1459769413, 'EP\x02W'),
    (1460796365, '\xcd\xfb\x11W'),
    (1471021973, '\x95\x03\xaeW'),
    (1485110472, '\xc8\xfc\x84X'),
    (1492611034, '\xdao\xf7X'),
    (1502562714, '\x9aI\x8fY')
])
def test_encode_timestamp(timestamp, expected):
    assert Game.encode_timestamp(timestamp) == expected