from testing.utilities import run_all_tests, run_test

if __name__ == "__main__":
    results = run_all_tests()
    import json

    print(json.dumps(results, indent=2))