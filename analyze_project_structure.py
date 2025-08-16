import os
import glob
from pathlib import Path

def analyze_project_structure():
    """
    Analyze the current project structure and compare with expected structure
    """
    
    # Base path from your folder
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"
    
    if not os.path.exists(base_path):
        print(f"❌ Base path does not exist: {base_path}")
        return
    
    print("=" * 80)
    print("📁 REDDIT MESSAGE MANAGER - PROJECT STRUCTURE ANALYSIS")
    print("=" * 80)
    print(f"📍 Analyzing: {base_path}")
    print()
    
    # Expected project structure with status
    expected_structure = {
        "src/main/java/com/anuj/redditmessagemanager/": {
            "type": "folder",
            "critical": True,
            "files": [
                "RedditMessageManagerApplication.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/config/": {
            "type": "folder", 
            "critical": True,
            "files": [
                "SecurityConfig.java",
                "WebSocketConfig.java",
                "DatabaseConfig.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/controller/": {
            "type": "folder",
            "critical": True, 
            "files": [
                "AuthController.java",
                "ChatController.java", 
                "UserController.java",
                "MessageController.java",
                "SearchController.java",
                "ExportController.java",
                "BlockController.java",
                "UploadController.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/entity/": {
            "type": "folder",
            "critical": True,
            "files": [
                "User.java",
                "Chat.java", 
                "Message.java",
                "BlockedUser.java",
                "ExportRequest.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/repository/": {
            "type": "folder",
            "critical": True,
            "files": [
                "UserRepository.java",
                "ChatRepository.java",
                "MessageRepository.java", 
                "BlockedUserRepository.java",
                "ExportRequestRepository.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/service/": {
            "type": "folder",
            "critical": True,
            "files": [
                "UserService.java",
                "ChatService.java",
                "MessageService.java",
                "SearchService.java",
                "ExportService.java",
                "BlockService.java", 
                "UploadService.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/websocket/": {
            "type": "folder",
            "critical": True,
            "files": [
                "ChatWebSocketHandler.java"
            ]
        },
        "src/main/java/com/anuj/redditmessagemanager/dto/": {
            "type": "folder",
            "critical": True,
            "files": [
                "ChatDTO.java",
                "MessageDTO.java",
                "UserDTO.java",
                "SearchResultDTO.java",
                "ExportRequestDTO.java"
            ]
        },
        "src/main/resources/": {
            "type": "folder",
            "critical": True,
            "files": [
                "application.properties"
            ]
        },
        "src/main/resources/static/css/": {
            "type": "folder",
            "critical": False,
            "files": [
                "main.css",
                "chat.css",
                "sidebar.css", 
                "modal.css",
                "animations.css",
                "responsive.css"
            ]
        },
        "src/main/resources/static/js/": {
            "type": "folder",
            "critical": False,
            "files": [
                "main.js",
                "chat.js",
                "websocket.js",
                "search.js",
                "filters.js",
                "autocomplete.js",
                "bulk-actions.js",
                "export.js",
                "image-handler.js",
                "utils.js"
            ]
        },
        "src/main/resources/static/images/": {
            "type": "folder",
            "critical": False,
            "files": [
                "logo.png",
                "default-avatar.png",
                "favicon.ico"
            ]
        },
        "src/main/resources/templates/": {
            "type": "folder",
            "critical": True,
            "files": [
                "index.html",
                "login.html",
                "error.html"
            ]
        },
        "src/main/resources/templates/modals/": {
            "type": "folder",
            "critical": False,
            "files": [
                "new-chat-modal.html",
                "settings-modal.html",
                "export-modal.html",
                "image-viewer-modal.html",
                "confirmation-modal.html",
                "user-profile-modal.html"
            ]
        }
    }
    
    # Root files
    root_files = ["pom.xml", "README.md", ".gitignore"]
    
    # Analyze actual structure
    found_files = []
    missing_critical = []
    missing_non_critical = []
    existing_count = 0
    total_count = 0
    
    def scan_directory(directory):
        """Recursively scan directory and return all files"""
        files = []
        if os.path.exists(directory):
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    rel_path = os.path.relpath(os.path.join(root, filename), base_path)
                    files.append(rel_path.replace('\\', '/'))
        return files
    
    # Get all existing files
    all_existing_files = scan_directory(base_path)
    
    print("🔍 SCANNING CURRENT PROJECT STRUCTURE...")
    print()
    
    # Check each expected folder and file
    for folder_path, folder_info in expected_structure.items():
        full_folder_path = os.path.join(base_path, folder_path.replace('/', os.sep))
        folder_exists = os.path.exists(full_folder_path)
        
        print(f"📁 {folder_path}")
        
        if folder_exists:
            print(f"   ✅ Folder exists")
        else:
            print(f"   ❌ Folder missing")
            if folder_info["critical"]:
                missing_critical.append(f"Folder: {folder_path}")
        
        # Check files in folder
        for filename in folder_info["files"]:
            total_count += 1
            file_path = folder_path + filename
            full_file_path = os.path.join(base_path, file_path.replace('/', os.sep))
            
            if os.path.exists(full_file_path):
                print(f"   ✅ {filename}")
                existing_count += 1
                found_files.append(file_path)
            else:
                print(f"   ❌ {filename}")
                if folder_info["critical"]:
                    missing_critical.append(file_path)
                else:
                    missing_non_critical.append(file_path)
        print()
    
    # Check root files
    print("📁 ROOT FILES")
    for filename in root_files:
        total_count += 1
        full_file_path = os.path.join(base_path, filename)
        if os.path.exists(full_file_path):
            print(f"   ✅ {filename}")
            existing_count += 1
        else:
            print(f"   ❌ {filename}")
            missing_critical.append(filename)
    
    print()
    print("=" * 80)
    print("📊 PROJECT ANALYSIS SUMMARY")
    print("=" * 80)
    
    completion_percentage = (existing_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"📈 Project Completion: {existing_count}/{total_count} files ({completion_percentage:.1f}%)")
    print()
    
    if completion_percentage >= 80:
        print("🎉 Great! Your project is mostly complete!")
    elif completion_percentage >= 50:
        print("👍 Good progress! About halfway there.")
    else:
        print("🚀 Getting started! Lots to build.")
    
    print()
    print("🔥 CRITICAL MISSING FILES (Required to run):")
    if missing_critical:
        for item in missing_critical:
            print(f"   ❌ {item}")
    else:
        print("   ✅ All critical files present!")
    
    print()
    print("📝 NON-CRITICAL MISSING FILES (Nice to have):")
    if missing_non_critical:
        for item in missing_non_critical[:10]:  # Show first 10
            print(f"   ⚠️ {item}")
        if len(missing_non_critical) > 10:
            print(f"   ... and {len(missing_non_critical) - 10} more")
    else:
        print("   ✅ All non-critical files present!")
    
    print()
    print("🎯 NEXT STEPS:")
    
    if missing_critical:
        print("1. Create critical missing files first")
        print("2. Focus on backend Java files for core functionality")
        print("3. Add main HTML templates for the UI")
        print("4. Configure application.properties and pom.xml")
    else:
        print("1. Test your application")
        print("2. Add remaining frontend features") 
        print("3. Write tests")
        print("4. Deploy and enjoy!")
    
    print()
    print("💡 UNEXPECTED/EXTRA FILES FOUND:")
    unexpected_files = []
    expected_files_set = set()
    
    # Build expected files set
    for folder_path, folder_info in expected_structure.items():
        for filename in folder_info["files"]:
            expected_files_set.add((folder_path + filename).replace('/', os.sep))
    
    for filename in root_files:
        expected_files_set.add(filename)
    
    # Find unexpected files
    for file_path in all_existing_files:
        normalized_path = file_path.replace('/', os.sep)
        if not any(normalized_path.endswith(expected.replace('/', os.sep)) for expected in expected_files_set):
            # Skip common IDE/build files
            if not any(skip in file_path.lower() for skip in ['.class', 'target/', '.idea/', '.git/', '__pycache__']):
                unexpected_files.append(file_path)
    
    if unexpected_files:
        for file_path in unexpected_files[:5]:  # Show first 5
            print(f"   📄 {file_path}")
        if len(unexpected_files) > 5:
            print(f"   ... and {len(unexpected_files) - 5} more files")
    else:
        print("   ✅ No unexpected files found")
    
    print()
    print("=" * 80)
    
    # Generate creation script suggestions
    if missing_critical:
        print("💻 RECOMMENDED SCRIPTS TO RUN:")
        if any("controller" in item.lower() for item in missing_critical):
            print("   python create_java_controllers.py")
        if any("service" in item.lower() for item in missing_critical):
            print("   python create_java_services.py") 
        if any("entity" in item.lower() for item in missing_critical):
            print("   python create_java_entities.py")
        if any("html" in item.lower() for item in missing_critical):
            print("   python create_main_templates.py")
        if "pom.xml" in missing_critical:
            print("   python create_project_config.py")

def main():
    analyze_project_structure()

if __name__ == "__main__":
    main()