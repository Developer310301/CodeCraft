import os
import shutil
from bs4 import BeautifulSoup
from codecraft.fileparsing.CodeCraftFile import CodeCraftConfig

class Projects:
    
    @staticmethod
    def createProject(name: str):
        if os.path.exists("./.codecraft") and os.path.isfile("./.codecraft"):
            print("Project already exists!")
        else:
            Projects._createProjectFile(name)
            Projects._createProjectDirs()
            print("Project created!")
    
    @staticmethod
    def _createProjectFile(project_name: str):
        print("Creating Project File...")
        CodeCraftConfig.createConfigFile(project_name)
        CodeCraftConfig()
        
    @staticmethod
    def _createProjectDirs():
        print("Creating Project Directories...")
        if not(os.path.exists("apps") and os.path.isdir("apps")):
            os.mkdir("apps")
        if not(os.path.exists("test") and os.path.isdir("test")):
            os.mkdir("test")
        if not(os.path.exists("outputs") and os.path.isdir("outputs")):
            os.mkdir("outputs")
        if not(os.path.exists("outputs/Release") and os.path.isdir("outputs/Release")):
            os.mkdir("outputs/Release")
        if not(os.path.exists("outputs/Debug") and os.path.isdir("outputs/Debug")):
            os.mkdir("outputs/Debug")
    
    @staticmethod
    def deleteProject():
        if os.path.exists("./.codecraft"):
            shutil.rmtree("./.codecraft")
            print("Project deleted")
        else:   
            print("Current folder doesn't contain a project!")
            
        