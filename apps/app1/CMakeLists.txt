set(APP_NAME App1)
set(APP_PATH ${CMAKE_CURRENT_SOURCE_DIR})
# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)

# Add all the .cpp files in the /src directory to the library
file(GLOB_RECURSE SOURCES ${APP_PATH}/src/*.cpp)
file(GLOB_RECURSE HEADERS ${APP_PATH}/include/*.h ${APP_PATH}/include/*.hpp)



# Create a library with the source files
add_executable(${APP_NAME} ${SOURCES} ${HEADERS})

add_dependencies(${APP_NAME} ProjectName)

# Specify the include directories
target_include_directories(${APP_NAME} PUBLIC ${APP_PATH}/include)
target_link_libraries(${APP_NAME} PRIVATE ProjectName)

# Install the library
install(TARGETS ${APP_NAME} DESTINATION bin)
# Install the header files
install(DIRECTORY include/ DESTINATION include)