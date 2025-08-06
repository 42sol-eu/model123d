from pathlib import Path
import zipfile

def extract_3mf_files(source_dir, dest_dir):
    # Convert to Path objects for consistent handling
    source_dir = Path(source_dir)
    dest_dir = Path(dest_dir)
    
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        
    for file_path in source_dir.glob("*.3mf"):
        # Create destination directory without the .3mf extension
        dst_path = dest_dir / file_path.stem  # stem removes the extension
        dst_path.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(dst_path)
        print(f"Extracted: {file_path.name} -> {dst_path}")

if __name__ == "__main__":
    source_directory = Path(__file__).parent / "_export"  # Change to your source directory if needed
    destination_directory = Path(__file__).parent / "./_extracted_3mf"
    if not destination_directory.exists():
        destination_directory.mkdir(parents=True, exist_ok=True)
    print(f"Extracting 3MF files from {source_directory} to {destination_directory}")
    extract_3mf_files(source_directory, destination_directory)