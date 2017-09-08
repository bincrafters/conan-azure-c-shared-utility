import platform
from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username=os.getenv("CONAN_USERNAME"), channel=os.getenv("CONAN_CHANNEL"))
    builder.add_common_builds(shared_option_name="azure-c-shared-utility:shared", pure_c=True)
    # Skip static library
    if platform.system() == "Linux":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if options["azure-c-shared-utility:shared"] and settings["build_type"] == "Release":
                 filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds
    builder.run()
