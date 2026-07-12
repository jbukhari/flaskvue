# Provides a Config object that can be accessed across the app. Config values
# can optionally be set using environment variables, which are stored in the
# Config object.

import pathlib, os, yaml

class Config():
    app = None
    VUE_SRC = 'https://unpkg.com/vue@3.5.29/dist/vue.esm-browser.js'
    VUE_DEVTOOLS_SRC = 'https://unpkg.com/@vue/devtools-api@8.1.1/dist/vue-devtools-api.esm-browser.js' # required for Pinia
    PINIA_SRC = 'https://unpkg.com/pinia@3.0.4/dist/pinia.esm-browser.js'
    INTERNAL_JS = False
    INTERNAL_JS_PATH = pathlib.Path('../app/static/js').resolve()
    VUE_FN = VUE_SRC.split('/')[-1]
    VUE_DEVTOOLS_FN = VUE_DEVTOOLS_SRC.split('/')[-1]
    PINIA_FN = PINIA_SRC.split('/')[-1]

# Set config values from environment variables, if they exist.
for key, value in os.environ.items():
    if value.lower() in ['0', 'false', 'none', 'null']:
        setattr(Config, key, None)
    else:
        setattr(Config, key, value)