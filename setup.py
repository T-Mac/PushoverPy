from distutils.core import setup

setup(
    name='PushoverPy',
    version='1.0.2',
    author='Taylor McKinnon',
    author_email='htmlfreak117@gmail.com',
    packages=['PushoverPy'],
    url='https://github.com/T-Mac/PushoverPy/blob/master/Pushover.py',
    license='GPLv3',
    description='Simple api to pushover.net',
    long_description=open('README.txt').read(),
    install_requires=[
       "requests == 2.0.0",
    ],
)