from auto_proxy_manager import AutoProxyManager


def test_non_exist_attribute_should_raise():
    mgr = AutoProxyManager()

    try:
        mgr.non_exist_attr
    except AttributeError as e:
        assert 'Attribute `non_exist_attr` is not found.' in str(e)
    else:
        assert False, 'Accessing non-exist attribute is expected to throw an error'


def test_duplicate_registration_should_raise():
    mgr = AutoProxyManager()
    mgr._register('outlier', object())

    try:
        mgr._register('outlier', object())
    except ValueError as e:
        assert 'outlier already registered!' in str(e)
    else:
        assert False, 'Registering the same attribute again is expected to throw an error'


def test_valid_registration_should_be_accessible():
    mgr = AutoProxyManager()
    mgr._allowed_types = (dict,)
    mgr._register('dict', dict())

    try:
        mgr.dict[1] = 1
    except ValueError as e:
        assert 'outlier already registered!' in str(e)
    else:
        assert False, 'Registering the same attribute again is expected to throw an error'


def test_allowed_types_validation():
    mgr = AutoProxyManager()
    mgr._allowed_types = (int, float)

    try:
        mgr._register('str', 'str')
    except ValueError as e:
        assert 'Type `str` is not allowed. Accepted types: int, float' in str(e)
    else:
        assert False, 'Registering invalid type is expected to throw an error'


if __name__ == '__main__':
    test_non_exist_attribute_should_raise()
    test_duplicate_registration_should_raise()
    test_allowed_types_validation()
