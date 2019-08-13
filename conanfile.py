import os

from conans import CMake, ConanFile, tools


class JsonSchemaValidatorConan(ConanFile):
    name = "json-schema-validator"
    version = "2.0.0"
    description = "JSON schema validator for JSON for Modern C++"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("json",)
    url = "https://github.com/rhololkeolke/conan-json-schema-validator"
    homepage = "https://github.com/pboettch/json-schema-validator"
    author = "Devin Schwab <dschwab@andrew.cmu.edu>"
    license = (
        "MIT"
    )  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]  # Packages the license for the
    exports_sources = ["CMakeLists.txt"]
    # conanfile.py
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    requires = "jsonformoderncpp/3.7.0@vthiery/stable"

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/pboettch/json-schema-validator"
        tools.get(
            "{0}/archive/{1}.tar.gz".format(source_url, self.version),
            sha256="ca8e4ca5a88c49ea52b5f5c2a08a293dbf02b2fc66cb8c09d4cce5810ee98b57",
        )
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
