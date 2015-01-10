from nose.tools import with_setup
from blaze.utils import example

from mbs.settings import settings
from . import config_file, data_file
import tempfile

def setup_function():
    settings.reset()
    settings.data_file = tempfile.mkdtemp()

def teardown_function():
    pass


@with_setup(setup_function, teardown_function)
def test_from_pyfile_no_data_directory():
    old_data_dir = settings.data_directory
    config = config_file("config_no_data_directory.py")
    assert 'data' not in settings.data
    settings.from_pyfile(config)
    assert 'data' in settings.data
    assert settings.data_directory == old_data_dir

@with_setup(setup_function, teardown_function)
def test_from_pyfile_with_data_directory():
    old_data_dir = settings.data_directory
    config = config_file("config_with_data_directory.py")
    assert 'data' not in settings.data
    settings.from_pyfile(config)
    assert 'data' in settings.data
    assert settings.data_directory == '/tmp'

@with_setup(setup_function, teardown_function)
def test_dataset_storage():
    storage = settings.storage
    assert len(storage) == 0

@with_setup(setup_function, teardown_function)
def test_all_datasets():
    iris_file = example('iris.csv')
    config = config_file("config.py")
    settings.from_pyfile(config)
    settings.data_directory = data_file('datadir')
    all_sets = settings.datamanager.all_datasets()
    assert set(all_sets.keys()) == {'accounts', 'cities', 'events'}

    #now we introduce an error by adding a csv that has tab separators
    settings.datamanager.configure('defaultuser', 'test.csv', delimiter="|")
    all_sets = settings.datamanager.all_datasets()
    assert set(all_sets.keys()) == {'accounts', 'cities', 'events',
                                    'defaultuser/test.csv'}