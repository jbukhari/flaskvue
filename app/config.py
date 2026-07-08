# Provides a Config object that can be accessed across the app. Config values
# can optionally be set using environment variables, which are stored in the
# Config object.

import pathlib, os, yaml

class Config():
    app = None
    INTERNAL_JS = False
    INTERNAL_JS_PATH = pathlib.Path('../app/static/js').resolve()
    VUE_SRC = 'https://unpkg.com/vue@3.5.29/dist/vue.esm-browser.js'
    VUE_DEVTOOLS_SRC = 'https://unpkg.com/@vue/devtools-api@8.1.1/dist/vue-devtools-api.esm-browser.js'
    PINIA_SRC = 'https://unpkg.com/pinia@3.0.4/dist/pinia.esm-browser.js'

for key, value in os.environ.items():
    setattr(Config, key, value)