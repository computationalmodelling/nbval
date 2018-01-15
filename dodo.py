PYTHON = "python3"

DOIT_CONFIG = {
    'default_tasks': ['test'],
    'verbosity': 2,
}

def task_test():
    return {
        'actions': [
            ["py.test", "-v", "tests/", "--nbval", "--current-env", "--sanitize-with", "tests/sanitize_defaults.cfg", "--ignore", "tests/ipynb-test-samples"],
        ],
    }

def task_install_test_deps():
    test_deps = ['matplotlib', 'sympy', 'pytest-cov']
    return {
        'actions': [['pip', 'install'] + test_deps],
    }

def task_build_dists():
    return {
        'actions': [
            ["rm", "-rf", "dist/"],
            [PYTHON, "setup.py", "sdist"],
            [PYTHON, "setup.py", "bdist_wheel"],
        ],
    }

def task_release():
    return {
        'actions': [["twine", "upload", "dist/*"]],
        'task_dep': ['build_dists']
    }
