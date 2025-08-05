const { app, BrowserWindow, ipcMain, dialog, globalShortcut, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const Store = require('electron-store');
const OpenAI = require('openai');

// Initialize secure settings store
const store = new Store({
    encryptionKey: 'speech2text-secure-key',
    defaults: {
        api_key: '',
        audio_settings: {
            sample_rate: 44100,
            chunk_size: 1024,
            channels: 1
        },
        transcription_settings: {
            model: 'whisper-1',
            language: 'en',
            temperature: 0.0,
            prompt: ''
        },
        output_settings: {
            auto_save: false,
            save_directory: '',
            file_format: 'txt'
        },
        ui: {
            theme: 'dark',
            window_geometry: '1200x900'
        },
        sound_notifications: {
            enabled: true,
            recording_start: true,
            recording_stop: true,
            transcription_processing: true,
            transcription_complete: true
        },
        auto_paste: {
            enabled: false
        }
    }
});

let mainWindow;
let openaiClient = null;

// Sound notification functions
function playNotificationSound(soundType) {
    const soundSettings = store.get('sound_notifications');
    if (!soundSettings.enabled || !soundSettings[soundType]) {
        return;
    }

    try {
        if (process.platform === 'win32') {
            // Windows system sounds
            const { exec } = require('child_process');
            switch (soundType) {
                case 'recording_start':
                    exec('powershell -c "[console]::beep(800,150)"');
                    break;
                case 'recording_stop':
                    exec('powershell -c "[console]::beep(600,150)"');
                    break;
                case 'transcription_processing':
                    exec('powershell -c "[console]::beep(700,100); Start-Sleep -m 50; [console]::beep(700,100)"');
                    break;
                case 'transcription_complete':
                    exec('powershell -c "[console]::beep(600,100); Start-Sleep -m 50; [console]::beep(800,100); Start-Sleep -m 50; [console]::beep(1000,150)"');
                    break;
            }
        } else if (process.platform === 'darwin') {
            // macOS system sounds
            const { exec } = require('child_process');
            switch (soundType) {
                case 'recording_start':
                    exec('afplay /System/Library/Sounds/Glass.aiff');
                    break;
                case 'recording_stop':
                    exec('afplay /System/Library/Sounds/Tink.aiff');
                    break;
                case 'transcription_processing':
                    exec('afplay /System/Library/Sounds/Submarine.aiff');
                    break;
                case 'transcription_complete':
                    exec('afplay /System/Library/Sounds/Hero.aiff');
                    break;
            }
        } else if (process.platform === 'linux') {
            // Linux system sounds
            const { exec } = require('child_process');
            switch (soundType) {
                case 'recording_start':
                case 'recording_stop':
                case 'transcription_processing':
                case 'transcription_complete':
                    exec('paplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null || echo -e "\\a"');
                    break;
            }
        }
    } catch (error) {
        console.warn('Failed to play notification sound:', error);
    }
}

// Auto-paste function with enhanced Windows support
function performAutoPaste(text) {
    const autoPasteSettings = store.get('auto_paste');
    if (!autoPasteSettings.enabled || !text || !text.trim()) {
        console.log('Auto-paste skipped: disabled or no text');
        return;
    }

    console.log('Attempting auto-paste with text:', text.substring(0, 50) + '...');

    try {
        const { clipboard } = require('electron');
        
        // Save current clipboard content
        const originalClipboard = clipboard.readText();
        console.log('Saved original clipboard content');
        
        // Set text to clipboard
        clipboard.writeText(text);
        console.log('Set transcription text to clipboard');
        
        // Small delay to ensure clipboard is updated
        setTimeout(() => {
            if (process.platform === 'win32') {
                performWindowsPaste();
            } else if (process.platform === 'darwin') {
                performMacOSPaste();
            } else if (process.platform === 'linux') {
                performLinuxPaste();
            }
            
            // Restore original clipboard after a delay
            setTimeout(() => {
                clipboard.writeText(originalClipboard);
                console.log('Restored original clipboard content');
            }, 800);
        }, 150);
        
    } catch (error) {
        console.error('Failed to perform auto-paste:', error);
    }
}

// Enhanced Windows auto-paste implementation
async function performWindowsPaste() {
    console.log('Performing Windows auto-paste');
    
    try {
        // Check if we should proceed with auto-paste
        const shouldPaste = await isTextFieldActive();
        if (!shouldPaste) {
            console.log('Auto-paste conditions not met, skipping');
            return;
        }

        const { exec } = require('child_process');
        
        // Method 1: Try with more reliable PowerShell approach
        // Use proper escaping for PowerShell
        const psScript = `
Add-Type -AssemblyName System.Windows.Forms
Start-Sleep -Milliseconds 100
[System.Windows.Forms.SendKeys]::SendWait('^v')
        `.trim();
        
        console.log('Executing PowerShell script:', psScript);
        
        exec(`powershell -Command "${psScript}"`, (error, stdout, stderr) => {
            if (error) {
                console.warn('PowerShell paste failed:', error.message, 'stderr:', stderr);
                // Fallback: Try with different approach
                tryAlternativeWindowsPaste();
            } else {
                console.log('Windows auto-paste completed successfully');
            }
        });
        
    } catch (error) {
        console.error('Windows auto-paste failed:', error);
        tryAlternativeWindowsPaste();
    }
}

// Alternative Windows paste method
function tryAlternativeWindowsPaste() {
    console.log('Trying alternative Windows paste method');
    
    try {
        const { exec } = require('child_process');
        
        // Use VBScript as alternative
        const vbsCommand = `Set WshShell = CreateObject("WScript.Shell")
WScript.Sleep 100
WshShell.SendKeys "^v"`;
        
        // Write VBS to temp file and execute
        const fs = require('fs');
        const path = require('path');
        const os = require('os');
        
        const tempVbs = path.join(os.tmpdir(), 'autopaste.vbs');
        console.log('Writing VBScript to:', tempVbs);
        console.log('VBScript content:', vbsCommand);
        fs.writeFileSync(tempVbs, vbsCommand);
        
        exec(`cscript //nologo "${tempVbs}"`, (error, stdout, stderr) => {
            // Clean up temp file
            try {
                fs.unlinkSync(tempVbs);
            } catch (e) {
                // Ignore cleanup errors
            }
            
            if (error) {
                console.warn('Alternative Windows paste failed:', error.message, 'stderr:', stderr);
            } else {
                console.log('Alternative Windows auto-paste completed successfully');
            }
        });
        
    } catch (error) {
        console.error('Alternative Windows paste method failed:', error);
    }
}

// Check if a text field is currently active (Windows-specific)
function isTextFieldActive() {
    return new Promise((resolve) => {
        try {
            const { exec } = require('child_process');
            
            // Check if VoiceForge is the active window - if so, don't auto-paste
            const checkCommand = `
                Add-Type -AssemblyName user32;
                $hwnd = [user32]::GetForegroundWindow();
                $length = [user32]::GetWindowTextLength($hwnd);
                $sb = New-Object System.Text.StringBuilder $length;
                [user32]::GetWindowText($hwnd, $sb, $length + 1);
                $windowTitle = $sb.ToString();
                Write-Output $windowTitle;
                
                Add-Type -MemberDefinition '
                    [DllImport("user32.dll")]
                    public static extern IntPtr GetForegroundWindow();
                    [DllImport("user32.dll")]
                    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
                    [DllImport("user32.dll")]
                    public static extern int GetWindowTextLength(IntPtr hWnd);
                ' -Name user32 -Namespace Win32Functions -PassThru | Out-Null;
            `;
            
            exec(`powershell -Command "${checkCommand}"`, { timeout: 2000 }, (error, stdout, stderr) => {
                if (error) {
                    console.warn('Could not detect active window, proceeding with auto-paste:', error.message);
                    resolve(true); // Default to attempting paste
                    return;
                }
                
                const windowTitle = stdout.trim().toLowerCase();
                console.log('Active window title:', windowTitle);
                
                // If VoiceForge is active, don't auto-paste (user is still in the app)
                if (windowTitle.includes('voiceforge') || windowTitle.includes('speech') || windowTitle.includes('modern speech recognition')) {
                    console.log('VoiceForge is still the active window, skipping auto-paste');
                    resolve(false);
                } else {
                    console.log('Different application is active, proceeding with auto-paste');
                    resolve(true);
                }
            });
            
        } catch (error) {
            console.warn('Could not detect active text field, proceeding anyway:', error);
            resolve(true); // Default to attempting paste
        }
    });
}

// Enhanced macOS auto-paste implementation
function performMacOSPaste() {
    console.log('Performing macOS auto-paste');
    
    try {
        const { exec } = require('child_process');
        
        const appleScript = `
            tell application "System Events"
                delay 0.1
                keystroke "v" using command down
            end tell
        `;
        
        exec(`osascript -e '${appleScript}'`, (error, stdout, stderr) => {
            if (error) {
                console.error('macOS auto-paste failed:', error.message);
            } else {
                console.log('macOS auto-paste completed successfully');
            }
        });
        
    } catch (error) {
        console.error('macOS auto-paste failed:', error);
    }
}

// Enhanced Linux auto-paste implementation
function performLinuxPaste() {
    console.log('Performing Linux auto-paste');
    
    try {
        const { exec } = require('child_process');
        
        // Try xdotool first
        exec('which xdotool', (error) => {
            if (error) {
                // xdotool not available, try xclip + xvkbd
                console.log('xdotool not found, trying alternative Linux paste method');
                exec('sleep 0.1 && xvkbd -text "\\Cv" 2>/dev/null || echo "Linux auto-paste failed"', (error) => {
                    if (error) {
                        console.warn('Linux auto-paste failed:', error.message);
                    } else {
                        console.log('Linux auto-paste completed (xvkbd)');
                    }
                });
            } else {
                // Use xdotool
                exec('sleep 0.1 && xdotool key ctrl+v', (error) => {
                    if (error) {
                        console.warn('Linux auto-paste failed:', error.message);
                    } else {
                        console.log('Linux auto-paste completed (xdotool)');
                    }
                });
            }
        });
        
    } catch (error) {
        console.error('Linux auto-paste failed:', error);
    }
}

function createWindow() {
    const geometry = store.get('ui.window_geometry', '1200x900');
    const [width, height] = geometry.split('x').map(Number);

    mainWindow = new BrowserWindow({
        width: width || 1200,
        height: height || 900,
        minWidth: 900,
        minHeight: 700,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, 'preload.js')
        },
        titleBarStyle: 'default',
        backgroundColor: '#1c1c1e',
        show: false,
        icon: path.join(__dirname, '../assets/icon.png')
    });

    // Load the renderer
    if (process.env.ELECTRON_IS_DEV) {
        mainWindow.loadURL('http://localhost:3000');
        mainWindow.webContents.openDevTools();
    } else {
        mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
    }

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        
        // Apply dark theme to title bar on Windows
        if (process.platform === 'win32') {
            try {
                // Check if titleBarStyle supports overlay before attempting
                if (mainWindow.setTitleBarOverlay && typeof mainWindow.setTitleBarOverlay === 'function') {
                    // Additional check - only set if the window was created with proper titleBarStyle
                    const webContents = mainWindow.webContents;
                    if (webContents && !webContents.isDestroyed()) {
                        mainWindow.setTitleBarOverlay({
                            color: '#1e1e1e',
                            symbolColor: '#ffffff'
                        });
                    }
                }
            } catch (error) {
                console.warn('Title bar overlay not supported:', error.message);
            }
        }
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    mainWindow.on('resize', () => {
        const [width, height] = mainWindow.getSize();
        store.set('ui.window_geometry', `${width}x${height}`);
    });

    // Initialize OpenAI client
    updateOpenAIClient();
}

