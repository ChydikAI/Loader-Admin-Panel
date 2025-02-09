import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import { createKey } from '../api';
import { Clock, Infinity, Calendar, Loader2 } from 'lucide-react';
import { Key } from '../types';

interface CreateKeyProps {
  onKeyCreated?: (key: Key) => void;
}

export default function CreateKey({ onKeyCreated }: CreateKeyProps) {
  const [durationType, setDurationType] = useState<'lifetime' | 'custom'>('custom');
  const [customValue, setCustomValue] = useState('');
  const [customUnit, setCustomUnit] = useState<'days' | 'hours' | 'minutes'>('days');
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    if (durationType === 'custom' && !customValue) {
      toast.error('Please enter a duration value');
      return;
    }

    setLoading(true);
    try {
      const duration = durationType === 'lifetime' 
        ? 'LifeTime'
        : `${customValue} ${customUnit}`;
        
      const response = await createKey(duration);
      
      toast.success(
        <div className="flex flex-col gap-2">
          <div className="font-semibold">Key Created Successfully</div>
          <div className="font-mono text-sm">{response.key}</div>
          <div className="text-sm">
            Expires: {response.expires_at === 'never' 
              ? 'Never' 
              : new Date(response.expires_at).toLocaleString()
            }
          </div>
        </div>,
        { duration: 5000 }
      );

      
      if (onKeyCreated) {
        onKeyCreated(response);
      }

   
      if (durationType === 'custom') {
        setCustomValue('');
      }
    } catch (error) {
      toast.error('Failed to create key');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-gradient-to-br from-card/80 to-card/60 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-border/20">
          <h2 className="text-2xl font-semibold text-foreground mb-8">Create New License Key</h2>
          
          <div className="space-y-8">
            {}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                onClick={() => setDurationType('lifetime')}
                className={`p-6 rounded-xl border-2 transition-all duration-200 ${
                  durationType === 'lifetime'
                    ? 'border-primary bg-primary/10'
                    : 'border-border hover:border-primary/50 hover:bg-muted/50'
                }`}
              >
                <div className="flex items-center">
                  <div className={`p-3 rounded-lg ${
                    durationType === 'lifetime'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-muted-foreground'
                  }`}>
                    <Infinity className="h-6 w-6" />
                  </div>
                  <div className="ml-4 text-left">
                    <p className="font-medium text-foreground">Lifetime</p>
                    <p className="text-sm text-muted-foreground">Never expires</p>
                  </div>
                </div>
              </button>

              <button
                onClick={() => setDurationType('custom')}
                className={`p-6 rounded-xl border-2 transition-all duration-200 ${
                  durationType === 'custom'
                    ? 'border-primary bg-primary/10'
                    : 'border-border hover:border-primary/50 hover:bg-muted/50'
                }`}
              >
                <div className="flex items-center">
                  <div className={`p-3 rounded-lg ${
                    durationType === 'custom'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-muted-foreground'
                  }`}>
                    <Calendar className="h-6 w-6" />
                  </div>
                  <div className="ml-4 text-left">
                    <p className="font-medium text-foreground">Custom Duration</p>
                    <p className="text-sm text-muted-foreground">Set specific time period</p>
                  </div>
                </div>
              </button>
            </div>

            {}
            {durationType === 'custom' && (
              <div className="grid grid-cols-2 gap-4 animate-fade-in">
                <div>
                  <label htmlFor="customValue" className="block text-sm font-medium text-foreground mb-2">
                    Duration
                  </label>
                  <input
                    type="number"
                    id="customValue"
                    value={customValue}
                    onChange={(e) => setCustomValue(e.target.value)}
                    className="input-field h-12 text-lg"
                    placeholder="Enter duration"
                    min="1"
                  />
                </div>
                <div>
                  <label htmlFor="customUnit" className="block text-sm font-medium text-foreground mb-2">
                    Unit
                  </label>
                  <select
                    id="customUnit"
                    value={customUnit}
                    onChange={(e) => setCustomUnit(e.target.value as 'days' | 'hours' | 'minutes')}
                    className="input-field h-12 text-lg"
                  >
                    <option value="days">Days</option>
                    <option value="hours">Hours</option>
                    <option value="minutes">Minutes</option>
                  </select>
                </div>
              </div>
            )}

            {}
            <div className="pt-4">
              <button
                onClick={handleCreate}
                disabled={loading || (durationType === 'custom' && !customValue)}
                className="btn-primary w-full h-12 text-lg font-medium flex items-center justify-center"
              >
                {loading ? (
                  <div className="flex items-center">
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Creating...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <Clock className="w-5 h-5 mr-2" />
                    Create License Key
                  </div>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}