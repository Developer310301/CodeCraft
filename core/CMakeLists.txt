set(CORE_NAME ProjectName)
set(CORE_PATH ${CMAKE_CURRENT_SOURCE_DIR})

# Set the C++ standard
set(CMAKE_CXX_STANDARD 14)

# Add all the .cpp files in the /src directory to the library
file(GLOB_RECURSE SOURCES ${CORE_PATH}/src/*.cpp)
file(GLOB_RECURSE HEADERS ${CORE_PATH}/include/*.h ${CORE_PATH}/include/*.hpp)

# Create a library with the source files
add_library(${CORE_NAME} SHARED ${SOURCES} ${HEADERS})

# Specify the include directories
target_include_directories(${CORE_NAME} PUBLIC ${CORE_PATH}/include)

# Install the library
install(TARGETS ${CORE_NAME} DESTINATION lib)
# Install the header files
install(DIRECTORY include/ DESTINATION include)