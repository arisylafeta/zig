"use client";

/**
 * @file PeopleIntelligencePanel.tsx
 * @description Panel component for displaying people intelligence data
 */

import React from 'react';
import { PanelProps } from '@/types/mosaic';

/**
 * Panel component for people intelligence
 * 
 * @param id - ID of the panel
 * @param path - Path to the panel in the Mosaic tree
 */
export function PeopleIntelligencePanel({ id, path }: PanelProps) {
  return (
    <div className="panel-content p-4">
      <h2 className="text-xl font-semibold mb-4">People Intelligence</h2>
      <div className="intelligence-content">
        <div className="mb-4 p-3 border rounded">
          <h3 className="font-medium mb-2">Person Overview</h3>
          <p className="text-gray-600">Select a person to view detailed intelligence</p>
        </div>
        <div className="mb-4 p-3 border rounded">
          <h3 className="font-medium mb-2">Career History</h3>
          <p className="text-gray-600">Professional background and experience</p>
        </div>
        <div className="mb-4 p-3 border rounded">
          <h3 className="font-medium mb-2">Skills & Expertise</h3>
          <p className="text-gray-600">Technical and professional capabilities</p>
        </div>
        <div className="p-3 border rounded">
          <h3 className="font-medium mb-2">Network Connections</h3>
          <p className="text-gray-600">Professional relationships and associations</p>
        </div>
      </div>
    </div>
  );
}
