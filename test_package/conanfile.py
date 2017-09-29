from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        
    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")        
        
    def test(self):
        os.chdir("bin")
        try:
            self.run("ulimit -c unlimited")
            self.run("./test_package")
        except:
            self.run('gdb --batch --quiet -ex "thread apply all bt full" -ex "quit" test_package  core')
