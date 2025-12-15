"""
Script to clean up unused documentation and batch files from the backend directory.
This will delete redundant documentation files and old batch scripts.
"""

import os
import shutil
from pathlib import Path

# Get the backend directory
BACKEND_DIR = Path(__file__).parent

# Files to delete - Documentation files
DOCS_TO_DELETE = [
    "API_DOCUMENTATION.md",
    "BACKEND_EXPLANATION.md",
    "FLASK_BACKEND_SUMMARY.md",
    "LAN_FIX_SUMMARY.md",
    "LAN_SETUP_GUIDE.md",
    "ORCHESTRATION_GUIDE.md",
    "QUICKSTART.md",
    "QUICK_REFERENCE.md",
    "QUICK_START.md",
    "STARTUP_GUIDE.md",
    "SUMMARY.md",
    "SYSTEM_SUMMARY.md",
    "TESTING_GUIDE.md",
    "WHICH_FILE_TO_USE.md",
]

# Batch files to delete
BATCH_FILES_TO_DELETE = [
    "configure_firewall.bat",
    "quick_start.bat",
    "start_all.bat.OLD",
    "start_all_servers.bat",
    "start_flask.bat",
    "start_lan_backend.bat",
    "start_system.bat",
    "test_endpoints.bat",
]

# Files to keep
KEEP_FILES = [
    "README.md",  # Main documentation
    "INSTALLATION_GUIDE.md",  # Important for setup
]

def delete_files(file_list, category_name):
    """Delete files from the list and report results."""
    deleted = []
    not_found = []
    errors = []
    
    print(f"\n{'='*60}")
    print(f"Deleting {category_name}...")
    print(f"{'='*60}\n")
    
    for filename in file_list:
        file_path = BACKEND_DIR / filename
        
        try:
            if file_path.exists():
                # Get file size before deletion
                size = file_path.stat().st_size
                size_kb = size / 1024
                
                # Delete the file
                file_path.unlink()
                deleted.append((filename, size_kb))
                print(f"✅ Deleted: {filename} ({size_kb:.1f} KB)")
            else:
                not_found.append(filename)
                print(f"⚠️  Not found: {filename}")
        except Exception as e:
            errors.append((filename, str(e)))
            print(f"❌ Error deleting {filename}: {e}")
    
    return deleted, not_found, errors

def main():
    print("\n" + "="*60)
    print("BACKEND CLEANUP SCRIPT")
    print("="*60)
    print("\nThis script will delete unused documentation and batch files.")
    print("\nFiles that will be KEPT:")
    for file in KEEP_FILES:
        print(f"  ✓ {file}")
    
    print(f"\nTotal files to delete: {len(DOCS_TO_DELETE) + len(BATCH_FILES_TO_DELETE)}")
    print(f"  - Documentation files: {len(DOCS_TO_DELETE)}")
    print(f"  - Batch files: {len(BATCH_FILES_TO_DELETE)}")
    
    # Delete documentation files
    docs_deleted, docs_not_found, docs_errors = delete_files(DOCS_TO_DELETE, "Documentation Files")
    
    # Delete batch files
    batch_deleted, batch_not_found, batch_errors = delete_files(BATCH_FILES_TO_DELETE, "Batch Files")
    
    # Summary
    print("\n" + "="*60)
    print("CLEANUP SUMMARY")
    print("="*60)
    
    total_deleted = len(docs_deleted) + len(batch_deleted)
    total_size = sum(size for _, size in docs_deleted) + sum(size for _, size in batch_deleted)
    
    print(f"\n✅ Successfully deleted: {total_deleted} files ({total_size:.1f} KB)")
    print(f"   - Documentation: {len(docs_deleted)} files")
    print(f"   - Batch files: {len(batch_deleted)} files")
    
    if docs_not_found or batch_not_found:
        total_not_found = len(docs_not_found) + len(batch_not_found)
        print(f"\n⚠️  Files not found: {total_not_found}")
    
    if docs_errors or batch_errors:
        total_errors = len(docs_errors) + len(batch_errors)
        print(f"\n❌ Errors encountered: {total_errors}")
        for filename, error in docs_errors + batch_errors:
            print(f"   - {filename}: {error}")
    
    print("\n" + "="*60)
    print("Cleanup completed!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
