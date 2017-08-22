find_path(azure_c_shared_utility_INCLUDE_DIR NAMES azure_c_shared_utility/shared_util_options.h PATHS ${CONAN_INCLUDE_DIRS_AZURE-C-SHARED-UTILITY} NO_CMAKE_FIND_ROOT_PATH)
find_library(azure_c_shared_utility_LIBRARY NAMES ${CONAN_LIBS_AZURE-C-SHARED-UTILITY} PATHS ${CONAN_LIB_DIRS_AZURE-C-SHARED-UTILITY} NO_CMAKE_FIND_ROOT_PATH)

MESSAGE("** azure_c_shared_utility ALREADY FOUND BY CONAN!")
SET(azure_c_shared_utility_FOUND TRUE)
MESSAGE("** FOUND azure_c_shared_utility: ${azure_c_shared_utility_LIBRARY}")
MESSAGE("** FOUND azure_c_shared_utility INCLUDE: ${azure_c_shared_utility_INCLUDE_DIR}")

set(azure_c_shared_utility_INCLUDE_DIR ${azure_c_shared_utility_INCLUDE_DIR})
set(azure_c_shared_utility_LIBRARIES ${azure_c_shared_utility_LIBRARY})

mark_as_advanced(azure_c_shared_utility_LIBRARY azure_c_shared_utility_INCLUDE_DIR)

set(azure_c_shared_utility_MAJOR_VERSION "1")
set(azure_c_shared_utility_MINOR_VERSION "0")
set(azure_c_shared_utility_PATCH_VERSION "41")
