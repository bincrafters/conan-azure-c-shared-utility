from conans import ConanFile, CMake, os


class AzureCSharedUtilityConan(ConanFile):
    name = "Azure-C-Shared-Utility"
    version = "1.0.41"
    generators = "cmake" 
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-azure-c-shared-utility"
    source_url = "https://github.com/Azure/azure-c-shared-utility"
    git_tag = "2017-08-11"
    description = "Azure C SDKs common code"
    license = "https://github.com/Azure/azure-c-shared-utility/blob/master/LICENSE"
    lib_short_name = "azure-c-shared-utility"
        
    def source(self):
        self.run("git clone --depth=1 --branch={0} {1}.git"
                .format(self.git_tag, self.source_url)) 

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.lib_short_name, build_dir="./")
        cmake.build()
        
    def package(self):
        include_dir = os.path.join(
            self.lib_short_name, "inc", self.lib_short_name.replace("-","_"))
            
        self.copy(pattern="*", dst="include", src=include_dir)
        self.copy(pattern="*.lib", dst="lib", src="")

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()

