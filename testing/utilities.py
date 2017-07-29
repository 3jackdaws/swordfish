from glob import glob
import re
import json
from importlib.util import spec_from_file_location, module_from_spec
from urllib.request import urlopen, Request
from urllib.parse import urlencode

registered_tests = []

def test(test_function):
    global registered_tests
    registered_tests.append({
        "module":test_function.__module__,
        "name":test_function.__name__,
        "function":test_function
    })

def run_test(test_object):
    if isinstance(test_object, dict) and "function" in test_object:
        return test_object['function']()


def load_module_from_path(path):
    spec = spec_from_file_location(re.findall("([a-z0-9-_]+)\.py$", path)[0], path)

    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_all_tests():
    global registered_tests
    for file_path in glob("tests/**", recursive=True):
        module_path = re.findall("tests[a-z0-9/-_]+\.py", file_path)
        if module_path:
            module_path = re.sub(r'\\{2}|\\', "/", module_path[0])
            load_module_from_path(module_path)

    results = []
    for test in registered_tests:
        test_passed = False
        message = None
        try:
            run_test(test)
            test_passed = True
        except Exception as e:
            test_passed = False
            message = str(type(e).__name__) + ": " + str(e)
        del test['function']
        results.append({
            "test":test,
            "result":{
                "passed":test_passed,
                "message":message
            }
        })
    return results

def http_get_json(url_or_request):
    return json.loads(urlopen(url_or_request).read().decode('utf-8'))


def http_post_json(url_or_request, data=None):
    return json.loads(urlopen(url_or_request, urlencode(data).encode('utf-8')).read().decode('utf-8'))

