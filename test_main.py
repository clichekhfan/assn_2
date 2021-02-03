# pylint: disable=C0114 (missing-module-docstring)
# pylint: disable=C0116 (missing-function-docstring)
# pylint: disable=W0621 (redefined-outer-name)
# pylint: disable=R0903 (too-few-public-methods)
# pylint: disable=E0401 (unused-import)
# pylint: disable=W0611 (line-too-long)
# pylint: disable=C0301 (line-too-long)
# pylint: disable=C0302 (too-many-lines)
# pylint: disable=C0103 (invalid-name)


import os
from unittest.mock import patch
from unittest.mock import mock_open
import copy
import pytest
import pysnooper
from loguru import logger
import main
import users
import user_status
import menu  # import last, menu contains logger sink


# fixtures


@pytest.fixture
def tolby():
    user_id = 'Cool_kid187'
    email = 'mommasboy2001@gmail.com'
    user_name = 'Tolby'
    user_last_name = 'Bryant'
    params = [user_id, email, user_name, user_last_name]

    tolby = users.Users(*params)
    return tolby


@pytest.fixture
def eve():
    line1 = ['evmiles97', 'eve.miles@uw.edu', 'Eve', 'Miles']
    eve = users.Users(*line1)

    return eve


@pytest.fixture
def dave():
    line2 = ['dave03', 'david.yuen@gmail.com', 'David', 'Yuen']
    dave = users.Users(*line2)

    return dave


@pytest.fixture
def collection():
    collection = users.UserCollection()

    return collection


@pytest.fixture()
def database(eve, dave, tolby):
    # database = {user_id: user_obj}
    database = {'evmiles97': eve,
                'dave03': dave,
                'Cool_kid187': tolby,
                }

    return database


@pytest.fixture
def impeach():
    status_id = 'XKPiC6*iW!H3#6'
    user_id = 'Hardline_Dem173'
    status_text = 'Impeach Trump!'
    params = [status_id, user_id, status_text]

    impeach = user_status.UserStatus(*params)

    return impeach


@pytest.fixture
def stolen():
    status_id = 'RbLr8!yCs*3DSC'
    user_id = 'Hardline_GOP173'
    status_text = 'The election was stolen from Trump!'
    params = [status_id, user_id, status_text]

    status = user_status.UserStatus(*params)

    return status


@pytest.fixture
def flat():
    status_id = 'G5Yz%#kTda&TFt'
    user_id = 'The_Real_Bill_Nye'
    status_text = 'The earth is flat!'
    params = [status_id, user_id, status_text]

    status = user_status.UserStatus(*params)

    return status


@pytest.fixture()
def status_database(impeach, stolen, flat):
    # database = {status_id: status_obj}
    database = {'XKPiC6*iW!H3#6': impeach,
                'RbLr8!yCs*3DSC': stolen,
                'G5Yz%#kTda&TFt': flat,
                }

    return database


@pytest.fixture
def status_collection():
    collection = user_status.UserStatusCollection()

    return collection


@pytest.fixture()
def csv_database(eve, dave):
    # database = {user_id: user_obj}
    database = {'evmiles97': eve,
                'dave03': dave
                }

    return database


@pytest.fixture
def csv_collection(csv_database):
    collection = users.UserCollection()

    collection.database = csv_database

    return collection


@pytest.fixture
def filename():
    filename = 'accounts.csv'

    return filename


@pytest.fixture
def temp_file():
    # this function will sometimes fail to create test.csv if the logs directory does not already exist
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')

        filename = os.path.join('logs', 'test.csv')
        logger.debug(filename)

        with open(filename, 'w'):
            pass
    except Exception as e:
        logger.critical('ERROR: ', e)
        raise e

    yield filename
    os.remove(filename)


# user tests


def test_users_init(tolby):
    assert tolby.email == 'mommasboy2001@gmail.com'


def test_user_collection_init(collection):
    assert collection.database == {}


def test_user_collection_add_user(collection, database):
    collection.database = database
    new_user = ['Big****123', 'AElrick@BTISolutions.com', 'My', 'Secret']
    assert collection.add_user(*new_user) is True


