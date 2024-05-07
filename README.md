# PyPluginizer
<span style="font-size:larger;">A Versatile Plugin Framework written in python</span>

<details open="open">
<summary>Table of Contents</summary>

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
- [Support](#support)
- [License](#license)

</details>

### Getting Started with PyPluginizer
Welcome to PyPluginizer, a Python plugin framework designed to simplify the development of modular applications and extendable systems.<br>

### Prerequisites
Before installing PyPluginizer, ensure that you have the following prerequisites met:<br>

* Python: PyPluginizer requires Python 3.6 or higher to run. Make sure Python is installed on your system.<br>

### Installation

To install PyPluginizer, you'll need to clone the repository to your local machine. Follow these steps:

1. Open your terminal or command prompt.

2. Navigate to the directory where you want to clone the repository.

3. Clone the PyPluginizer repository using the following command:

   ```bash
   git clone https://github.com/cbabil/PyPluginizer.git
   ```

### Configuration

The configuration file `config.yaml` controls various aspects of PyPluginizer:

```yaml
app:
  name: "PyPluginizer"
  description: "A Plugin framework written in python"

  # Logger
  logger:
    level: "INFO"
    format: "%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"

  # Core plugins
  core:
    directory: ./src/plugins/core
    
  # Users plugins
  users:
    directory: ./src/plugins/users

  # Plugins responsible for exporting data in a particular format.
  exporters:
    directory: ./src/plugins/exporters
```

This configuration file (configuration.yaml) defines:

**app**: Details about the PyPluginizer application.<br>
**logger**: Configuration for the logging system.<br>
**core**: Directory where core plugins are located.<br>
**users**: Directory where user plugins are located.<br>
**exporters**: Directory where exporter plugins are located.<br>

You can modify this configuration file according to your requirements.

### Usage

To get started with PyPluginizer, follow these steps:

1. **Setup Virtual Environment**: Run the following command to create a virtual environment:
   ```bash
   make venv
   ```
2. **Activate Virtual Environment**: Run the following command to activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. **Install Dependencies**: Run the following command to install the dependencies:
   ```bash
   make setup
   ```
4. **Run the Application**: Execute the following command to run the application:
  ```bash
  make run
  ```
5. **Run Tests**: To run the unit tests using pytest, use the following command:
  ```bash
  make test
  ```
6. **Clean Up**: Before running make clean, make sure to deactivate the virtual environment:
  ```bash
  deactivate
  make clean
  ```

### How-To

The How-To section provides guidance on common tasks related to PyPluginizer.

#### Ignoring a Plugin

To ignore a plugin, simply create a blank `IGNORE` file in the plugin directory.

#### Defining Dependencies

To define dependencies for a plugin, create a `DEPENDENCY` file in the plugin directory and list the dependent plugin names in the order of dependencies.

#### Changing Plugin Version

To change the version of a plugin, edit the `VERSION` file in the plugin directory.


## Support
Reach out to the maintainer at the following places:

- [GitHub discussions](https://github.com/pi-detective/discussions)


## License

This project is licensed under the **MIT license**. Feel free to edit and distribute this as you like.

See [LICENSE](LICENSE) for more information.
