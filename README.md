# nano_machina
**nano machines?**

This is a Twitch chat/irc bot written in Python (2.6 / 2.7) with **full whisper support** and a twist on the Metal Gear Solid series.

## Installation
You can follow my detailed instructions below or just run:

```shell
python setup.py
```

### Virtual Environment
I would recommend running this in a virtual environment to keep your dependencies in check. If you'd like to do that, run:

```shell
sudo pip install virtualenv
```

Followed by:

```shell
virtualenv venv
```

This will create an empty virtualenv in your project directory in a folder called "venv." To enable it, run:

```shell
source venv/bin/activate
```

and your console window will be in that virtualenv state. To deactivate, run:

```shell
deactivate
```

### Dependencies
To install all dependencies locally (preferably inside your activated virtualenv), run:

```shell
pip install -r requirements.txt
```

### Further Steps
Make a copy of the example config file and globals file:

```shell
cp src/config/config_example.py src/config/config.py
cp globals_example.py globals.py
```

#### Config Files
Head into `src/config/config.py` and enter the correct channels and cron jobs you'd like to run. Input appropriate Oauth tokens in `globals.py`.

## Make It Do
### Adding your own commands
You're going to need to know basic Python if you want to add your own commands. Open up `src/lib/command_headers.py`. There are examples of pre-made commands in there as examples. The limit parameter is the amount of times a command can be used in seconds, if you don't want a limit to be enforced put in `0`.

If your command is only going to return a string, ex - `'!hello'` returns `'Welcome!'`, don't include the `'argc'` parameter. Place the string you wish to be returned to the user in the `'return'` parameter. For example, if you wanted to create a command such as this and limit it to being used ever 30 seconds, you would add in:

```python
'!hello': {
    'limit': 10,
    'return': 'Welcome!'
}
```

However, if your command has to have some logic implemented and if the command is just going to return whatever a function returns, set the `'return'` parameter on the command to `'command'`, and set `'argc'` to `0`. If your command is going to take arguments, ex `'!hello [name]'`, set `'argc'` to `'1'` or however many arguments the command is going to take in.

Make a new file in `'lib/commands/'` and give the filename `'command.py'` where `command` is the command name. If your `'argc'` was set to `0`, don't include `'args'` in the functions parameters, else set the only parameter to `'args'`. Args will contain a list of whatever arguments were passed to the command.

This command will contain whatever logic needs to be carried out. You should validate the arguments in there. After you have the response that you want a user to see, just 'return' it.

Let's say we want to add a command which will take two arguments, we will call it `'!random'` and it will take a `'minimum'` and `'maximum'` argument. We will limit this command to be allowed to be called every 20 seconds.

Add the following to the `'commands'` dictionary in `src/lib/command_headers.py`:

```python
'!random': {
    'limit': 20,
    'user_limit': 15,
    'argc': 2,
    'return': 'command',
    'ul': 'mod',
    'space_case': True,
    'optional': True
}
```

`'limit'` refers to the cooldown. The cooldown is only active per separate channel

`'user_limit'` is the same as `'limit'`, but affects individual users

`'argc'` refers to the number of arguments a command accepts, separated by spaces. If the command does not have `'command'` as its `'return'` value, this is not necessary. However, even if there are no arguments and `'command'` is listed, `0` should be used.

If a command is not intended for use by moderators, there is no need for `'ul'` to be included

a `'space_case'` is a special scenario where you would like a command to have a single argument, but no limits to the number of separate strings you can input. Normally, arguments are separated by spaces.

If `'optional'` is specified as a key, no matter what its value is (`True`/`False`), etc, the command will have optional arguments. The corresponding function should take into account the possibility of args being an empty array (`if len(args) < 1`).

## Finally
### To run:

```shell
./serve.py
```