def test_user_collection_add_user_reject_existing(collection, database):
    collection.database = database
    line1 = ['evmiles97', 'eve.miles@uw.edu', 'Eve', 'Miles']
    assert collection.add_user(*line1) is False


def test_user_collection_add_user_database_updated(collection, database):
    collection.database = database
    initial_database_length = len(database)
    new_user = ['Big****123', 'AElrick@BTISolutions.com', 'My', 'Secret']
    collection.add_user(*new_user)
    assert collection.database['Big****123']
    assert len(database) > initial_database_length


def test_user_collection_modify_user_reject_not_existing(collection, database):
    collection.database = database
    line1 = ['ClicheKHFan', 'eve.miles@uw.edu', 'Eve', 'Miles']
    result = collection.modify_user(*line1)
    assert result is False


def test_user_collection_modify_user_updated_fields(collection, database):
    collection.database = database
    new_info = ['evmiles97', 'AElrick@BTISolutions.com', 'My', 'Secret']
    result = collection.modify_user(*new_info)
    assert collection.database['evmiles97'].email == 'AElrick@BTISolutions.com'
    assert collection.database['evmiles97'].user_name == 'My'
    assert collection.database['evmiles97'].user_last_name == 'Secret'
    assert result is True


def test_user_collection_delete_user_reject_not_existing(collection, database):
    collection.database = database
    result = collection.delete_user('ClicheKHFan')
    assert result is False


def test_user_collection_delete_user(collection, database):
    collection.database = database
    result = collection.delete_user('evmiles97')
    with pytest.raises(KeyError):
        save = collection.database['evmiles97']
        assert save is None
    assert result is True


def test_user_collection_search_user(collection, database):
    collection.database = database
    result = collection.search_user('evmiles97')
    assert result.user_id == 'evmiles97'


def test_user_collection_search_user_not_existing(collection, database):
    collection.database = database
    result = collection.search_user('ClicheKHFan')
    assert result.user_id is None


# user status tests


def test_user_status_init(impeach):
    assert impeach.status_id == 'XKPiC6*iW!H3#6'


def test_status_collection_init(status_collection):
    assert status_collection.database == {}


