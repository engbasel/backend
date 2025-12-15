#!/usr/bin/env python3
"""
Cleanup Script for VM Deployment
This script removes unnecessary files for VM deployment
"""

import os
import shutil
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent

# Files to delete (documentation)
DOCS_TO_DELETE = [
    "API_DOCUMENTATION.md",
    "BACKEND_EXPLANATION.md",
    "FLASK_BACKEND_SUMMARY.md",
    "INSTALLATION_GUIDE.md",
    "LAN_FIX_SUMMARY.md",
    "LAN_SETUP_GUIDE.md",
    "ORCHESTRATION_GUIDE.md",
    "QUICKSTART.md",
    "QUICK_REFERENCE.md",
    "QUICK_START.md",
    "README.md",
    "STARTUP_GUIDE.md",
    "SUMMARY.md",
    "SYSTEM_SUMMARY.md",
    "TESTING_GUIDE.md",
    "WHICH_FILE_TO_USE.md",
]

# Batch files to delete (Windows-specific)
BAT_FILES_TO_DELETE = [
    "configure_firewall.bat",
    "quick_start.bat",
    "start_all.bat.OLD",
    "start_all_servers.bat",
    "start_flask.bat",
    "start_lan_backend.bat",
    "start_system.bat",
    "test_endpoints.bat",
]

# Other files to delete
OTHER_FILES_TO_DELETE = [
    "package-lock.json",
    "config.json",
]

# Directories to delete
DIRS_TO_DELETE = [
    "routes",
]

def delete_files(file_list, description):
    """Delete files from the list"""
    print(f"\n🗑️  Deleting {description}...")
    deleted_count = 0
    for filename in file_list:
        file_path = BASE_DIR / filename
        if file_path.exists():
            try:
                os.remove(file_path)
                print(f"  ✅ Deleted: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ Error deleting {filename}: {e}")
        else:
            print(f"  ⚠️  Not found: {filename}")
    
    print(f"  📊 Deleted {deleted_count}/{len(file_list)} files")
    return deleted_count

def delete_directories(dir_list, description):
    """Delete directories from the list"""
    print(f"\n🗑️  Deleting {description}...")
    deleted_count = 0
    for dirname in dir_list:
        dir_path = BASE_DIR / dirname
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.rmtree(dir_path)
                print(f"  ✅ Deleted directory: {dirname}")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ Error deleting {dirname}: {e}")
        else:
            print(f"  ⚠️  Not found or not a directory: {dirname}")
    
    print(f"  📊 Deleted {deleted_count}/{len(dir_list)} directories")
    return deleted_count

def main():
    print("=" * 60)
    print("🧹 Backend Cleanup Script for VM Deployment")
    print("=" * 60)
    
    # Confirm with user
    print("\n⚠️  This will delete the following:")
    print(f"  - {len(DOCS_TO_DELETE)} documentation files")
    print(f"  - {len(BAT_FILES_TO_DELETE)} Windows batch files")
    print(f"  - {len(OTHER_FILES_TO_DELETE)} other unnecessary files")
    print(f"  - {len(DIRS_TO_DELETE)} empty/unused directories")
    
    response = input("\n❓ Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cleanup cancelled.")
        return
    
    total_deleted = 0
    
    # Delete documentation files
    total_deleted += delete_files(DOCS_TO_DELETE, "Documentation Files")
    
    # Delete batch files
    total_deleted += delete_files(BAT_FILES_TO_DELETE, "Windows Batch Files")
    
    # Delete other files
    total_deleted += delete_files(OTHER_FILES_TO_DELETE, "Other Unnecessary Files")
    
    # Delete directories
    total_deleted += delete_directories(DIRS_TO_DELETE, "Empty/Unused Directories")
    
    print("\n" + "=" * 60)
    print(f"✅ Cleanup Complete! Total items deleted: {total_deleted}")
    print("=" * 60)
    
    print("\n📝 Essential files remaining:")
    print("  ✅ run_system.py")
    print("  ✅ gateway.py")
    print("  ✅ requirements.txt")
    print("  ✅ .env")
    print("  ✅ flask_server/")
    print("  ✅ ai_services/")
    print("  ✅ uploads/")
    print("  ✅ data/")
    
    print("\n🚀 To run on VM:")
    print("  1. pip install -r requirements.txt")
    print("  2. python run_system.py")

if __name__ == "__main__":
    main()
