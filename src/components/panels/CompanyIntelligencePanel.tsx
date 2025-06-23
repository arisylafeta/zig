"use client";

/**
 * @file CompanyIntelligencePanel.tsx
 * @description Panel component for displaying company intelligence data
 */

import React from 'react';
import { PanelProps } from '@/types/mosaic';

/**
 * Panel component for company intelligence
 * 
 * @param id - ID of the panel
 * @param path - Path to the panel in the Mosaic tree
 */
export function CompanyIntelligencePanel({ id, path }: PanelProps) {
  return (
    <div className="panel-content p-4">
      <h2 className="text-xl font-semibold mb-4">Company Intelligence</h2>
      <div className="intelligence-content">
        <div className="mb-4 p-3 border rounded">
          <h3 className="font-medium mb-2">Company Overview</h3>
          <p className="text-gray-600">Select a company to view detailed intelligence</p>
        </div>
        <div className="mb-4 p-3 border rounded">
          <h3 className="font-medium mb-2">Market Position</h3>
          <p className="text-gray-600">Industry standing and competitive analysis</p>
        </div>
        <div className="mb-4 p-3 border rounded">
          <h3 className="font-medium mb-2">Key Personnel</h3>
          <p className="text-gray-600">Leadership and decision makers</p>
        </div>
        <div className="p-3 border rounded">
          <h3 className="font-medium mb-2">Financial Performance</h3>
          <p className="text-gray-600">Revenue, growth, and financial metrics</p>
        </div>
      </div>
    </div>
  );
}
