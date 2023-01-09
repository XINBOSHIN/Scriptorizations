from setuptools import setup

setup(
	name = 'xinboshin.script-validation-example',
	version = '1.0',
	py_modules = ['validation'],
	include_package_data = False,
	install_requires = ['xinboshin.script'],
	entry_points = {'console_scripts': ['validation = validation:main']}
)
