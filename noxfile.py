import os
import nox


@nox.session(venv_backend='conda',
             python=os.environ.get('TRAVIS_PYTHON_VERSION', '3.7'))
def tests(session):
    session.install('.[all]')

    # run unit tests
    # docstrings
    # pytest doctest docs: https://docs.pytest.org/en/latest/doctest.html
    # doctest docs: https://docs.python.org/3/library/doctest.html
    # and examples (this is a hacky way to do it since --doctest-modules will
    # first load any .py files, which are the examples, and then try to run
    # any doctests, there isn't any)
    session.run(
        'pytest',
        'tests/',
        'src/',
        'examples/',
        '--cov=sklearn_evaluation',
        '--doctest-modules',
    )
    session.run('coveralls')

    if session.python == '3.7':
        session._run('conda', 'env', 'update', '--prefix',
                     session.virtualenv.location, '--file',
                     'docs/environment.yml')

        # build docs so we can detect build errors
        session.run('make', '-C', 'docs/', 'html', external=True)
