```table-of-contents
```
# Multiple Python Runtime (Raw)
ways:
1. visit python download center, choose your required version and download & install it.
2. download python manager from python website and use the following commands.
	`py install <required version>`
	be specific for subversion or else it will download the latest version
3. check the downloaded versions using `py -0`
4. get the executable path using following commands on 
	`py -<version> -c "import sys; print(sys.executable)"
5. set the executable path in environment variables using:
	`setx PYTHON<VERSION> "EXCECUTABLE PATH FOR THE VERSION"`
`
# Manage using python virtual environments
1. create python virtual environment, after setting environment variables using:
	`py -<version> -m venv <virtual environment name>`
	eg: `py -3.13 -m venv .venv313`
2. Access the virtual environment using:
	eg. `.venv313/scripts/activate`

# Manage using python poetry library
1. Now to create poetry shell for this version use `poetry env use $env:PYTHON314` and after its output use poetry shell
2. If using poetry regularly, add the following method in $PROFILE file:
```powershell
function poetry-use {
    param([string]$ver)
    $exe = (py -$ver -c "import sys; print(sys.executable)")
    poetry env use $exe
    poetry shell
}
```
*not sure about $PROFILE*: run `echo $PROFILE` this will give you path and you can add the above function to it
