const { app, BrowserWindow, Menu } = require('electron');

let window;

function createWindow() {
  // Menu.setApplicationMenu(
  //   Menu.buildFromTemplate([{
  //     label: 'Restart',
  //     click() { app.relaunch(); app.quit(); }
  //   }])
  // );
  window = new BrowserWindow({ show: false, webPreferences: { nodeIntegration: true } });
  window.maximize();
  window.loadFile('client/index.html');
  window.webContents.openDevTools();
  window.show();

  window.on('closed', () => window = null);
}

app.on('ready', createWindow);
app.on('activate', () => {
  !window && createWindow();
});


app.on('window-all-closed', () => {
  process.platform !== 'darwin' && app.quit();
});
