# Discord Bot

<!-- Table of contents generated using `npx doctoc README.md -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Run](#run)
- [Updating dependencies](#updating-dependencies)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Getting started

### Installation

On Linux/MacOS:

```
pip install -r requirements.txt
```

On Windows:

```
py -m pip install -r requirements.txt
```


### Configuration

Copy `config.yml.example` to `config.yml`.

Go to [Discord Developer Portal](https://discord.com/developers/applications) and create a new app and save the secret token.

Edit `config.py` and set `token: 'YOUR_TOKEN_HERE'`.


### Run

On Linux/MacOs:

```
python main.py
```

On Windows:

```
py main.py
```

## Updating dependencies

Delete and regenerate `requirements.txt`:

```
pip freeze > requirements.txt
```
