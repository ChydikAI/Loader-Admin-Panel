import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import { updateLoaderVersion } from '../api';
import { Loader2, Save } from 'lucide-react';

export default function Settings() {
  const [loaderVersion, setLoaderVersion] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpdateVersion = async () => {
    if (!loaderVersion) {
      toast.error('Please enter a loader version');
      return;
    }

    setLoading(true);
    try {
      await updateLoaderVersion(loaderVersion);
      toast.success('Loader version updated successfully');
      setLoaderVersion('');
    } catch (error) {
      toast.error('Failed to update loader version');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-gradient-to-br from-card/80 to-card/60 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-border/20">
          <h2 className="text-2xl font-semibold text-foreground mb-8">Settings</h2>
          
          <div className="space-y-8">
            {}
            <div className="space-y-4">
              <label className="block text-sm font-medium text-foreground">
                Loader Version
              </label>
              <div className="flex gap-4">
                <input
                  type="text"
                  value={loaderVersion}
                  onChange={(e) => setLoaderVersion(e.target.value)}
                  placeholder="Enter loader version..."
                  className="input-field flex-1 h-12 text-lg"
                />
                <button
                  onClick={handleUpdateVersion}
                  disabled={loading || !loaderVersion}
                  className="btn-primary h-12 px-8 text-lg font-medium flex items-center justify-center min-w-[160px]"
                >
                  {loading ? (
                    <div className="flex items-center">
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Updating...
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <Save className="w-5 h-5 mr-2" />
                      Update
                    </div>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}