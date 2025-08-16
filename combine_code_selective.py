import os
import fnmatch
from datetime import datetime

def combine_selective_code():
    """
    Combine only essential code files from the Reddit Message Manager project into a single organized text file
    """

    # Base path from your project structure
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    if not os.path.exists(base_path):
        print(f"❌ Base path does not exist: {base_path}")
        return

    # Define ONLY the file extensions you want to include
    code_extensions = {
        '*.java': 'Java',
        '*.html': 'HTML',
        '*.css': 'CSS',
        '*.js': 'JavaScript',
        'pom.xml': 'XML',
        '*.properties': 'Properties'
    }

    # Directories to exclude
    exclude_dirs = {
        'target', 'build', '.git', '.idea', 'node_modules', '__pycache__',
        '.vscode', 'logs', 'temp', 'cache'
    }

    # Files to exclude
    exclude_files = {
        'mvnw', 'mvnw.cmd', '.gitignore', '.gitattributes',
        'analyze_project_structure.py', 'combine_all_code.py', 'combine_code_selective.py'
    }

    print("=" * 80)
    print("📁 REDDIT MESSAGE MANAGER - SELECTIVE CODE COMBINER")
    print("=" * 80)
    print(f"📍 Scanning: {base_path}")
    print(f"🔍 Including only: Java, HTML, CSS, JavaScript, pom.xml, Properties")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Collect all code files
    code_files = []

    for root, dirs, files in os.walk(base_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Get relative path for organization
        rel_path = os.path.relpath(root, base_path)
        if rel_path == '.':
            rel_path = 'root'

        for filename in files:
            # Skip excluded files
            if filename in exclude_files:
                continue

            # Check if file matches our extensions
            file_type = None
            for pattern, ftype in code_extensions.items():
                if pattern == filename or fnmatch.fnmatch(filename, pattern):
                    file_type = ftype
                    break

            if file_type:
                full_path = os.path.join(root, filename)
                rel_file_path = os.path.join(rel_path, filename).replace('\\', '/')

                code_files.append({
                    'path': full_path,
                    'relative_path': rel_file_path,
                    'filename': filename,
                    'type': file_type,
                    'category': get_file_category(rel_file_path, filename)
                })

    # Sort files by category and then by path
    code_files.sort(key=lambda x: (x['category'], x['relative_path']))

    print(f"📊 Found {len(code_files)} code files")

    # Create combined file
    output_filename = f"RedditMessageManager_Essential_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(base_path, output_filename)

    try:
        with open(output_path, 'w', encoding='utf-8') as combined_file:
            # Write header
            write_header(combined_file, len(code_files))

            # Group files by category
            current_category = None
            files_written = 0

            for file_info in code_files:
                # Write category header if changed
                if file_info['category'] != current_category:
                    current_category = file_info['category']
                    write_category_header(combined_file, current_category)

                # Write file content
                if write_file_content(combined_file, file_info):
                    files_written += 1
                    print(f"✅ Added: {file_info['relative_path']}")
                else:
                    print(f"⚠️  Skipped: {file_info['relative_path']} (error reading)")

            # Write footer
            write_footer(combined_file, files_written)

        print()
        print("=" * 80)
        print("✅ SELECTIVE CODE COMBINATION COMPLETED!")
        print("=" * 80)
        print(f"📄 Output file: {output_filename}")
        print(f"📊 Files processed: {files_written}/{len(code_files)}")
        print(f"📦 File size: {format_file_size(os.path.getsize(output_path))}")
        print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"❌ Error creating combined file: {str(e)}")

def get_file_category(file_path, filename):
    """Categorize files based on their path"""
    if filename == 'pom.xml':
        return '1_Project_Configuration'
    elif file_path.endswith('.properties'):
        return '2_Application_Properties'
    elif 'src/main/java' in file_path:
        if '/controller/' in file_path:
            return '3_Controllers'
        elif '/service/' in file_path:
            return '4_Services'
        elif '/entity/' in file_path:
            return '5_Entities'
        elif '/repository/' in file_path:
            return '6_Repositories'
        elif '/dto/' in file_path:
            return '7_DTOs'
        elif '/config/' in file_path:
            return '8_Configuration'
        elif '/websocket/' in file_path:
            return '9_WebSocket'
        else:
            return '10_Java_Other'
    elif '/css/' in file_path:
        return '11_CSS_Styles'
    elif '/js/' in file_path:
        return '12_JavaScript'
    elif '/templates/' in file_path:
        if '/modals/' in file_path:
            return '13_HTML_Modals'
        else:
            return '14_HTML_Templates'
    else:
        return '15_Other'

