import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { Key as KeyIcon, Moon, Sun, LayoutDashboard, Settings as SettingsIcon } from 'lucide-react';
import KeyManagement from './components/KeyManagement';
import CreateKey from './components/CreateKey';
import Settings from './components/Settings';
import { Tab } from './components/Tab';
import { Key } from './types';

function App() {
  const [activeTab, setActiveTab] = useState<'manage' | 'create' | 'settings'>('manage');
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [lastCreatedKey, setLastCreatedKey] = useState<Key | null>(null);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark');
  };

  const handleKeyCreated = (key: Key) => {
    setLastCreatedKey(key);
    setActiveTab('manage');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-background/90 transition-colors duration-300">
      <Toaster position="top-right" />
      
      {}
      <header className="bg-card/80 backdrop-blur-sm border-b border-border/50 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="p-2 bg-gradient-to-r from-primary to-primary/80 rounded-lg">
                <KeyIcon className="h-8 w-8 text-primary-foreground" />
              </div>
              <h1 className="ml-4 text-3xl font-bold bg-gradient-to-r from-primary to-primary/80 text-transparent bg-clip-text">
                License Manager
              </h1>
            </div>
            
            {}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-card hover:bg-muted transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'light' ? (
                <Moon className="h-5 w-5 text-foreground" />
              ) : (
                <Sun className="h-5 w-5 text-foreground" />
              )}
            </button>
          </div>
        </div>
      </header>

      {}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {}
        <div className="flex justify-center mb-8">
          <div className="inline-flex rounded-lg bg-card/50 backdrop-blur-sm p-1.5 shadow-lg gap-1">
            <Tab
              value="manage"
              activeTab={activeTab}
              onClick={setActiveTab}
              icon={<LayoutDashboard className="w-4 h-4" />}
            >
              Manage Keys
            </Tab>
            <Tab
              value="create"
              activeTab={activeTab}
              onClick={setActiveTab}
              icon={<KeyIcon className="w-4 h-4" />}
            >
              Create New Key
            </Tab>
            <Tab
              value="settings"
              activeTab={activeTab}
              onClick={setActiveTab}
              icon={<SettingsIcon className="w-4 h-4" />}
            >
              Settings
            </Tab>
          </div>
        </div>

        {}
        <div className="glass-card rounded-2xl overflow-hidden animate-fade-in">
          {activeTab === 'manage' && <KeyManagement lastCreatedKey={lastCreatedKey} />}
          {activeTab === 'create' && <CreateKey onKeyCreated={handleKeyCreated} />}
          {activeTab === 'settings' && <Settings />}
        </div>
      </main>
    </div>
  );
}

export default App;