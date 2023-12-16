import os
from bs4 import BeautifulSoup
from codecraft.fileparsing.CodeCraftFile import CodeCraftConfig

class Apps:
    
    @staticmethod
    def createApp(app_name: str, app_type: str, lib_type: str):
        if not (os.path.exists("./.codecraft") and os.path.isfile("./.codecraft")):
            print("Project doesn't exists!")
        else:
            Apps._addAppToProjectFile(app_name, app_type, lib_type)
            #Projects._createAppDirs()
    
    @staticmethod
    def _addAppToProjectFile(app_name: str, app_type: str, lib_type: str):
        print("Creating App File...")
        config = CodeCraftConfig()
        config.addApp(app_name, app_type, lib_type)

        
    @staticmethod
    def _createAppDirs():
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
    def deleteApp(app_name: str):
        if os.path.exists("./.codecraft"):
            config = CodeCraftConfig()
            config.removeApp(app_name)
        else:   
            print("Current folder doesn't contain a project!")
            
    @staticmethod
    def linkLibrary(app_name: str, library_name: str, accessibility: str = "PRIVATE", modules: dict = []):
        
        if os.path.exists("./.codecraft"):
            if accessibility != "PUBLIC" and accessibility != "PRIVATE":
                print("Invalid accessibility keyword!")
                return
            config = CodeCraftConfig()
            config.linkLibrary(app_name, library_name, accessibility, modules)
        else:   
            print("Current folder doesn't contain a project!")
        
        return
    
    @staticmethod
    def unlinkLibrary(app_name: str, library_name: str):
        
        if os.path.exists("./.codecraft"):
            config = CodeCraftConfig()
            config.unlinkLibrary(app_name, library_name)
        else:   
            print("Current folder doesn't contain a project!")
        
        return
            
        