def write_header(file, total_files):
    """Write file header"""
    file.write("=" * 100 + "\n")
    file.write("          REDDIT MESSAGE MANAGER - ESSENTIAL CODE BASE (SELECTIVE)\n")
    file.write("=" * 100 + "\n")
    file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    file.write(f"Total files: {total_files}\n")
    file.write(f"Project: Local Reddit Chat Application\n")
    file.write(f"Includes: Java, HTML, CSS, JavaScript, pom.xml, Properties only\n")
    file.write("=" * 100 + "\n\n")

    # Write table of contents
    file.write("📋 TABLE OF CONTENTS:\n")
    file.write("-" * 50 + "\n")
    categories = [
        "1. Project Configuration (pom.xml)",
        "2. Application Properties",
        "3. Controllers (REST API endpoints)",
        "4. Services (Business logic)",
        "5. Entities (Database models)",
        "6. Repositories (Data access)",
        "7. DTOs (Data transfer objects)",
        "8. Configuration (Spring Boot config)",
        "9. WebSocket (Real-time messaging)",
        "10. Other Java files",
        "11. CSS Styles (Frontend styling)",
        "12. JavaScript (Frontend logic)",
        "13. HTML Modals (Modal templates)",
        "14. HTML Templates (Main templates)"
    ]

    for category in categories:
        file.write(f"   • {category}\n")

    file.write("\n" + "=" * 100 + "\n\n")

def write_category_header(file, category):
    """Write category section header"""
    category_names = {
        '1_Project_Configuration': '📋 PROJECT CONFIGURATION (pom.xml)',
        '2_Application_Properties': '⚙️ APPLICATION PROPERTIES',
        '3_Controllers': '🔌 REST API CONTROLLERS',
        '4_Services': '⚙️ BUSINESS SERVICES',
        '5_Entities': '🗃️ DATABASE ENTITIES',
        '6_Repositories': '💾 DATA REPOSITORIES',
        '7_DTOs': '📦 DATA TRANSFER OBJECTS',
        '8_Configuration': '⚙️ SPRING CONFIGURATION',
        '9_WebSocket': '🔗 WEBSOCKET HANDLERS',
        '10_Java_Other': '☕ OTHER JAVA FILES',
        '11_CSS_Styles': '🎨 CSS STYLESHEETS',
        '12_JavaScript': '⚡ JAVASCRIPT FILES',
        '13_HTML_Modals': '🪟 HTML MODAL TEMPLATES',
        '14_HTML_Templates': '📄 HTML MAIN TEMPLATES',
        '15_Other': '📁 OTHER FILES'
    }

    section_name = category_names.get(category, category.replace('_', ' ').upper())

    file.write("\n" + "🔸" * 50 + "\n")
    file.write(f"   {section_name}\n")
    file.write("🔸" * 50 + "\n\n")

def write_file_content(file, file_info):
    """Write individual file content"""
    try:
        file.write(f"{'='*20} {file_info['filename']} {'='*20}\n")
        file.write(f"📁 Path: {file_info['relative_path']}\n")
        file.write(f"📄 Type: {file_info['type']}\n")
        file.write(f"🕒 Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("-" * 80 + "\n\n")

        # Read and write file content
        try:
            with open(file_info['path'], 'r', encoding='utf-8') as source_file:
                content = source_file.read()
                file.write(content)
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_info['path'], 'r', encoding='latin-1') as source_file:
                content = source_file.read()
                file.write(content)

        file.write(f"\n\n{'='*20} END OF {file_info['filename']} {'='*20}\n\n\n")
        return True

    except Exception as e:
        file.write(f"❌ ERROR READING FILE: {str(e)}\n\n")
        return False

def write_footer(file, files_processed):
    """Write file footer"""
    file.write("\n" + "=" * 100 + "\n")
    file.write("                    END OF SELECTIVE CODE COMPILATION\n")
    file.write("=" * 100 + "\n")
    file.write(f"📊 Files processed: {files_processed}\n")
    file.write(f"📁 Includes: Java, HTML, CSS, JavaScript, pom.xml, Properties\n")
    file.write(f"🚫 Excludes: Markdown, JSON, YAML, build files, IDE files\n")
    file.write(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    file.write(f"📋 Project: Reddit Message Manager - Essential Code Only\n")
    file.write("=" * 100 + "\n")

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0

    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"

def main():
    print("🚀 Starting Reddit Message Manager SELECTIVE Code Combination...")
    print("🎯 Including ONLY: Java, HTML, CSS, JavaScript, pom.xml, Properties")
    combine_selective_code()
    print("\n💡 This file contains only your essential source code and configuration!")

if __name__ == "__main__":
    main()