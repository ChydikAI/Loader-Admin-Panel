import React from 'react';
import { TabProps } from '../types';

export function Tab({ children, value, activeTab, onClick, icon }: TabProps) {
  return (
    <button
      onClick={() => onClick(value)}
      className={`${
        activeTab === value
          ? 'bg-primary text-primary-foreground shadow-lg'
          : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
      } flex items-center px-6 py-3 rounded-lg transition-all duration-200`}
    >
      {icon && <span className="mr-2">{icon}</span>}
      {children}
    </button>
  );
}