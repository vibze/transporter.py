from setuptools import setup


setup(
    name='Transporter',
    version='1.0',
    py_modules=['transporter'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        transporter=cli:cli
    '''
)