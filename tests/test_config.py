# -*- coding: utf-8 -*-
import yaml

from src.lib.config import yaml_parser


def test_yaml_parser_valid(mocker):
    """Test parsing valid YAML."""

    test_data = {'key1': 'value1'}

    # Mock open and yaml.safe_load
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=yaml.dump(test_data)))
    mock_safe_load = mocker.patch('yaml.safe_load', return_value=test_data)

    # Call with fake file path since we mocked open
    output = yaml_parser('fake/path/test.yaml')

    assert output == test_data
    mock_open.assert_called_once()
    mock_safe_load.assert_called_once()


def test_yaml_parser_yaml_error_with_mark(mocker):
    """Test parsing YAML with a marked error."""
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='key: value\ninvalid_yaml'))
    mock_safe_load = mocker.patch('yaml.safe_load')

    # Provide all required positional arguments for yaml.Mark
    mark = yaml.Mark('fake/path/test.yaml', 1, 5, pointer=10, column=5, buffer='context')
    mock_safe_load.side_effect = yaml.MarkedYAMLError('error', mark, 'context', 'problem', 'context_mark')

    output = yaml_parser('fake/path/test.yaml')

    assert output is None
    mock_open.assert_called_once()
    mock_safe_load.assert_called_once()


def test_yaml_parser_yaml_error_with_context(mocker):
    """Test parsing YAML with a context error."""
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='key: value\ninvalid_yaml'))
    mock_safe_load = mocker.patch('yaml.safe_load')
    mock_safe_load.side_effect = yaml.YAMLError('error', 'context', 'problem')

    output = yaml_parser('fake/path/test.yaml')
    assert output is None
    mock_open.assert_called_once()
    mock_safe_load.assert_called_once()


def test_yaml_parser_yaml_error_without_mark(mocker):
    """Test parsing YAML with an error but no mark."""
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='key: value\ninvalid_yaml'))
    mock_safe_load = mocker.patch('yaml.safe_load')
    mock_safe_load.side_effect = yaml.MarkedYAMLError('error', None, 'context', 'problem', 'context_mark')

    output = yaml_parser('fake/path/test.yaml')

    assert output is None
    mock_open.assert_called_once()
    mock_safe_load.assert_called_once()


def test_yaml_parser_file_not_found(mocker):
    """Test file not found case when parsing YAML."""

    # Mock open to raise FileNotFoundError
    mock_open = mocker.patch('builtins.open', side_effect=FileNotFoundError('File not found'))

    # Call with fake file path since we mocked open
    output = yaml_parser('fake/path/test.yaml')

    assert output is None
    mock_open.assert_called_once()


def test_yaml_parser_permission_error(mocker):
    """Test permission error case when parsing YAML."""

    # Mock open to raise PermissionError
    mock_open = mocker.patch('builtins.open', side_effect=PermissionError('Permission denied'))

    # Call with fake file path since we mocked open
    output = yaml_parser('fake/path/test.yaml')

    assert output is None
    mock_open.assert_called_once()


def test_yaml_parser_invalid_yaml(mocker):
    """Test parsing invalid YAML."""

    # Mock open and yaml.safe_load
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='{invalid: yaml}'))
    mock_safe_load = mocker.patch('yaml.safe_load', side_effect=yaml.YAMLError('Error parsing YAML'))

    # Call with fake file path since we mocked open
    output = yaml_parser('fake/path/test.yaml')

    assert output is None
    mock_open.assert_called_once()
    mock_safe_load.assert_called_once()


def test_yaml_parser_generic_exception(mocker):
    """Test a generic exception during YAML parsing."""

    # Mock open and yaml.safe_load
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    mock_safe_load = mocker.patch('yaml.safe_load', side_effect=yaml.YAMLError('Generic error'))

    # Call with fake file path since we mocked open
    output = yaml_parser('fake/path/test.yaml')

    # Assert that the output is None
    assert output is None

    # Assert that open and safe_load were called once
    mock_open.assert_called_once()
    mock_safe_load.assert_called_once()

def test_yaml_parser_io_error(mocker):
    """Test IOError case when parsing YAML."""

    # Mock open to raise an IOError
    mock_open = mocker.patch('builtins.open', side_effect=IOError('I/O error occurred'))

    # Call with fake file path since we mocked open
    output = yaml_parser('fake/path/test.yaml')

    assert output is None
    mock_open.assert_called_once()

