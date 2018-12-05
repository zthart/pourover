init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test: 
	pipenv run py.test

publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg pourover.egg-info

