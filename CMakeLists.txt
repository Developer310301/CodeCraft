cmake_minimum_required(VERSION 3.10)
set(PROJECT_NAME ProjectName)
set(PROJECT_VERSION 1.0)

project(Builder)

# Check if CMAKE_INSTALL_PREFIX is set
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    message(FATAL_ERROR "CMAKE_INSTALL_PREFIX is not set, please specify a directory using -DCMAKE_INSTALL_PREFIX=<dir>")
endif()

# Set the install prefix
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME})

#--------------------------- Set Binary Output Directories --------------------------
# Set the output directory for the build executables
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${CMAKE_BUILD_TYPE}/bin)
# Set the output directory for the build libraries
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${CMAKE_BUILD_TYPE}/lib)
# Set the output directory for the build libraries
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${CMAKE_BUILD_TYPE}/lib)

#--------------------------- Include the core library --------------------------------
add_subdirectory(core)

#--------------------------- Include the applications---------------------------------
# Get all directories inside the 'apps' directory
file(GLOB children RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/apps ${CMAKE_CURRENT_SOURCE_DIR}/apps/*)

# Loop over the directories
foreach(child ${children})
    # Check if it's a directory
    if(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/apps/${child})
        # Add the directory
        add_subdirectory(apps/${child})
    endif()
endforeach()
#---------------------------------------------------------------------------------------
