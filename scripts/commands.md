### Steps

1. Pull Paketo Builder Image
   ```sh
   docker pull paketobuildpacks/builder-jammy-base:latest
   ```
1. Run copy script

   Run a temporary container to copy the buildpack metadata from the image. Paketo builders store buildpack data under /cnb/buildpacks/

   This copies all buildpack directories (e.g., paketo-buildpacks_java, paketo-buildpacks_python) to ./buildpacks, each containing a buildpack.toml.

   ```sh
   chmod +x copy_script.sh
   sh copy_script.sh
   ```

1. Run Download depedency script

   The buildpack.toml files in this builder image contain dependency metadata under the metadata.dependencies section.

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install toml requests
   ### pipx runs Python applications in isolated environments without requiring manual virtual environment management.
   # pipx run --spec toml --spec requests python download_deps.py
   python3 download_deps.py
   ```

   This script:

   - Walks through ./buildpacks to find all buildpack.toml files.
   - Parses each file for uri and sha256 in the metadata.dependencies section.
   - Downloads the files and verifies their integrity using SHA256 sums.