def test_userstatuscollection_add_status_reject_existing(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'
    user_id = 'Hardline_Dem173'
    status_text = 'Impeach Trump!'
    params = [status_id, user_id, status_text]

    assert status_collection.add_status(*params) is False


def test_userstatuscollection_add_status_update_database(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'
    user_id = 'Faithless_Floridian'
    status_text = 'God is dead!'
    params = [status_id, user_id, status_text]

    initial_database_length = len(status_database)
    result = status_collection.add_status(*params)

    assert len(status_database) > initial_database_length
    assert status_collection.database['byg8L^qJDjAkR6']
    assert result is True


def test_userstatuscollection_modify_status_reject_not_existing(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'
    user_id = 'Faithless_Floridian'
    status_text = 'God is dead!'
    params = [status_id, user_id, status_text]

    result = status_collection.modify_status(*params)

    assert result is False


def test_userstatuscollection_modify_status_update_database(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'
    user_id = 'Faithless_Floridian'
    status_text = 'God is dead!'
    params = [status_id, user_id, status_text]

    initial_database_length = len(status_database)
    result = status_collection.modify_status(*params)
    nietzsche = status_collection.database['XKPiC6*iW!H3#6'].status_text

    assert len(status_database) == initial_database_length
    assert nietzsche == 'God is dead!'
    assert result is True


def test_userstatuscollection_delete_status_reject_not_existing(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'

    result = status_collection.delete_status(status_id)

    assert result is False


def test_userstatuscollection_delete_status_update_database(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'

    initial_database_length = len(status_database)
    result = status_collection.delete_status(status_id)

    assert len(status_database) < initial_database_length
    assert result is True


def test_userstatuscollection_search_status_reject_not_existing(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'byg8L^qJDjAkR6'

    result = status_collection.search_status(status_id)

    assert result.status_id is None


def test_userstatuscollection_search_status_return_status(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'

    initial_database_length = len(status_database)
    result = status_collection.search_status(status_id)

    assert isinstance(result, user_status.UserStatus)
    assert len(status_database) == initial_database_length


# test main


def test_init_user_collection():
    collection = main.init_user_collection()

    assert collection.database == {}


def test_init_status_collection():
    collection = main.init_status_collection()

    assert collection.database == {}


def test_load_users_false(collection):
    result = main.load_users('missing_fields.csv', collection)

    assert result is False


def test_load_users_true(filename, collection):
    result = main.load_users(filename, collection)

    assert result is True


def test_load_users_ignore_existing(filename, csv_collection):
    main.load_users(filename, csv_collection)
    loaded_users = []
    for key in csv_collection.database:
        loaded_users.append(key)

    for item in loaded_users:
        assert loaded_users.count(item) == 1
    assert len(loaded_users) == 3


def test_save_users_false(collection):
    filename = ' C:by.pyg8 : L^qJ/D-jA.kR6'
    result = main.save_users(filename, collection)

    assert result is False


def test_save_users_true(temp_file, collection):
    result = main.save_users(temp_file, collection)

    assert result is True


def test_save_users_existing_file(temp_file, csv_collection):
    main.save_users(temp_file, csv_collection)

    with open(temp_file, 'r') as file:
        lines = file.readlines()

    ref_lines = ['USER_ID,EMAIL,NAME,LASTNAME\n',
                 'evmiles97,eve.miles@uw.edu,Eve,Miles\n',
                 'dave03,david.yuen@gmail.com,David,Yuen']

    comparison = lines == ref_lines
    print('lines:')
    print(lines)
    print('ref_lines:')
    print(ref_lines)

    assert comparison


def test_load_status_updates_false(status_collection, status_database):
    filename = 'missing_fields_status.csv'
    status_collection.database = status_database

    result = main.load_status_updates(filename, status_collection)

    assert result is False


def test_load_status_updates_true(status_collection, status_database):
    status_collection.database = status_database

    file = '''STATUS_ID,USER_ID,STATUS_TEXT
evmiles97_00001,evmiles97,"Code is finally compiling"
dave03_00001,dave03,"Sunny in Seattle this morning"
evmiles97_00002,evmiles97,"Perfect weather for a hike"
ted_00002,evmiles97,"Perfect weather for a hike"
ted_moop,ted,"Perfect weather for a hike"'''

    with patch('builtins.open', mock_open(read_data=file)) as mock_file:
        result = main.load_status_updates(mock_file, status_collection)

    assert result is True


def test_load_status_updates_not_exists(status_collection):
    filename = 'status_updates.csv'
    old_database = copy.copy(status_collection.database)

    result = main.load_status_updates(filename, status_collection)

    assert result is True
    assert status_collection.database != old_database


def test_save_status_updates_false(status_collection):
    filename = ' C:by.pyg8 : L^qJ/D-jA.kR6'

    result = main.save_status_updates(filename, status_collection)

    assert result is False


def test_save_status_updates_true(temp_file, status_collection, status_database):
    status_collection.database = status_database

    result = main.save_status_updates(temp_file, status_collection)

    assert result is True


def test_save_status_updates_not_exists(temp_file, status_collection):
    main.save_status_updates(temp_file, status_collection)

    with open(temp_file, 'r') as file:
        text = file.read()

    assert text != ''


def test_add_user_false(tolby, collection, database):
    collection.database = database

    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.add_user(*params)

    assert result is False


def test_add_user_true(tolby, collection):
    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.add_user(*params)

    assert result is True


def test_update_user_false(tolby, collection):
    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.update_user(*params)

    assert result is False


def test_update_user_true(tolby, collection, database):
    collection.database = database

    user_id = tolby.user_id
    email = tolby.email
    user_name = tolby.user_name
    user_last_name = tolby.user_last_name
    params = (user_id, email, user_name, user_last_name, collection)

    result = main.update_user(*params)

    assert result is True


def test_delete_user_false(collection):
    user_id = 'Cool_kid187'

    result = main.delete_user(user_id, collection)

    assert result is False


def test_delete_user_true(collection, database):
    collection.database = database

    user_id = 'Cool_kid187'

    result = main.delete_user(user_id, collection)

    assert result is True


def test_search_user(collection, database):
    collection.database = database

    user_id = 'Cool_kid187'

    result = main.search_user(user_id, collection)

    assert result.user_id == 'Cool_kid187'

    user_id = 'ClicheKHFan'

    result = main.search_user(user_id, collection)

    assert result is None


def test_add_status_false(stolen, status_collection, status_database):
    status_collection.database = status_database

    user_id = stolen.user_id
    status_id = stolen.status_id
    status_text = stolen.status_text
    params = (user_id, status_id, status_text, status_collection)

    result = main.add_status(*params)

    assert result is False


def test_add_status_true(stolen, status_collection):
    user_id = stolen.user_id
    status_id = stolen.status_id
    status_text = stolen.status_text
    params = (user_id, status_id, status_text, status_collection)

    result = main.add_status(*params)

    assert result is True


def test_update_status_false(stolen, status_collection):
    user_id = stolen.user_id
    status_id = stolen.status_id
    status_text = stolen.status_text
    params = (status_id, user_id, status_text, status_collection)

    result = main.update_status(*params)

    assert result is False


def test_update_status_true(stolen, status_collection, status_database):
    status_collection.database = status_database

    user_id = 'test'
    status_id = stolen.status_id
    status_text = 'test'
    params = (status_id, user_id, status_text, status_collection)

    result = main.update_status(*params)

    assert result is True


def test_delete_status_false(status_collection):
    status_id = 'test'

    result = main.delete_status(status_id, status_collection)

    assert result is False


def test_delete_status_true(status_collection, status_database):
    status_collection.database = status_database

    status_id = 'XKPiC6*iW!H3#6'

    result = main.delete_status(status_id, status_collection)

    with pytest.raises(KeyError):
        save = status_collection.database['XKPiC6*iW!H3#6']
        assert save is None
    assert result is True


def test_search_status(status_collection, status_database):
    status_collection.database = status_database
    print(status_collection.database)

    status_id = 'XKPiC6*iW!H3#6'

    result = main.search_status(status_id, status_collection)

    assert result.status_id == 'XKPiC6*iW!H3#6'

    status_id = 'test'

    result = main.search_status(status_id, status_collection)

    assert result is None


# menu tests


def test_menu_load_users_true(collection):
    menu.user_collection = collection
    with patch('menu.input') as mock_input:
        mock_input.return_value = "accounts.csv"
        menu.load_users()

        assert len(menu.user_collection.database) > 0
        assert menu.user_collection.database['evmiles97'].email == 'eve.miles@uw.edu'


def test_menu_load_users_false(collection):
    expected = "call('An error occurred while trying to load users')"
    menu.user_collection = collection
    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.return_value = "temp_file"
            menu.load_users()

    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_load_status_updates(status_collection):
    menu.status_collection = status_collection
    with patch('menu.input') as mock_input:
        mock_input.return_value = "status_updates.csv"
        menu.load_status_updates()

        assert len(menu.status_collection.database) > 0
        assert menu.status_collection.database['evmiles97_00001'].status_text == 'Code is finally compiling'


def test_menu_load_status_updates_false(collection):
    expected = "call('An error occurred while trying to load status updates')"
    menu.user_collection = collection
    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.return_value = "temp_file"
            menu.load_status_updates()

    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_add_user_true(collection):
    menu.user_collection = collection
    with patch('menu.input') as mock_input:
        mock_input.side_effect = ['ted', 'ted', 'ted', 'ted']
        menu.add_user()

        assert menu.user_collection.database['ted'].email == 'ted'


def test_menu_add_user_false(collection):
    menu.user_collection = collection
    menu.user_collection.database['ted'] = 'exists'
    with patch('menu.input') as mock_input:
        mock_input.side_effect = ['ted', 'ted', 'ted', 'ted']
        menu.add_user()

        assert menu.user_collection.database['ted'] == 'exists'


def test_menu_update_user_true(collection, tolby):
    menu.user_collection = collection
    with patch('menu.input') as mock_input:
        menu.user_collection.database['Cool_kid187'] = tolby
        mock_input.side_effect = ['Cool_kid187', 'ted', 'ted', 'ted']
        menu.update_user()

        assert menu.user_collection.database['Cool_kid187'].email == 'ted'


def test_menu_update_user_false(collection):
    menu.user_collection = collection
    with patch('menu.input') as mock_input:
        mock_input.side_effect = ['ted', 'ted', 'ted', 'ted']
        menu.update_user()

        with pytest.raises(KeyError):
            print(menu.user_collection.database['ted'])


def test_menu_search_user_true(collection, tolby):
    user_last_name = 'Bryant'

    expected = '''[call('User ID: Cool_kid187'),
 call('Email: mommasboy2001@gmail.com'),
 call('Name: Tolby'),
 call('Last name: Bryant')]'''

    menu.user_collection = collection
    menu.user_collection.database['Cool_kid187'] = tolby
    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['Cool_kid187']
            menu.search_user()

            mock_print.assert_called_with('Last name: ' + user_last_name)
    print(str(mock_print.call_args_list))
    assert str(mock_print.call_args_list) == expected


def test_menu_search_user_false(collection):
    expected = "call('ERROR: User does not exist')"

    menu.user_collection = collection
    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['Cool_kid187']
            menu.search_user()

    mock_print.assert_called_with("ERROR: User does not exist")
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_delete_user_true(collection, tolby):
    menu.user_collection = collection
    menu.user_collection.database['Cool_kid187'] = tolby

    with patch('menu.input') as mock_input:
        mock_input.side_effect = ['Cool_kid187']
        menu.delete_user()

    with pytest.raises(KeyError):
        print(menu.user_collection.database['Cool_kid187'])


def test_menu_delete_user_false(collection):
    expected = "call('An error occurred while trying to delete user')"
    menu.user_collection = collection

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['Cool_kid187']
            menu.delete_user()

    print(str(mock_print.call_args))
    with pytest.raises(KeyError):
        print(menu.user_collection.database['Cool_kid187'])
    assert str(mock_print.call_args) == expected


def test_menu_save_users_true(temp_file, collection, tolby):
    expected = """USER_ID,EMAIL,NAME,LASTNAME
Cool_kid187,mommasboy2001@gmail.com,Tolby,Bryant"""
    menu.user_collection = collection
    menu.user_collection.database['Cool_kid187'] = tolby

    with patch('menu.input') as mock_input:
        mock_input.side_effect = [f'{temp_file}']
        menu.save_users()

    with open(f'{temp_file}', 'r') as file:
        text = file.read()

    print(text)
    assert text == expected


def test_menu_save_users_false(collection, tolby):
    expected = """call('An error occurred while trying to save users')"""
    menu.user_collection = collection
    menu.user_collection.database['Cool_kid187'] = tolby

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['C:by.pyg8 : L^qJ/D-jA.kR6']
            menu.save_users()

    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_add_status_true(status_collection):
    menu.status_collection = status_collection

    with patch('menu.input') as mock_input:
        mock_input.side_effect = ['ted', 'ted', 'ted', 'ted']
        menu.add_status()

    assert menu.status_collection.database['ted'].status_text == "ted"


def test_menu_add_status_false(impeach, status_collection):
    menu.status_collection = status_collection
    menu.status_collection.database['XKPiC6*iW!H3#6'] = impeach
    expected = "call('An error occurred while trying to add new status')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.add_status()

    assert menu.status_collection.database['XKPiC6*iW!H3#6'].status_text != "ted"
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_update_status_true(impeach, status_collection):
    menu.status_collection = status_collection
    menu.status_collection.database['XKPiC6*iW!H3#6'] = impeach
    expected = "call('Status was successfully updated')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.update_status()

    assert menu.status_collection.database['XKPiC6*iW!H3#6'].status_text == "ted"
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_update_status_false(status_collection):
    menu.status_collection = status_collection
    expected = "call('An error occurred while trying to update status')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.update_status()

    with pytest.raises(KeyError):
        print(menu.status_collection.database['XKPiC6*iW!H3#6'])
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_search_status_true(impeach, status_collection):
    menu.status_collection = status_collection
    menu.status_collection.database['XKPiC6*iW!H3#6'] = impeach
    expected = "call('Status text: Impeach Trump!')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.search_status()

    assert menu.status_collection.database['XKPiC6*iW!H3#6'].status_text == "Impeach Trump!"
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_search_status_false(status_collection):
    menu.status_collection = status_collection
    expected = "call('ERROR: Status does not exist')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.search_status()

    with pytest.raises(KeyError):
        print(menu.status_collection.database['XKPiC6*iW!H3#6'])
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_delete_status_true(impeach, status_collection):
    menu.status_collection = status_collection
    menu.status_collection.database['XKPiC6*iW!H3#6'] = impeach
    expected = "call('Status was successfully deleted')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.delete_status()

    with pytest.raises(KeyError):
        print(menu.status_collection.database['XKPiC6*iW!H3#6'])
    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_menu_delete_status_false(collection):
    expected = "call('An error occurred while trying to delete status')"
    menu.user_collection = collection

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['Cool_kid187']
            menu.delete_status()

    print(str(mock_print.call_args))
    with pytest.raises(KeyError):
        print(menu.user_collection.database['Cool_kid187'])
    assert str(mock_print.call_args) == expected


def test_search_status_false(status_collection):
    menu.status_collection = status_collection
    expected = "call('ERROR: Status does not exist')"

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = ['XKPiC6*iW!H3#6', 'ted', 'ted', 'ted']
            menu.search_status()

    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


def test_save_status_true(temp_file, status_collection, impeach):
    expected = """STATUS_ID,USER_ID,STATUS_TEXT
XKPiC6*iW!H3#6,Hardline_Dem173,Impeach Trump!"""
    menu.status_collection = status_collection
    menu.status_collection.database['XKPiC6*iW!H3#6'] = impeach

    with patch('menu.input') as mock_input:
        mock_input.side_effect = [f'{temp_file}']
        menu.save_status()

    with open(f'{temp_file}', 'r') as file:
        text = file.read()

    print(text)
    assert text == expected


def test_save_status_false(status_collection, impeach):
    expected = """call('An error occurred while trying to save status updates')"""
    menu.status_collection = status_collection
    menu.status_collection.database['XKPiC6*iW!H3#6'] = impeach

    with patch('builtins.print') as mock_print:
        with patch('menu.input') as mock_input:
            mock_input.side_effect = [' C:by.pyg8 : L^qJ/D-jA.kR6']
            menu.save_status()

    print(str(mock_print.call_args))
    assert str(mock_print.call_args) == expected


@pysnooper.snoop()
def test_menu_menu():
    expected_input = ("[call('\\n    A: Load user database\\n    B: Load status database\\n    C: Add user\\n    "
                      "D: Update user\\n    E: Search user\\n    F: Delete user\\n    G: Save user database to file\\n"
                      "    H: Add status\\n    I: Update status\\n    J: Search status\\n    K: Delete status\\n    "
                      "L: Save status database to file\\n    Q: Quit\\n\\n    Please enter your choice: ')]")
    expected_print = "[call('Goodbye!')]"

    with pytest.raises(SystemExit):
        with patch('menu.print') as mock_print:
            with patch('menu.input') as mock_input:
                mock_input.side_effect = ['q']
                menu.menu()

    print('input:')
    print(str(mock_input.call_args_list))
    print('print:')
    print(str(mock_print.call_args_list))
    assert str(mock_input.call_args_list) == expected_input
    assert str(mock_print.call_args_list) == expected_print


if __name__ == '__main__':
    pytest.main(['-v'])
