import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import { Search, RefreshCw, Shield, Ban, Clock, List, Monitor } from 'lucide-react';
import { getAllKeys, getKeyInfo, freezeKey, banKey, resetHWID, addTime, getAuthHistory, getSystemInfo } from '../api';
import type { Key, AuthHistory, SystemInfo } from '../types';

interface KeyManagementProps {
  lastCreatedKey: Key | null;
}

export default function KeyManagement({ lastCreatedKey }: KeyManagementProps) {
  const [searchKey, setSearchKey] = useState('');
  const [keyInfo, setKeyInfo] = useState<Key | null>(null);
  const [authHistory, setAuthHistory] = useState<AuthHistory[]>([]);
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [allKeys, setAllKeys] = useState<Key[]>([]);
  const [showAllKeys, setShowAllKeys] = useState(true);
  const [showSystemInfo, setShowSystemInfo] = useState(false);

  useEffect(() => {
    handleGetAllKeys();
  }, []);


  useEffect(() => {
    if (lastCreatedKey) {
      setSearchKey(lastCreatedKey.key);
      handleSearch(lastCreatedKey.key);
    }
  }, [lastCreatedKey]);

  const handleGetAllKeys = async () => {
    setLoading(true);
    try {
      const keys = await getAllKeys();
      setAllKeys(keys);
      setShowAllKeys(true);
      setKeyInfo(null);
      setSystemInfo(null);
    } catch (error) {
      console.error('Error fetching all keys:', error);
      toast.error('Failed to fetch keys');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (keyToSearch: string = searchKey) => {
    if (!keyToSearch) return;
    
    setLoading(true);
    try {
      const info = await getKeyInfo(keyToSearch);
      setKeyInfo(info);
      setShowAllKeys(false);
      setSystemInfo(null);
      
      const history = await getAuthHistory(keyToSearch);
      setAuthHistory(history);
    } catch (error) {
      console.error('Search error:', error);
      toast.error('Failed to fetch key information');
      setKeyInfo(null);
      setAuthHistory([]);
    } finally {
      setLoading(false);
    }
  };

  const handleViewSystemInfo = async (key: Key) => {
    try {
      const info = await getSystemInfo(key.id);
      setSystemInfo(info);
      setShowSystemInfo(true);
    } catch (error) {
      if (error.response?.data?.error === 'Системная информация для этого ключа отсутствует') {
        toast.error('System information is not available for this key');
      } else {
        toast.error('Failed to fetch system information');
      }
    }
  };

  const handleFreeze = async (key: Key) => {
    try {
      await freezeKey(key.key);
      toast.success('Key frozen successfully');
      handleGetAllKeys();
    } catch (error) {
      toast.error('Failed to freeze key');
    }
  };

  const handleBan = async (key: Key) => {
    try {
      await banKey(key.key);
      toast.success('Key banned successfully');
      handleGetAllKeys();
    } catch (error) {
      toast.error('Failed to ban key');
    }
  };

  const handleResetHWID = async (key: Key) => {
    try {
      await resetHWID(key.key);
      toast.success('HWID reset successfully');
      handleGetAllKeys();
    } catch (error) {
      toast.error('Failed to reset HWID');
    }
  };

  const handleAddTime = async (key: Key) => {
    const days = prompt('Enter number of days to add:');
    if (!days) return;
    
    try {
      await addTime(key.key, parseInt(days));
      toast.success('Time added successfully');
      handleGetAllKeys();
    } catch (error) {
      toast.error('Failed to add time');
    }
  };

  const getStatusBadge = (key: Key) => {
    if (key.is_banned) return <span className="badge-red">Banned</span>;
    if (key.is_frozen) return <span className="badge-yellow">Frozen</span>;
    return <span className="badge-green">Active</span>;
  };

  return (
    <div className="p-8">
      {}
      <div className="max-w-full mx-auto mb-8">
        <div className="relative flex gap-2">
          <div className="relative flex-1">
            <input
              type="text"
              value={searchKey}
              onChange={(e) => setSearchKey(e.target.value)}
              placeholder="Enter license key..."
              className="input-field pl-12 h-12 text-lg"
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          </div>
          <button
            onClick={() => handleSearch()}
            disabled={loading || !searchKey}
            className="btn-primary h-12 px-8 text-lg font-medium flex items-center justify-center min-w-[120px]"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin mr-2">
                  <RefreshCw className="h-5 w-5" />
                </div>
                Searching
              </div>
            ) : (
              'Search'
            )}
          </button>
          <button
            onClick={handleGetAllKeys}
            disabled={loading}
            className="btn-secondary h-12 px-6 text-lg font-medium flex items-center justify-center"
            title="View all keys"
          >
            <List className="h-5 w-5" />
          </button>
        </div>
      </div>

      {}
      {showAllKeys && (
        <div className="space-y-8 animate-fade-in">
          <div className="bg-gradient-to-br from-card/80 to-card/60 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-border/20">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-border">
                <thead>
                  <tr>
                    <th className="table-header">#</th>
                    <th className="table-header">Key</th>
                    <th className="table-header">HWID</th>
                    <th className="table-header">IP</th>
                    <th className="table-header">Expires</th>
                    <th className="table-header">Status</th>
                    <th className="table-header">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {allKeys.map((key, index) => (
                    <tr key={key.id} className="hover:bg-muted/50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                        {key.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap font-mono text-sm text-foreground">
                        {key.key}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                        {key.hwid || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                        {key.ip || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                        {key.expires_at}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {getStatusBadge(key)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleViewSystemInfo(key)}
                            className="btn-secondary p-2"
                            title="System Info"
                          >
                            <Monitor className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleFreeze(key)}
                            className="btn-warning p-2"
                            title={key.is_frozen ? 'Unfreeze' : 'Freeze'}
                          >
                            <Shield className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleBan(key)}
                            className="btn-danger p-2"
                            title={key.is_banned ? 'Unban' : 'Ban'}
                          >
                            <Ban className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleResetHWID(key)}
                            className="btn-primary p-2"
                            title="Reset HWID"
                          >
                            <RefreshCw className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleAddTime(key)}
                            className="btn-success p-2"
                            title="Add Time"
                          >
                            <Clock className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {}
      {showSystemInfo && systemInfo && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-card p-8 rounded-xl shadow-xl max-w-2xl w-full mx-4 relative animate-fade-in">
            <button
              onClick={() => setShowSystemInfo(false)}
              className="absolute top-4 right-4 text-muted-foreground hover:text-foreground"
            >
              ✕
            </button>
            <h3 className="text-xl font-semibold mb-6">System Information</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">Processor</p>
                  <p className="text-foreground">{systemInfo.processor}</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">Motherboard</p>
                  <p className="text-foreground">{systemInfo.motherboard}</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">BIOS</p>
                  <p className="text-foreground">{systemInfo.bios_version} ({systemInfo.bios_date})</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">Storage</p>
                  <p className="text-foreground">{systemInfo.disk}</p>
                </div>
              </div>
              <div className="space-y-2">
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">GPU</p>
                  <p className="text-foreground">{systemInfo.gpu}</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">RAM</p>
                  <p className="text-foreground">{systemInfo.ram}</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">Operating System</p>
                  <p className="text-foreground">{systemInfo.os_name} ({systemInfo.arch})</p>
                </div>
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium text-muted-foreground">Network</p>
                  <p className="text-foreground">MAC: {systemInfo.mac_address}</p>
                  <p className="text-foreground">IP: {systemInfo.ip}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}