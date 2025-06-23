"use client";

/**
 * @file ICPSearchPanel.tsx
 * @description Panel component for ICP (Ideal Customer Profile) search
 */

import React from 'react';
import { PanelProps } from '@/types/mosaic';

/**
 * Panel component for ICP search
 * 
 * @param id - ID of the panel
 * @param path - Path to the panel in the Mosaic tree
 */
export function ICPSearchPanel({ id, path }: PanelProps) {
  return (
    <div className="panel-content p-4">
      <h2 className="text-xl font-semibold mb-4">ICP Search</h2>
      <div className="search-form mb-4">
        <input 
          type="text" 
          placeholder="Search ideal customer profiles..." 
          className="w-full p-2 border rounded"
        />
        <button className="mt-2 bg-blue-500 text-white px-4 py-2 rounded">
          Search
        </button>
      </div>
      <div className="search-results">
        <p>Enter a search query to find ideal customer profiles</p>
      </div>
    </div>
  );
}
