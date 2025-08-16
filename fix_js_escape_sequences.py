import os
import re

def fix_js_files_script():
    """
    Fix escape sequence warnings in create_js_files.py
    """
    
    script_path = "create_js_files.py"
    
    if not os.path.exists(script_path):
        print(f"❌ Error: {script_path} not found!")
        return False
    
    try:
        # Read the original file
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing escape sequence issues in create_js_files.py...")
        
        # Create backup
        backup_path = "create_js_files.py.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📦 Created backup: {backup_path}")
        
        # Fix 1: Convert all JavaScript content strings to raw strings
        content = re.sub(r'("content":\s*)"""', r'\1r"""', content)
        print("✅ Converted JavaScript content to raw strings")
        
        # Fix 2: Fix template literals and variables inside the content
        # This is more complex - we need to find content blocks and fix them
        
        # Split content into parts to isolate the JavaScript content blocks
        parts = content.split('r"""')
        
        for i in range(1, len(parts), 2):  # Process every other part (the JS content)
            js_content = parts[i].split('"""')[0]  # Get content before closing """
            
            # Fix template literals
            js_content = js_content.replace('\\`', '`')
            js_content = js_content.replace('\\${', '${')
            
            # Fix the specific problematic lines mentioned in the error
            if 'CONFIG.API_BASE_URL' in js_content:
                js_content = js_content.replace('\\${CONFIG.API_BASE_URL}', '${CONFIG.API_BASE_URL}')
                js_content = js_content.replace('\\${encodeURIComponent(query)}', '${encodeURIComponent(query)}')
            
            # Put the fixed content back
            remaining = parts[i].split('"""', 1)[1] if '"""' in parts[i] else ''
            parts[i] = js_content + '"""' + remaining
        
        # Reconstruct the content
        content = 'r"""'.join(parts)
        
        print("✅ Fixed template literals and variables")
        
        # Write the fixed content back
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully fixed create_js_files.py!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing file: {str(e)}")
        
        # Restore backup if something went wrong
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
                print(f"🔄 Restored original file from backup")
            except:
                print("❌ Failed to restore backup")
        
        return False

def main():
    print("=" * 60)
    print("🛠️  JavaScript Files Script Fixer (Fixed Version)")
    print("=" * 60)
    
    if fix_js_files_script():
        print("\n🎉 Script fixed successfully!")
        print("\nYou can now run:")
        print("   python create_js_files.py")
        print("\nwithout any escape sequence warnings!")
    else:
        print("\n❌ Failed to fix the script.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()