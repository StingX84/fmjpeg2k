cmake_minimum_required(VERSION 3.12)

set (fmjpeg2k_VERSION_MAJOR 1)
set (fmjpeg2k_VERSION_MINOR 0)
set (fmjpeg2k_VERSION_BUILD 3)
set(fmjpeg2k_VERSION "${fmjpeg2k_VERSION_MAJOR}.${fmjpeg2k_VERSION_MINOR}.${fmjpeg2k_VERSION_BUILD}")

project(fmjpeg2k LANGUAGES CXX VERSION "${fmjpeg2k_VERSION}")
if(NOT CMAKE_CXX_STANDARD)
	set (CMAKE_CXX_STANDARD 17)
	if (MSVC) # Force MSVC to return actual C++ version from "__cplusplus" macro
		add_compile_options(/Zc:__cplusplus)
	endif ()
endif()

if(CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
	### Warn if not an out-of-source builds
	if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)
		set(lines
				"You are building in-place. If that is not what you intended to "
				"do, you can clean the source directory with:\n"
				"rm -r CMakeCache.txt CMakeFiles/ cmake_uninstall.cmake fmjpeg2kConfig.cmake "
				"fmjpeg2konfigVersion.cmake\n")
		message(AUTHOR_WARNING ${lines})
	endif()

	set(fmjpeg2k_MASTER_PROJECT ON)
else()
	set(fmjpeg2k_MASTER_PROJECT OFF)

	if(NOT fmjpeg2k_FIND_QUIETLY)
		message(STATUS "Using fmjpeg2k v${fmjpeg2k_VERSION}")
	endif()
endif()

option(fmjpeg2k_CREATE_INSTALL_RULES "Create installation rules" ${fmjpeg2k_MASTER_PROJECT})
option(fmjpeg2k_BUILD_SHARED_LIBS "Build fmjpeg2k shared library and link executables against it." ${fmjpeg2k_MASTER_PROJECT})
option(fmjpeg2k_BUILD_APPS "Build fmjpeg2k applications." ${fmjpeg2k_MASTER_PROJECT})


# ---------------------------------------------------------------------------
# Check whether all dependencies are present
# ---------------------------------------------------------------------------
if (NOT TARGET DCMTK::dcmimage)
	find_package(DCMTK REQUIRED COMPONENTS DCMTK::dcmimage)
endif()

if (NOT TARGET openjp2)
	find_package(OpenJPEG REQUIRED)
endif()

# ---------------------------------------------------------------------------
# Declare a library
# ---------------------------------------------------------------------------

if (fmjpeg2k_BUILD_SHARED_LIBS)
	set(BUILD_SHARED_LIBS ON)
else ()
	set(BUILD_SHARED_LIBS OFF)
endif()

set(fmjpeg2k_HEADERS
		include/fmjpeg2k/djcodecd.h
		include/fmjpeg2k/djcodece.h
		include/fmjpeg2k/djcparam.h
		include/fmjpeg2k/djdecode.h
		include/fmjpeg2k/djencode.h
		include/fmjpeg2k/djerror.h
		include/fmjpeg2k/djlsutil.h
		include/fmjpeg2k/djrparam.h
		include/fmjpeg2k/dldefine.h
		include/fmjpeg2k/memory_file.h
)

set(fmjpeg2k_SRCS
		djcodecd.cc
		djcodece.cc
		djcparam.cc
		djdecode.cc
		djencode.cc
		djrparam.cc
		djutils.cc
		memory_file.cpp
)

add_library(fmjpeg2k ${fmjpeg2k_HEADERS} ${fmjpeg2k_SRCS})
set(fmjpeg2k_LIBRARY_NAME fmjpeg2k)

target_link_libraries(fmjpeg2k PUBLIC DCMTK::dcmimage openjp2)
if (NOT BUILD_SHARED_LIBS)
	target_compile_definitions(fmjpeg2k PUBLIC fmjpeg2k_STATIC)
endif()
target_compile_definitions(fmjpeg2k PUBLIC fmjpeg2k_EXPORTS)

if(WIN32)
	target_compile_definitions(fmjpeg2k PRIVATE _BIND_TO_CURRENT_VCLIBS_VERSION=1)
endif()

# Cache variable so this can be used in parent projects
set(fmjpeg2k_INCLUDE_DIR
		"${CMAKE_CURRENT_LIST_DIR}/include"
		CACHE INTERNAL "Directory where fmjpeg2k headers are located")

target_include_directories(fmjpeg2k
	PUBLIC
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
		$<BUILD_INTERFACE:${fmjpeg2k_INCLUDE_DIR}>
)

set_target_properties(fmjpeg2k PROPERTIES
	VERSION ${fmjpeg2k_VERSION}
	SOVERSION 1
	INTERFACE_fmjpeg2k_MAJOR_VERSION 1
	COMPATIBLE_INTERFACE_STRING fmjpeg2k_MAJOR_VERSION
)

# ---------------------------------------------------------------------------
# Applications definition
# ---------------------------------------------------------------------------

if (fmjpeg2k_BUILD_APPS)
	add_executable(dcmcjp2k dcmcjp2k.cc)
	target_link_libraries(dcmcjp2k fmjpeg2k)

	add_executable(dcmdjp2k dcmdjp2k.cc)
	target_link_libraries(dcmdjp2k fmjpeg2k)
endif()

# ---------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------

install(TARGETS fmjpeg2k EXPORT fmjpeg2kTargets
		LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
		ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
		RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(EXPORT fmjpeg2kTargets
		DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/fmjpeg2k
)

if(fmjpeg2k_CREATE_INSTALL_RULES AND NOT CMAKE_SKIP_INSTALL_RULES)
	# Standard includes
	include(GNUInstallDirs)
	include(CMakePackageConfigHelpers)
	include(CMakeDependentOption)

	include(GenerateExportHeader)
	generate_export_header(fmjpeg2k)

	if (FMJPEG2K_BUILD_APPS)
		install(TARGETS dcmdjp2k dcmcjp2k EXPORT fmjpeg2kTargets
			RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
		)
	endif()

	include(CMakePackageConfigHelpers)
	write_basic_package_version_file(
		"${CMAKE_CURRENT_BINARY_DIR}/fmjpeg2k/fmjpeg2kConfigVersion.cmake"
		VERSION ${fmjpeg2k_VERSION}
		COMPATIBILITY AnyNewerVersion
	)

	export(TARGETS fmjpeg2k
		FILE "${CMAKE_CURRENT_BINARY_DIR}/fmjpeg2kExports.cmake"
	)
	configure_file( ${PROJECT_SOURCE_DIR}/cmake/fmjpeg2kConfig.cmake.in
		${CMAKE_CURRENT_BINARY_DIR}/fmjpeg2kConfig.cmake
		@ONLY
	)

	install(
		FILES
			${fmjpeg2k_HEADERS}
		DESTINATION
			include/fmjpeg2k
		COMPONENT
			Devel
	)

	install(
		FILES
			"${CMAKE_CURRENT_BINARY_DIR}/fmjpeg2kConfig.cmake"
			"${CMAKE_CURRENT_BINARY_DIR}/fmjpeg2k/fmjpeg2kConfigVersion.cmake"
		DESTINATION
			lib/cmake/fmjpeg2k
		COMPONENT
			Devel
	)
endif ()
