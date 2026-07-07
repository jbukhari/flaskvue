# Provides a Config object that can be accessed across the app. Config values
# can optionally be set using environment variables, which are stored in the
# Config object.

import pathlib, os, yaml

class Config():
    app = None
    INTERNAL_JS = False
    INTERNAL_JS_PATH = pathlib.Path('../app/static/js').resolve()

for key, value in os.environ.items():
    setattr(Config, key, value)