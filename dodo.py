import sys
PYTHON = sys.executable

DOIT_CONFIG = {
    'default_tasks': ['test'],
    'verbosity': 2,
}

def _make_cmd(cmd):
    import os
    if os.name == 'nt':
        return ' '.join(cmd)
    return cmd

def _clean_dist_cmd():
    import shutil
    try:
        shutil.rmtree("dist")
    except FileNotFoundError:
        pass

def task_test():
    return {
        'actions': [
            _make_cmd(["py.test", "-v", "tests/", "--nbval", "--nbval-current-env", "--nbval-sanitize-with", "tests/sanitize_defaults.cfg", "--ignore", "tests/ipynb-test-samples"]),
        ],
    }

def task_install_test_deps():
    # ipython_genutils is an indirect dependency of nbdime, but can be removed from this list
    # once https://github.com/jupyter/nbdime/pull/618 ends up in a release
    test_deps = ['matplotlib', 'sympy', 'pytest-cov', 'pytest-mock', 'nbdime', 'ipython_genutils']
    return {
        'actions': [_make_cmd(['pip', 'install'] + test_deps)],
    }

def task_build_dists():
    return {
        'actions': [
            (_clean_dist_cmd,),
            _make_cmd([PYTHON, "setup.py", "sdist"]),
            _make_cmd([PYTHON, "setup.py", "bdist_wheel"]),
        ],
    }

def task_release():
    return {
        'actions': [["twine", "upload", "dist/*"]],
        'task_dep': ['build_dists']
    }
