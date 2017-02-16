from distutils.core import setup

setup(
    name='qrep',
    packages=['qrep'],
    version='0.1.2',
    description='Interactive query-replace',
    author='Logan Buckley',
    author_email='logan.buckley@gmail.com',
    url='https://github.com/loganmhb/qrep',
    download_url='https://github.com/loganmhb/qrep/tarball/0.1.2',
    keywords=['cli query replace sed'],
    entry_points={
        'console_scripts': [
            'qrep=qrep.qrep:main'
        ]
    },
    classifiers=[]
)
