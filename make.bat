if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  test         to run tests
	echo.  build-dists  to build distribution files
	echo.  release      to build distribution files and upload them
	goto end
)

if "%1" == "test" (
	REM Note: to run the tests, we also need additional dependencies
	REM call make.bat install-test-deps
	py.test -v tests/ --nbval --current-env --sanitize-with tests/sanitize_defaults.cfg --ignore tests/ipynb-test-samples
	goto end
)

if "%1" == "build-dists" (
    for /d %%i in (dist\*) do rmdir /q /s %%i
	del /q /s dist\*
	python setup.py sdist
	python setup.py bdist_wheel
	goto end
)

if "%1" == "release" (
    for /d %%i in (dist\*) do rmdir /q /s %%i
	del /q /s dist\*
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
	goto end
)

:end
