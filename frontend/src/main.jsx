import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// Ensure root element exists
const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("❌ Root element not found. Make sure index.html has <div id='root'></div>");
}

// Create and render the app
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    {/* You can wrap with <ThemeProvider> or <GlobalContext> here in the future */}
    <App />
  </React.StrictMode>
);