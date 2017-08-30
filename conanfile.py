from os import path
from conans import ConanFile, CMake, tools


class AzureCSharedUtilityConan(ConanFile):
    name = "Azure-C-Shared-Utility"
    version = "1.0.41"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-c-shared-utility"
    license = "https://github.com/Azure/azure-c-shared-utility/blob/master/LICENSE"
    description = "Azure C SDKs common code"
    release_name = "%s-2017-08-11" % name.lower()
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = ["LICENSE", "azure_c_shared_utilityConfig.cmake"]

    def source(self):
        tools.get("https://github.com/Azure/azure-c-shared-utility/archive/2017-08-11.tar.gz")

    def configure(self):
        # TODO: static library fails on Linux
        if self.settings.os == "Linux":
            self.options.shared = True

    def requirements(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.requires.add("OpenSSL/1.0.2l@conan/stable")

    def system_requirements(self):
        # libcurl and uuid are required on Linux
        if self.settings.os == "Linux":
            package_tool = tools.SystemPackageTool()
            package_tool.install(packages="libcurl4-gnutls-dev uuid-dev pkg-config", update=True)

    def build(self):
        conan_magic_lines = '''project(azure_c_shared_utility)
    include(../conanbuildinfo.cmake)
    conan_basic_setup()
    '''
        tools.replace_in_file("%s/CMakeLists.txt" % self.release_name, "project(azure_c_shared_utility)", conan_magic_lines)
        cmake = CMake(self)
        cmake.definitions["skip_samples"] = True
        cmake.definitions["build_as_dynamic"] = self.options.shared
        cmake.configure(source_dir=self.release_name)
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst=".", src=".")
        self.copy(pattern="*", dst="include", src=path.join(self.release_name, "inc"))
        self.copy(pattern="azure_c_shared_utilityConfig.cmake", dst="res", src=".")
        self.copy(pattern="azure_c_shared_utilityFunctions.cmake", dst="res", src=path.join(self.release_name, "configs"))
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("curl")
            self.cpp_info.libs.append("uuid")
