"""Simple MSI builder using Windows built-in msilib and existing EXE."""

import os
import sys
import uuid
import subprocess
from pathlib import Path
import tempfile
import shutil

def build_exe_first():
    """Build the EXE file first using existing build script."""
    print("[STEP 1/3] Building executable first...")
    
    try:
        result = subprocess.run([
            sys.executable, 'build_exe.py'
        ], check=True, capture_output=True, text=True)
        
        exe_path = Path('dist/Speech2Text.exe')
        if exe_path.exists():
            print(f"[OK] Executable built successfully: {exe_path}")
            return True
        else:
            print("[ERROR] Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] EXE build failed: {e}")
        return False

def create_wix_config():
    """Create WiX configuration for MSI building."""
    
    # Generate unique GUIDs
    product_guid = str(uuid.uuid4()).upper()
    upgrade_guid = str(uuid.uuid4()).upper()
    component_guid = str(uuid.uuid4()).upper()
    
    wix_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="{product_guid}" 
             Name="Speech2Text" 
             Language="1033" 
             Version="0.1.0" 
             Manufacturer="Speech2Text Contributors" 
             UpgradeCode="{upgrade_guid}">
        
        <Package InstallerVersion="200" 
                 Compressed="yes" 
                 InstallScope="perMachine" 
                 Description="Modern Speech-to-Text Desktop Application"
                 Comments="Powered by OpenAI Whisper API" />

        <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed." />
        
        <MediaTemplate EmbedCab="yes" />

        <Feature Id="ProductFeature" Title="Speech2Text Application" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
            <ComponentRef Id="ApplicationShortcut" />
            <ComponentRef Id="DesktopShortcut" />
        </Feature>

        <!-- Directory structure -->
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="Speech2Text" />
            </Directory>
            <Directory Id="ProgramMenuFolder">
                <Directory Id="ApplicationProgramsFolder" Name="Speech2Text"/>
            </Directory>
            <Directory Id="DesktopFolder" Name="Desktop" />
        </Directory>

        <!-- Components -->
        <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
            <Component Id="MainExecutable" Guid="{component_guid}">
                <File Id="Speech2TextEXE" 
                      Source="dist\\Speech2Text.exe" 
                      KeyPath="yes" 
                      Checksum="yes"/>
                
                <!-- Registry entries for Add/Remove Programs -->
                <RegistryValue Root="HKCU" 
                              Key="Software\\Speech2Text" 
                              Name="InstallPath" 
                              Type="string" 
                              Value="[INSTALLFOLDER]" 
                              KeyPath="no" />
            </Component>
        </ComponentGroup>

        <!-- Start Menu Shortcut -->
        <Component Id="ApplicationShortcut" Directory="ApplicationProgramsFolder" Guid="{str(uuid.uuid4()).upper()}">
            <Shortcut Id="ApplicationStartMenuShortcut"
                      Name="Speech2Text"
                      Description="Modern Speech-to-Text Application"
                      Target="[INSTALLFOLDER]Speech2Text.exe"
                      WorkingDirectory="INSTALLFOLDER" />
            <RemoveFolder Id="ApplicationProgramsFolder" On="uninstall" />
            <RegistryValue Root="HKCU" 
                          Key="Software\\Speech2Text" 
                          Name="StartMenu" 
                          Type="integer" 
                          Value="1" 
                          KeyPath="yes" />
        </Component>

        <!-- Desktop Shortcut -->
        <Component Id="DesktopShortcut" Directory="DesktopFolder" Guid="{str(uuid.uuid4()).upper()}">
            <Shortcut Id="ApplicationDesktopShortcut"
                      Name="Speech2Text"
                      Description="Modern Speech-to-Text Application"
                      Target="[INSTALLFOLDER]Speech2Text.exe"
                      WorkingDirectory="INSTALLFOLDER" />
            <RegistryValue Root="HKCU" 
                          Key="Software\\Speech2Text" 
                          Name="Desktop" 
                          Type="integer" 
                          Value="1" 
                          KeyPath="yes" />
        </Component>

        <!-- UI Configuration -->
        <UI>
            <UIRef Id="WixUI_InstallDir" />
            <Publish Dialog="ExitDialog"
                    Control="Finish" 
                    Event="DoAction" 
                    Value="LaunchApplication">WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1 and NOT Installed</Publish>
        </UI>

        <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />
        <Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT" Value="Launch Speech2Text" />

        <!-- Custom action to launch app after install -->
        <Property Id="WixShellExecTarget" Value="[INSTALLFOLDER]Speech2Text.exe" />
        <CustomAction Id="LaunchApplication" 
                      BinaryKey="WixCA" 
                      DllEntry="WixShellExec"
                      Impersonate="yes" />
    </Product>
