# translator-menu
A tkinter window allowing to find Linguee-traduction in a convenient way

When you execute the program, you can type a word and then press enter to get up to 3 possible translations.

Pressing Escape closes the window.

When installed, the dictionnary is french <--> english but you can modify the comportment by changing the value of the `base_url` member in the Lingueebackend class.

# Dependencies

You can install all dependencies with

```bash
pip install -r requirements.txt
```

I recommend using a virtual environment such as [venv](https://docs.python.org/3/library/venv.html) to isolate the dependencies from what is already installed on your system.

# Usage

Simply run
```bash
/bin/python3 main.py
```

I suggest to bind the command to a key combination to make it more convenient. I use [xbindkey](https://wiki.archlinux.org/title/Xbindkeys) for instance.