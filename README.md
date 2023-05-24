# itch-lutris-script-generator
Generates scripts for installing itch games on lutris.

# How to Use
Run `itch-lutris.py` to generate an install script for lutris.

The program takes the following arguments:

 * url (positional) - The URL for the game you want to install
 * apikey (optional) - Your itch.io API key. This is used to detect what platforms a game is available on. This is not needed if you force a specific version
 * force_linux (optional) - Force the program to generate a script to install the linux version. apikey is not needed if this is set
 * force_wine (optional) - Force the program to generate a script to install the windows version. apikey is not needed if this is set
 * install (optional) - Install the generated script with lutris immediately. Lutris must be in your path for this to work

Examples:

Generates a script for windows and installs immediately:
 * `itch-lutris.py https://rayquaza01.itch.io/enchanted-gemstones --force-wine --install`

Generates a script for the default version (linux if available, fallback to windows if not):
 * `itch-lutris.py https://rayquaza01.itch.io/enchanted-gemstones --apikey <YOUR_API_KEY>`

# Acknowledgements
Much of the code for generating the install scripts was adapted from the lutris source code.
