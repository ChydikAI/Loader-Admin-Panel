import { ReactNode } from 'react';

export interface Key {
  id: number;
  key: string;
  expires_at: string;
  is_frozen: boolean;
  is_banned: boolean;
  is_bsod: boolean;
  created_at: string;
  hwid?: string | null;
  ip?: string | null;
}

export interface SystemInfo {
  processor: string;
  motherboard: string;
  bios_version: string;
  bios_date: string;
  disk: string;
  gpu: string;
  ram: string;
  monitor: string;
  os_name: string;
  arch: string;
  mac_address: string;
  ip: string;
}

export interface AuthHistory {
  timestamp: string;
  ip: string;
  status: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export interface Settings {
  loader_version: string;
}

export interface TabProps {
  children: ReactNode;
  value: string;
  activeTab: string;
  onClick: (value: string) => void;
  icon: ReactNode;
}