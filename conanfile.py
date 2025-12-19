import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import (copy, rmdir)

required_conan_version = ">=2.12.0"

class Fmjpeg2kConan(ConanFile):
    name = "fmjpeg2k"
    version = "1.1.0"
    url = "https://github.com/StingX84/fmjpeg2k"
    homepage = "https://github.com/StingX84/fmjpeg2k"
    description = "JPEG2000 codec for DCMTK based on openjpeg"
    license = "Apache-2.0"
    topics = ("jpeg2000", "dcmtk")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_apps": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_apps": False,
    }

    exports_sources = "CMakeLists.txt", "*.cc", "*.cpp", "include/*", "cmake/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("dcmtk/[>=3.6.8]", transitive_headers=True, transitive_libs=True)
        self.requires("openjpeg/[>=2.5.0]")

    def validate(self):
        dcmtk_options = self.dependencies["dcmtk"].options
        if not bool(dcmtk_options.shared) and bool(self.options.shared):
            raise ConanInvalidConfiguration(
                "fmjpeg2k cannot be built as shared library when DCMTK is built as static library"
            )

    def generate(self):
        tc = CMakeDeps(self)
        tc.generate()
        tc = CMakeToolchain(self)
        tc.variables["fmjpeg2k_BUILD_SHARED_LIBS"] = bool(self.options.shared)
        tc.variables["fmjpeg2k_BUILD_APPS"] = bool(self.options.build_apps)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "fmjpeg2k")
        self.cpp_info.set_property("cmake_target_name", "fmjpeg2k::fmjpeg2k")
        self.cpp_info.requires = ["dcmtk::dcmimage", "openjpeg::openjpeg"]

        self.cpp_info.libs = ["fmjpeg2k"]
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.defines.append("fmjpeg2k_SHARED")
