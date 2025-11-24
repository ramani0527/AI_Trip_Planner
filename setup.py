from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """ This fuction will return list of requirements"""
    requirement_list:List[str]=[]
    
    try:
        #open and read the requirements.txt file
        
        with open('requirements.txt','r') as file:
        # read lines from the file
            lines= file.readlines()
        #process each line
            for line in lines:
        # strip whitspace and newline characters
                requirement = line.strip()
        #ignore empty lines and -e .

                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)
                
    except FileNotFoundError:
        print("requirement.txt file not found.")
    return requirement_list
print(get_requirements())    


setup(
    name= "AI_Trip_Planner",
    version = "0.0.1",
    author= "ramani",
    author_email = "ramanim.ip@gmail.com",
    packages= find_packages(),
    install_requires= get_requirements()
        
)