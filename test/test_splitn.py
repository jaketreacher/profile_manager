import pytest

from steamprof.steamhelper import splitn

	# splitn(value, n)

def test_raise_typeerror_value_not_string():
	with pytest.raises(TypeError):
		splitn(5, 2)

def test_raise_typeerror_n_not_int():
	with pytest.raises(TypeError):
		splitn('string', 'c')

@pytest.mark.parametrize('value, n', [
	('123', 2),
	('1234', 3),
	('12345', 6),
	('123456', 7),
])
def test_raise_valueerror_value_len_not_factor_of_n(value, n):
	with pytest.raises(ValueError):
		splitn(value, n)

@pytest.mark.parametrize('value, n, expected', [
	('1234', 2, ['12', '34']),
	('123456', 2, ['12', '34', '56']),
	('11110000', 4, ['1111', '0000']),
	('Jake is really good!', 5, ['Jake ', 'is re', 'ally ', 'good!'] ),
	('Practicing pytest.', 3, ['Pra', 'cti', 'cin', 'g p', 'yte', 'st.']),
])
def test_split_values_correctly(value, n, expected):
	assert splitn(value, n) == expected

@pytest.mark.parametrize('value, n', [
	('string', 0),
	('string', -1),
	('string', -2)
])
def test_raise_vaueerror_on_n_0_or_less(value, n):
	with pytest.raises(ValueError):
		splitn(value, n)
