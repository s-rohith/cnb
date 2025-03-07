import toml
import os
import requests
import hashlib

def download_and_verify(uri, sha256sum, output_dir):
    filename = os.path.join(output_dir, uri.split("/")[-1])
    response = requests.get(uri, stream=True)
    response.raise_for_status()

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Verify SHA256
    with open(filename, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    if file_hash != sha256sum:
        raise ValueError(f"SHA256 mismatch for {uri}: expected {sha256sum}, got {file_hash}")
    return filename

# Directory with buildpack.toml files
buildpacks_dir = "./buildpacks"
output_dir = "./downloads"
os.makedirs(output_dir, exist_ok=True)

for root, _, files in os.walk(buildpacks_dir):
    for file in files:
        if file == "buildpack.toml":
            with open(os.path.join(root, file), "r") as f:
                data = toml.load(f)
                # Extract dependencies from metadata
                for dep in data.get("metadata", {}).get("dependencies", []):
                    uri = dep.get("uri")
                    sha256sum = dep.get("sha256")
                    if uri and sha256sum:
                        print(f"Downloading {uri}...")
                        downloaded_file = download_and_verify(uri, sha256sum, output_dir)
                        print(f"Downloaded and verified: {downloaded_file}")