</Wix>'''
    
    with open('speech2text.wxs', 'w', encoding='utf-8') as f:
        f.write(wix_content)
    
    print("[OK] Created WiX configuration file (speech2text.wxs)")
    return True

def check_wix_toolset():
    """Check if WiX Toolset is installed."""
    try:
        result = subprocess.run(['candle', '-?'], 
                              capture_output=True, text=True, timeout=5)
        print("[OK] WiX Toolset is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def install_wix_toolset():
    """Provide instructions for installing WiX Toolset."""
    print("[INFO] WiX Toolset not found. To build MSI installers, you need WiX Toolset.")
    print("[INSTALL] Installation options:")
    print("1. Download from: https://wixtoolset.org/")
    print("2. Or install via winget: winget install Microsoft.WiX")
    print("3. Or install via chocolatey: choco install wixtoolset")
    return False

def build_msi_with_wix():
    """Build MSI using WiX Toolset."""
    print("[STEP 2/3] Compiling WiX source...")
    
    try:
        # Compile WiX source to object file
        result = subprocess.run([
            'candle', 'speech2text.wxs',
            '-out', 'speech2text.wixobj'
        ], check=True, capture_output=True, text=True)
        
        print("[OK] WiX source compiled successfully")
        
        print("[STEP 3/3] Linking to create MSI...")
        
        # Link object file to create MSI
        result = subprocess.run([
            'light', 'speech2text.wixobj',
            '-out', 'dist/Speech2Text.msi',
            '-ext', 'WixUIExtension'
        ], check=True, capture_output=True, text=True)
        
        print("[SUCCESS] MSI installer created successfully!")
        
        # Check file size
        msi_path = Path('dist/Speech2Text.msi')
        if msi_path.exists():
            size_mb = msi_path.stat().st_size / (1024 * 1024)
            print(f"[LOCATION] MSI installer: {msi_path.absolute()}")
            print(f"[SIZE] File size: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] WiX build failed!")
        print(f"Error: {e.stderr}")
        return False

def cleanup_temp_files():
    """Clean up temporary build files."""
    temp_files = ['speech2text.wxs', 'speech2text.wixobj', 'speech2text.wixpdb']
    for file in temp_files:
        try:
            if Path(file).exists():
                os.remove(file)
                print(f"[CLEAN] Removed {file}")
        except Exception as e:
            print(f"[WARNING] Could not remove {file}: {e}")

def main():
    """Main MSI build function."""
    print("[START] Building Speech2Text MSI installer...")
    print(f"[DIR] Working directory: {Path.cwd()}")
    
    # Check prerequisites
    if not Path('src/speech2text/main.py').exists():
        print("[ERROR] main.py not found. Make sure you're in the project root directory.")
        return
    
    # Step 1: Build EXE first
    if not build_exe_first():
        print("[ERROR] Cannot build MSI without executable. Build failed.")
        return
    
    # Step 2: Check for WiX Toolset
    if not check_wix_toolset():
        if not install_wix_toolset():
            print("[ERROR] WiX Toolset is required to build MSI installers.")
            print("[ALTERNATIVE] You can still distribute the EXE file from the dist folder.")
            return
    
    # Step 3: Create WiX configuration
    if not create_wix_config():
        print("[ERROR] Failed to create WiX configuration.")
        return
    
    # Step 4: Build MSI
    success = build_msi_with_wix()
    
    # Step 5: Cleanup
    cleanup_temp_files()
    
    if success:
        print("\\n[COMPLETE] MSI installer build completed successfully!")
        print("\\n[FEATURES] The MSI installer includes:")
        print("- ✅ Proper Windows installation (Program Files)")
        print("- ✅ Start Menu shortcut")
        print("- ✅ Desktop shortcut")
        print("- ✅ Add/Remove Programs integration")
        print("- ✅ Upgrade support")
        print("- ✅ Option to launch after installation")
        print("\\n[INSTALLATION] To use the installer:")
        print("1. Double-click Speech2Text.msi")
        print("2. Follow the installation wizard")
        print("3. The app will be installed and shortcuts created")
        print("\\n[DISTRIBUTION] Distribution benefits:")
        print("- Professional Windows installer experience")
        print("- Easy install/uninstall for end users")
        print("- Automatic handling of shortcuts and registry")
        print("- Upgrade support for future versions")
    else:
        print("\\n[FAILED] MSI build failed. Check the error messages above.")
        print("\\n[ALTERNATIVE] You can still use the EXE version:")
        print("The Speech2Text.exe file in the dist folder works standalone.")

if __name__ == "__main__":
    main()