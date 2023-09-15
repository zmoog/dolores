# Dolores

Dolores is my personal assistant Discord bot.

The plan is to automate and make easy to access a variety of tasks like:

- Suggesting things to do next in work and personal environment.
- Fetch information (kids's grades, deals on Apple refurbished products, and more).
- Remind me of expiring tasks or old stuff I must clear out.

## Installation

There are no installation options for now. We are targeting pip in later releases.


## Usage

To run the bot, run the following:

    dolores run

For help, run:

    dolores --help

You can also use:

    python -m dolores --help

## Development

To contribute to this tool, first check out the code. Then, create a new virtual environment:

    cd dolores
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
