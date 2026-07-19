# Flask custom commands tests. Fixtures come from conftest.py.

import pytest, click, responses
from app.config import Config

@responses.activate
def test_download_js_modules(runner, tmp_path):
    Config.INTERNAL_JS_PATH = tmp_path
    responses.add(responses.GET, Config.VUE_SRC, body='ok')
    responses.add(responses.GET, Config.VUE_DEVTOOLS_SRC, body='ok')
    responses.add(responses.GET, Config.PINIA_SRC, body='ok')
    result = runner.invoke(args='cmd download-js-modules')
    
    for module_fn in [Config.VUE_FN, Config.VUE_DEVTOOLS_FN, Config.PINIA_FN]:
        with open(f'{Config.INTERNAL_JS_PATH}/{module_fn}', 'r') as f:
            assert f.readline() == 'ok'
