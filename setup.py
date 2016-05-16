from setuptools import setup, find_packages


setup(
    name='jupyweave',
    version='0.1.2',

    description='Dynamic report generator',

    url='https://github.com/jablonskim/jupyweave',

    author='Mateusz Jablonski',
    author_email='mjablonski92@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Documentation',
        'Topic :: Text Processing :: Markup',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='jupyweave literate programming',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=['pygments', 'jupyter', 'jupyter_client'],
    package_data={
        'jupyweave': ['configs/*.json', 'user_processors/*.py', 'processors/*.py']
    },

    entry_points={
        'console_scripts': [
            'jupyweave=jupyweave:main',
            'jupyweave_install=jupyweave:install'
        ]
    }
)
