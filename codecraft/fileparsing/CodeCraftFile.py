import os
import shutil
from bs4 import BeautifulSoup
from bs4.element import Tag

FILE_NAME = "./.codecraft"

class CodeCraftConfig:
    
    def __init__(self):
        with open(FILE_NAME,"r") as f:
            self._root = BeautifulSoup(f.read(),"xml")
        if(not os.path.exists("CMakeLists.txt")):
            self._writeProjectCMake()
    
    @staticmethod
    def createConfigFile(project_name: str):
        with open(FILE_NAME,"w") as f:
            data=""
            xml_data = BeautifulSoup(data,"xml")
            xml_project = xml_data.new_tag("Project")
            xml_projectsettings = xml_data.new_tag("ProjectSettings")
            xml_apps = xml_data.new_tag("Apps")
            xml_projectsettings.attrs["ProjectName"] = project_name
            xml_projectsettings.attrs["CMakeVersion"] = "3.10"
            xml_project.append(xml_projectsettings)
            xml_project.append(xml_apps)
            xml_data.append(xml_project)
            f.write(xml_data.prettify())
    
    def addApp(self, appName: str, appType: str, libType: str = ""):
        if not self._root.find("App", {"name":appName}):
            app_tag = self._root.new_tag("App")
            app_tag.attrs["name"] = appName
            app_tag.attrs["type"] = appType
            if appType == "lib":
                app_tag.attrs["lib_type"] = libType
            self._root.find("Apps").append(app_tag)
            with open(FILE_NAME,"w") as f:
                f.write(self._root.prettify())
            os.mkdir("apps/"+appName)
            os.mkdir("apps/"+appName+"/include")
            os.mkdir("apps/"+appName+"/src")
            self._writeAppCMake(app_tag)
            print(f"App {appName} successfully created!")
        else:
            print(f"App {appName} already exists!")
            
    def removeApp(self, appName: str):
        
        app = self._root.find("App", {"name":appName})
        
        if app:
            
            for lib in self._root.find_all("Library", {"name": appName}):
                lib.decompose()
                #Update others apps that have the current app as dependency
                self._writeAppCMake(lib.find_parent("App"))
            
            app.decompose()
            with open(FILE_NAME,"w") as f:
                f.write(self._root.prettify())
            if os.path.exists("apps/"+appName):
                shutil.rmtree("apps/"+appName)
            print(f"App {appName} deleted!")
            
        else:
            print("Selected app doesn't exists!")
            
    def linkLibrary(self, app_name: str, library_name: str, accessibility: str = "PRIVATE", modules: dict = []):
        
        app = self._root.find("App", {"name":app_name})

        if app:
            lib = app.findChild("Library", {"name": library_name})
            if lib:
                print(f"Library {library_name} already linked in app!")
            else:
                lib = self._root.new_tag("Library")
                modules_tag = self._root.new_tag("Modules")
                lib.attrs["name"] = library_name
                lib.attrs["access"] = accessibility
                
                for module in modules:
                    if module != "":
                        mod = self._root.new_tag("Module")
                        mod.attrs["name"] = module
                        modules_tag.append(mod)
                
                lib.append(modules_tag)
                libs = app.findChild("Libraries")
                if libs:
                    libs.append(lib)
                else:
                    libs = self._root.new_tag("Libraries")
                    libs.append(lib)
                    app.append(libs)
                with open(FILE_NAME,"w") as f:
                    f.write(self._root.prettify())
                self._writeAppCMake(app)
                print(f"Library {library_name} linked to {app_name}!")
        else:
            print(f"App {app_name} doesn't exists!")
            
    def unlinkLibrary(self, app_name: str, library_name: str):
        
        app = self._root.find("App", {"name":app_name}) 
        
        if app:
            lib = app.findChild("Library", {"name": library_name})
            
            if lib:
                lib.decompose()
                with open(FILE_NAME,"w") as f:
                    f.write(self._root.prettify())
                self._writeAppCMake(app)
                print(f"Library {library_name} unlinked from {app_name}!")
            else:
                print(f"Library {library_name} doesn't exists!")
            
        else:
            print(f"App {app_name} doesn't exists!")
            
    def _writeProjectCMake(self):
        
        project_settings = self._root.find('ProjectSettings')
        
        content = f"cmake_minimum_required(VERSION {project_settings.attrs['CMakeVersion']})\n"
        content += f"set(PROJECT_NAME {project_settings.attrs['ProjectName']})\nset(CMAKE_CXX_STANDARD 14)\n"
        content += r"project(${PROJECT_NAME})" + "\n"
        content += r"set(CMAKE_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME})" + "\n"
        content += r"# Set the install prefix\n"\
                    r"set(CMAKE_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME})" + "\n"\
                    "\n"\
                    "#--------------------------- Set Binary Output Directories --------------------------\n"\
                    "# Set the output directory for the build executables\n"\
                    r"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/outputs/${CMAKE_BUILD_TYPE}/bin)" + "\n"\
                    "# Set the output directory for the build libraries\n"\
                    r"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/outputs/${CMAKE_BUILD_TYPE}/lib)" + "\n"\
                    "# Set the output directory for the build libraries\n"\
                    r"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/outputs/${CMAKE_BUILD_TYPE}/lib)" + "\n"
        content += "#--------------------------- Include the applications---------------------------------\n"\
                    "# Get all directories inside the 'apps' directory\n"\
                    r"file(GLOB children RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/apps ${CMAKE_CURRENT_SOURCE_DIR}/apps/*)" + "\n"\
                    "# Loop over the directories\n"\
                    r"foreach(child ${children})" + "\n"\
                    "    # Check if it's a directory\n"\
                    r"    if(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/apps/${child})" + "\n"\
                    "        # Add the directory\n"\
                    r"        add_subdirectory(apps/${child})" + "\n"\
                    r"    endif()" + "\n"\
                    r"endforeach()" + "\n"\
                    "#---------------------------------------------------------------------------------------"
        
        with open("CMakeLists.txt","w") as f:
            
            f.write(content)
            
    def _writeAppCMake(self, app: Tag):
        
        app_name = app.attrs["name"]
        
        content = f"set(APP_NAME {app_name})\n"
        content += r"set(APP_PATH ${CMAKE_CURRENT_SOURCE_DIR})" + "\n"
        content += r"file(GLOB_RECURSE SOURCES ${APP_PATH}/src/*.cpp)" + "\n"\
                    r"file(GLOB_RECURSE HEADERS ${APP_PATH}/include/*.h ${APP_PATH}/include/*.hpp)" + "\n"
        if app.attrs["type"] == "lib":
            lib_str = r"add_executable(${APP_NAME} {{type}} ${SOURCES} ${HEADERS})" + "\n"
            content += lib_str.format(type = app.attrs["lib_type"])
        else:
            content += r"add_executable(${APP_NAME} ${SOURCES} ${HEADERS})" + "\n"
            
        content += "# Specify the include directories\n"\
                    r"target_include_directories(${APP_NAME} PUBLIC ${APP_PATH}/include)" + "\n"
        
        lib_str = r"target_link_libraries(${APP_NAME}"
        
        for lib in app.findChildren("Library"):
            
            if len(lib.findChildren("Module")) == 0:
                #content+= f"find_package({lib.attrs['name']} REQUIRED)"+"\n"
                #content+= r"add_dependencies(${APP_NAME} " + lib.attrs["name"] + ")\n"
                content+= r"target_link_libraries(${APP_NAME} " + lib.attrs["access"] + " " + lib.attrs["name"]+")\n"
            else:
                #find_package_base = f"find_package({lib.attrs['name']} REQUIRED COMPONENTS"
                #add_dependencies_base = r"add_dependencies(${APP_NAME}"
                link_lib_base = r"target_link_libraries(${APP_NAME} "
                for module in lib.findChildren("Module"):
                    #find_package_base+=" "+lib.attrs["name"]+"::"+module.attrs["name"]
                    #add_dependencies_base+=" "+lib.attrs["name"]+"::"+module.attrs["name"]
                    link_lib_base+=" "+lib.attrs["access"] + " " + lib.attrs["name"]+"::"+module.attrs["name"]
                #find_package_base+=")\n"
                #add_dependencies_base+=")\n"
                link_lib_base+=")\n"
                #content+=find_package_base+add_dependencies_base+link_lib_base
                content+=link_lib_base
        
        content += "# Install the app\n"\
                    r"install(TARGETS ${APP_NAME} DESTINATION bin)" + "\n"\
                    "# Install the header files\n"\
                    r"install(DIRECTORY include/ DESTINATION include)" + "\n" 
                    
        with open("apps/"+app_name+"/CMakeLists.txt","w") as f:
            f.write(content)