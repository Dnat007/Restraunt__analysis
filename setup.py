# responsible to create a ml project as a package and we can deploy it in pypi

from setuptools import find_packages, setup
from typing import List

HYPHEN = '-e .'
def get_requirements(file_path: str) -> List[str]:
    '''
    This function return the requirements list
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "")for req in requirements]
        
        if HYPHEN in requirements:
            requirements.remove(HYPHEN)
            
    return requirements


# meta-data
setup(
    name="MLPROJECT",
    version="0.0.1",
    author="Abhishek Singh",
    author_email="a.singh.gla@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)
