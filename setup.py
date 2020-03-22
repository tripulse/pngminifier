import setuptools
import subprocess

setuptools.setup(
    name= 'pngminifier',
    version= subprocess.check_output(['git', 'describe', '--tags']).strip() \
            .decode('utf-8') \
            .split('-g')[0],
    description= "a program that strips out ancillary data "
                "from PNG files and reduces the file slightly",
    author= "Shantanu Biswas",
    author_email= "bsantanu381@gmail.com",
    packages= ['pngminifier'],
    project_urls= {
        'Github': 'https://github.com/tripulse/pngminifier'
    },
    license= 'The Unlicense',
    license_file= 'LICENSE.md',
    keywords= [
        'png', 'minifier', 'minification', 'truncator'
        'exif tag remover', 'pngminify'
    ],
    python_requires= ">=3.8",
    entry_points={
        'console_scripts': [
            'pngminifier=pngminifier.__main__:main',
        ],
    }
)