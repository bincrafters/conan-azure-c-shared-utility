from os import path
from conans import ConanFile, CMake, tools


class AzureCSharedUtilityConan(ConanFile):
    name = "Azure-C-Shared-Utility"
    version = "1.0.46"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-c-shared-utility"
    description = "Azure C SDKs common code"
    license = "https://github.com/Azure/azure-c-shared-utility/blob/master/LICENSE"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    lib_short_name = "azure_c_shared_utility"
    release_date = "2017-10-20"
    release_name = "%s-%s" % (name.lower(), release_date)
    exports = ["LICENSE", "azure_c_shared_utilityConfig.cmake"]

    def source(self):
        source_url = "https://github.com/Azure/azure-c-shared-utility"
        tools.get("%s/archive/%s.tar.gz" % (source_url, self.release_date))

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.requires.add("OpenSSL/1.0.2l@conan/stable")
            self.requires.add("libcurl/7.50.3@lasote/stable")
            self.requires.add("zlib/1.2.11@conan/stable", override=True)
        if self.settings.os == "Linux":
            self.requires.add("libuuid/1.0.3@%s/stable" % self.user)

    def build(self):
        conan_magic_lines = '''project(%s)
    include(../conanbuildinfo.cmake)
    conan_basic_setup()
    ''' % self.lib_short_name
        cmake_file = "%s/CMakeLists.txt" % self.release_name
        tools.replace_in_file(cmake_file, "project(%s)" % self.lib_short_name, conan_magic_lines)
        conan_magic_lines = "target_link_libraries(aziotsharedutil ${aziotsharedutil_target_libs} ${CONAN_LIBS})"
        tools.replace_in_file(cmake_file, "target_link_libraries(aziotsharedutil ${aziotsharedutil_target_libs})", conan_magic_lines)
        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["skip_samples"] = True
        cmake.definitions["build_as_dynamic"] = self.settings.os == "Windows" and self.options.shared
        cmake.configure(source_dir=self.release_name)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst=".", src=".")
        self.copy(pattern="*", dst="include", src=path.join(self.release_name, "inc"))
        self.copy(pattern="azure_c_shared_utilityConfig.cmake", dst=path.join("res", "deps", "c-utility", "configs"), src=".")
        self.copy(pattern="azure_c_shared_utilityFunctions.cmake", dst=path.join("res", "deps", "c-utility", "configs"), src=path.join(self.release_name, "configs"))
        self.copy(pattern="azure_iot_build_rules.cmake", dst=path.join("res", "deps", "c-utility", "configs"), src=path.join(self.release_name, "configs"))
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("wsock32")
            self.cpp_info.libs.append("ws2_32")
            self.cpp_info.libs.append("Secur32")
            self.cpp_info.libs.append("Ncrypt")
            self.cpp_info.libs.append("Crypt32")
