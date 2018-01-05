#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class AzureCSharedUtilityConan(ConanFile):
    name = "azure-c-shared-utility"
    version = "1.0.49"
    release_date = "2017-12-14"
    url = "https://github.com/bincrafters/conan-azure-c-shared-utility"
    description = "Azure C SDKs common code"
    license = "MIT"
    exports = ["LICENSE.md", "azure_c_shared_utilityConfig.cmake"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    
    
    def source(self):
        source_url = "https://github.com/Azure/azure-c-shared-utility"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.release_date))
        extracted_dir = self.name + "-" + self.release_date
        os.rename(extracted_dir, self.source_subfolder)
        
    def requirements(self):
        if self.settings.compiler != "Visual Studio":
            self.requires.add("OpenSSL/[>=1.0.2l]@conan/stable")
            self.requires.add("libcurl/[>=7.56.1]@bincrafters/stable")
            self.requires.add("libuuid/[>=1.0.3]@bincrafters/stable")

    def build(self):
        cmake = CMake(self, parallel=False)
        cmake.definitions["skip_samples"] = True
        cmake.definitions["build_as_dynamic"] = self.options.shared
        cmake.configure()
        cmake.build()

    def package(self):
        configs_folder = os.path.join(self.source_subfolder, "configs")
        include_folder = os.path.join(self.source_subfolder, "inc")
        self.copy(pattern="LICENSE", dst=".", src=".")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="azure_c_shared_utilityConfig.cmake", dst="res", src=".")
        self.copy(pattern="azure_c_shared_utilityFunctions.cmake", dst="res", src=configs_folder)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("curl")
            self.cpp_info.libs.append("uuid")
            self.cpp_info.libs.append("m")
