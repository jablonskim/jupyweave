from setuptools import setup, find_packages


setup(
    name='jupyweave',
    version='0.1.0',

    description='',  # TODO
    long_description='',  # TODO

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
    packages=find_packages(),
    install_requires=[],  # TODO
    package_data={},  # TODO

    entry_points={
        'console_scripts': ['jupyweave=jupyweave:main']
    }
)
