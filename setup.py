from setuptools import setup


setup(
    name='django-fly',
    long_description=open('README.md').read(),
    version='0.0.2',
    py_modules=['django_fly'],
    install_requires=[
        'click',
    ],

    url = "https://github.com/LehaoLin/django-fly",
    author = "Lehao Lin",
    author_email = "lehaolin@link.cuhk.edu.cn",
    license='MIT',

    entry_points='''
        [console_scripts]
        django-fly=django_fly:cli
    ''',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],

)

