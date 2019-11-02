const { app, BrowserWindow } = require('electron');

let window;

function createWindow() {
  window = new BrowserWindow({ show: false, webPreferences: { nodeIntegration: true } });
  window.maximize();
  window.loadURL('http://localhost:50123/client/');
  window.webContents.openDevTools();
  window.on('closed', () => window = null);
  window.once('ready-to-show', () => {
    window.show();
  });
}

app.on('ready', createWindow);
app.on('activate', () => {
  !window && createWindow();
});
app.on('window-all-closed', () => {
  process.platform !== 'darwin' && app.quit();
});
