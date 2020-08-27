from setuptools import setup, find_packages, Extension

setup(
    name="lightmatchingengine",
    url="https://github.com/gavincyi/LightMatchingEngine",
    license='MIT',

    author="Gavin Chan",
    author_email="gavincyi@gmail.com",

    description="A light matching engine",

    packages=find_packages(exclude=('tests',)),

    use_scm_version=True,
    install_requires=[],
    setup_requires=['setuptools_scm', 'cython'],
    ext_modules=[Extension(
        'lightmatchingengine.lightmatchingengine',
        ['lightmatchingengine/lightmatchingengine.pyx'])],
    tests_require=[
	'pytest'
    ],
    extras_require={
        'performance': ['pandas', 'docopt', 'tabulate', 'tqdm']
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

)
