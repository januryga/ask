@echo off

where virtualenv
if %ERRORLEVEL% NEQ 0 (
	echo Couldn't find virtualenv. Please install it with pip.
	goto :end
) else (
	goto :safe
)

:safe
	echo WARNING! THIS SCRIPT WILL CLEAR THE CURRENT lib/ FOLDER!
	set /p givenpath= "Enter a path to a Python 2.7 executable: "
	if exist %givenpath% goto :install else goto :error


:install
	virtualenv --python=%givenpath% --clear lib && (
	lib\Scripts\pip install -r requirements.txt )
	goto :end


:error
	echo %givenpath% Doesn't exist or isn't a valid Python exe.
	goto :end




:end