function updateOpenAIClient() {
    const apiKey = store.get('api_key');
    if (apiKey) {
        openaiClient = new OpenAI({ apiKey });
    } else {
        openaiClient = null;
    }
}

function setupMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                {
                    label: 'Save Text',
                    accelerator: 'CmdOrCtrl+S',
                    click: () => {
                        mainWindow.webContents.send('menu-save-text');
                    }
                },
                { type: 'separator' },
                {
                    label: 'Exit',
                    accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: 'Recording',
            submenu: [
                {
                    label: 'Toggle Recording',
                    accelerator: 'CmdOrCtrl+N',
                    click: () => {
                        mainWindow.webContents.send('menu-toggle-recording');
                    }
                },
                {
                    label: 'Stop Recording',
                    accelerator: 'Escape',
                    click: () => {
                        mainWindow.webContents.send('menu-stop-recording');
                    }
                }
            ]
        },
        {
            label: 'View',
            submenu: [
                {
                    label: 'Settings',
                    accelerator: 'CmdOrCtrl+,',
                    click: () => {
                        mainWindow.webContents.send('menu-toggle-settings');
                    }
                },
                { type: 'separator' },
                { role: 'reload' },
                { role: 'forceReload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' }
            ]
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'Keyboard Shortcuts',
                    accelerator: 'F1',
                    click: () => {
                        mainWindow.webContents.send('menu-show-shortcuts');
                    }
                },
                {
                    label: 'About',
                    click: () => {
                        mainWindow.webContents.send('menu-show-about');
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function setupGlobalShortcuts() {
    // Global hotkey for toggle recording (Ctrl+Win on Windows, Cmd+Ctrl on Mac)
    const toggleShortcut = process.platform === 'darwin' ? 'Cmd+Ctrl+Space' : 'Ctrl+Super+Space';
    
    try {
        const success = globalShortcut.register(toggleShortcut, () => {
            if (mainWindow && !mainWindow.isDestroyed()) {
                mainWindow.webContents.send('global-toggle-recording');
                console.log('Global shortcut triggered');
            }
        });
        
        if (success) {
            console.log(`Global shortcut registered: ${toggleShortcut}`);
        } else {
            console.error(`Failed to register global shortcut: ${toggleShortcut}`);
            // Try alternative shortcuts
            const altShortcut = process.platform === 'darwin' ? 'Cmd+Option+Space' : 'Ctrl+Alt+Space';
            const altSuccess = globalShortcut.register(altShortcut, () => {
                if (mainWindow && !mainWindow.isDestroyed()) {
                    mainWindow.webContents.send('global-toggle-recording');
                    console.log('Alternative global shortcut triggered');
                }
            });
            
            if (altSuccess) {
                console.log(`Alternative global shortcut registered: ${altShortcut}`);
            }
        }
    } catch (error) {
        console.error('Error registering global shortcut:', error);
    }
}

// IPC Handlers
ipcMain.handle('get-settings', (event, key) => {
    if (key) {
        return store.get(key);
    }
    return store.store;
});

ipcMain.handle('set-setting', (event, key, value) => {
    store.set(key, value);
    
    // Update OpenAI client if API key changed
    if (key === 'api_key') {
        updateOpenAIClient();
    }
    
    return true;
});

ipcMain.handle('save-settings', () => {
    // Settings are automatically saved by electron-store
    return true;
});

ipcMain.handle('reset-settings', () => {
    store.clear();
    updateOpenAIClient();
    return true;
});

ipcMain.handle('transcribe-audio', async (event, audioBuffer, settings) => {
    if (!openaiClient) {
        throw new Error('OpenAI API key not configured');
    }

    try {
        // Create temporary file
        const tempDir = require('os').tmpdir();
        const tempFile = path.join(tempDir, `speech2text_${Date.now()}.wav`);
        
        // Write audio buffer to file
        fs.writeFileSync(tempFile, audioBuffer);

        // Transcribe using OpenAI
        const transcript = await openaiClient.audio.transcriptions.create({
            file: fs.createReadStream(tempFile),
            model: settings.model || 'whisper-1',
            language: settings.language || 'en',
            temperature: settings.temperature || 0.0,
            prompt: settings.prompt || undefined
        });

        // Clean up temp file
        fs.unlinkSync(tempFile);

        return transcript.text;
    } catch (error) {
        console.error('Transcription error:', error);
        throw error;
    }
});

ipcMain.handle('save-transcript', async (event, text, filename) => {
    try {
        if (filename) {
            fs.writeFileSync(filename, text, 'utf8');
            return filename;
        } else {
            // Auto-save with timestamp
            const outputSettings = store.get('output_settings');
            const saveDir = outputSettings.save_directory || require('os').homedir();
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            const autoFilename = path.join(saveDir, `transcript_${timestamp}.${outputSettings.file_format || 'txt'}`);
            
            fs.writeFileSync(autoFilename, text, 'utf8');
            return autoFilename;
        }
    } catch (error) {
        console.error('Save error:', error);
        throw error;
    }
});

ipcMain.handle('show-save-dialog', async (event, options) => {
    const result = await dialog.showSaveDialog(mainWindow, options);
    return result;
});

ipcMain.handle('show-message-box', async (event, options) => {
    const result = await dialog.showMessageBox(mainWindow, options);
    return result;
});

// Sound notification handlers
ipcMain.handle('play-notification-sound', (event, soundType) => {
    playNotificationSound(soundType);
    return true;
});

// Safe auto-paste handler (doesn't interfere with main clipboard)
ipcMain.handle('auto-paste-text', (event, text) => {
    const autoPasteSettings = store.get('auto_paste');
    if (!autoPasteSettings || !autoPasteSettings.enabled || !text || !text.trim()) {
        console.log('Auto-paste skipped: disabled or no text');
        return true;
    }

    console.log('Safe auto-paste: pasting without touching main clipboard');
    
    // Use direct keyboard simulation without clipboard manipulation
    if (process.platform === 'win32') {
        safeWindowsPaste(text);
    } else if (process.platform === 'darwin') {
        safeMacOSPaste(text);
    } else if (process.platform === 'linux') {
        safeLinuxPaste(text);
    }
    
    return true;
});

// Clipboard handler (reliable clipboard operations from main process)
ipcMain.handle('copy-to-clipboard', (event, text) => {
    try {
        const { clipboard } = require('electron');
        clipboard.writeText(text);
        console.log('Text copied to clipboard via main process');
        return true;
    } catch (error) {
        console.error('Failed to copy to clipboard:', error);
        return false;
    }
});

// Safe Windows paste using direct text typing
function safeWindowsPaste(text) {
    try {
        const { exec } = require('child_process');
        
        // More robust text escaping for VBScript
        // Replace quotes, newlines, and other special characters
        let escapedText = text
            .replace(/\\/g, '\\\\')        // Escape backslashes first
            .replace(/"/g, '""')           // Escape quotes for VBScript
            .replace(/\r?\n/g, '" & vbCrLf & "')  // Handle newlines properly
            .replace(/\t/g, '" & vbTab & "');     // Handle tabs
        
        // Split long text into smaller chunks to avoid command line limits
        const maxChunkSize = 500;
        const textChunks = [];
        
        if (escapedText.length > maxChunkSize) {
            for (let i = 0; i < escapedText.length; i += maxChunkSize) {
                textChunks.push(escapedText.substring(i, i + maxChunkSize));
            }
        } else {
            textChunks.push(escapedText);
        }
        
        console.log(`Safe auto-paste: Processing ${textChunks.length} text chunks`);
        
        const vbsCommand = `Set WshShell = CreateObject("WScript.Shell")
WScript.Sleep 200
${textChunks.map((chunk, index) => `WshShell.SendKeys "${chunk}"`).join('\nWScript.Sleep 50\n')}`;
        
        const fs = require('fs');
        const path = require('path');
        const os = require('os');
        
        const tempVbs = path.join(os.tmpdir(), `safeautopaste_${Date.now()}.vbs`);
        console.log('Writing VBScript to:', tempVbs);
        console.log('VBScript content preview:', vbsCommand.substring(0, 200) + '...');
        
        fs.writeFileSync(tempVbs, vbsCommand, 'utf8');
        
        exec(`cscript //nologo "${tempVbs}"`, { timeout: 10000 }, (error, stdout, stderr) => {
            try {
                fs.unlinkSync(tempVbs);
            } catch (e) {
                console.warn('Failed to cleanup temp VBS file:', e.message);
            }
            
            if (error) {
                console.warn('Safe auto-paste failed:', error.message);
                if (stderr) console.warn('VBScript stderr:', stderr);
            } else {
                console.log('Safe auto-paste successful');
                if (stdout) console.log('VBScript stdout:', stdout);
            }
        });
        
    } catch (error) {
        console.error('Safe Windows paste failed:', error);
    }
}

// Safe macOS paste using direct text typing
function safeMacOSPaste(text) {
    try {
        const { exec } = require('child_process');
        
        // More robust escaping for AppleScript
        const escapedText = text
            .replace(/\\/g, '\\\\')    // Escape backslashes
            .replace(/"/g, '\\"')      // Escape quotes
            .replace(/\r?\n/g, '" & return & "')  // Handle newlines
            .replace(/\t/g, '" & tab & "');       // Handle tabs
        
        console.log('Safe macOS auto-paste: Typing text directly');
        
        const appleScript = `tell application "System Events"
    delay 0.2
    keystroke "${escapedText}"
end tell`;
        
        exec(`osascript -e '${appleScript}'`, { timeout: 10000 }, (error, stdout, stderr) => {
            if (error) {
                console.warn('Safe macOS auto-paste failed:', error.message);
                if (stderr) console.warn('AppleScript stderr:', stderr);
            } else {
                console.log('Safe macOS auto-paste successful');
                if (stdout) console.log('AppleScript stdout:', stdout);
            }
        });
        
    } catch (error) {
        console.error('Safe macOS paste failed:', error);
    }
}

// Safe Linux paste using direct text typing
function safeLinuxPaste(text) {
    try {
        const { exec } = require('child_process');
        
        // More robust escaping for xdotool
        const escapedText = text.replace(/'/g, "\\'");
        
        console.log('Safe Linux auto-paste: Typing text directly with xdotool');
        
        // Add a small delay and use xdotool type
        exec(`sleep 0.2 && xdotool type '${escapedText}' 2>/dev/null`, { timeout: 10000 }, (error, stdout, stderr) => {
            if (error) {
                console.warn('Safe Linux auto-paste failed:', error.message);
                if (stderr) console.warn('xdotool stderr:', stderr);
            } else {
                console.log('Safe Linux auto-paste successful');
                if (stdout) console.log('xdotool stdout:', stdout);
            }
        });
        
    } catch (error) {
        console.error('Safe Linux paste failed:', error);
    }
}


// App event handlers
app.whenReady().then(() => {
    createWindow();
    setupMenu();
    setupGlobalShortcuts();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    globalShortcut.unregisterAll();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});

// Handle app protocol for dev/prod
if (process.env.ELECTRON_IS_DEV) {
    require('electron-reload')(__dirname, {
        electron: path.join(__dirname, '..', 'node_modules', '.bin', 'electron'),
        hardResetMethod: 'exit'
    });
}