import axios from 'axios';
import { Key, AuthHistory, ApiResponse, SystemInfo, Settings } from './types';

const API_BASE_URL = 'http://127.0.0.1:5000';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: false
});


axiosInstance.interceptors.response.use(
  (response) => {

    if (response.data.hasOwnProperty('data')) {
      return response.data;
    }

    return { data: response.data };
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const getAllKeys = async (): Promise<Key[]> => {
  try {
    const response = await axiosInstance.get<Key[]>('/api/keys');
    return response.data;
  } catch (error) {
    console.error('Error getting all keys:', error);
    throw error;
  }
};

export const createKey = async (duration: string): Promise<Key> => {
  try {
    const response = await axiosInstance.post<ApiResponse<Key>>('/api/keys', { duration });
    return response.data;
  } catch (error) {
    console.error('Error creating key:', error);
    throw error;
  }
};

export const getKeyInfo = async (key: string): Promise<Key> => {
  try {
    const response = await axiosInstance.get<ApiResponse<Key>>(`/api/keys/${key}`);
    return response.data;
  } catch (error) {
    console.error('Error getting key info:', error);
    throw error;
  }
};

export const getAuthHistory = async (key: string): Promise<AuthHistory[]> => {
  try {
    const response = await axiosInstance.get<AuthHistory[]>(`/api/keys/${key}/auth_history`);
    return response.data;
  } catch (error) {
    console.error('Error getting auth history:', error);
    throw error;
  }
};

export const getSystemInfo = async (id: number): Promise<SystemInfo> => {
  try {
    const response = await axiosInstance.get<SystemInfo>(`/api/key/${id}/system_info`);
    if (response.data.error) {
      throw new Error(response.data.error);
    }
    return response.data;
  } catch (error) {
    console.error('Error getting system info:', error);
    throw error;
  }
};

export const freezeKey = async (key: string): Promise<void> => {
  try {
    await axiosInstance.post(`/api/keys/${key}/freeze`);
  } catch (error) {
    console.error('Error freezing key:', error);
    throw error;
  }
};

export const banKey = async (key: string): Promise<void> => {
  try {
    await axiosInstance.post(`/api/keys/${key}/ban`);
  } catch (error) {
    console.error('Error banning key:', error);
    throw error;
  }
};

export const resetHWID = async (key: string): Promise<void> => {
  try {
    await axiosInstance.post(`/api/keys/${key}/reset_hwid`);
  } catch (error) {
    console.error('Error resetting HWID:', error);
    throw error;
  }
};

export const addTime = async (key: string, days: number): Promise<void> => {
  try {
    await axiosInstance.post(`/api/keys/${key}/add_time`, { days });
  } catch (error) {
    console.error('Error adding time:', error);
    throw error;
  }
};

export const updateLoaderVersion = async (version: string): Promise<void> => {
  try {
    await axiosInstance.put('/api/settings/loader_version', { loader_version: version });
  } catch (error) {
    console.error('Error updating loader version:', error);
    throw error;
  }
};