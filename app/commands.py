# Custom Flask commands defined in blueprints. Run with `flask cmd <command>`.

import os, click, requests
from flask import Blueprint
from app.config import Config

commands = Blueprint('cmd', __name__)

@commands.cli.command('download-js-modules')
def download_js_modules():
    """Download JS modules for internal use."""

    print('Running...')

    js_modules = {
        Config.VUE_FN: Config.VUE_SRC,
        Config.VUE_DEVTOOLS_FN: Config.VUE_DEVTOOLS_SRC,
        Config.PINIA_FN: Config.PINIA_SRC
    }

    js_dir = Config.INTERNAL_JS_PATH
    os.makedirs(js_dir, exist_ok=True)

    for filename, url in js_modules.items():
        response = requests.get(url)

        if response.status_code == 200:
            with open(os.path.join(js_dir, filename), 'wb') as f:
                f.write(response.content)

            print(f'Downloaded {filename} to {js_dir}')
        else:
            print(f'Failed to download {filename} from {url}')
