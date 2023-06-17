from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.1.2',
    description='Sorting files be category',
    url='https://github.com/notabe71/clean_folder',
    author='Nataliia Bushyna',
    author_email='notabe71@gmail.com',
    license='KE',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:main']}
)
