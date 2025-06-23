"use client";

/**
 * @file MosaicToolbar.tsx
 * @description Main toolbar component for controlling Mosaic panels.
 * This component provides UI controls for adding, removing, and managing panels.
 */

import React from 'react';
import { useMosaic } from './MosaicProvider';
import { usePanelRegistry } from '@/hooks/usePanelRegistry';
import { PanelId, PanelPosition } from '@/types/mosaic';

interface MosaicToolbarProps {
  /** Additional CSS class names */
  className?: string;
}

/**
 * Toolbar component for controlling Mosaic panels
 * 
 * @param className - Additional CSS class names
 */
export function MosaicToolbar({ className = '' }: MosaicToolbarProps) {
  const { addPanel, removePanel, getVisiblePanels, isPanelVisible } = useMosaic();
  const { panels } = usePanelRegistry();
  
  // Get list of visible panels
  const visiblePanels = getVisiblePanels();
  
  // Get list of available panels that aren't currently visible
  const availablePanels = Object.entries(panels)
    .filter(([id]) => !visiblePanels.includes(id as PanelId))
    .map(([id, config]) => ({
      id: id as PanelId,
      title: config.title || id
    }));
  
  /**
   * Handle adding a new panel
   * 
   * @param id - ID of the panel to add
   * @param position - Position to add the panel
   */
  const handleAddPanel = (id: PanelId, position: PanelPosition = 'right') => {
    addPanel(id, position);
  };
  
  return (
    <div className={`mosaic-toolbar ${className}`} style={{ 
      padding: '8px 16px',
      background: '#f5f5f5',
      borderBottom: '1px solid #e0e0e0',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <div className="mosaic-toolbar-title">
        <h2 style={{ margin: 0, fontSize: '16px' }}>Panel Controls</h2>
      </div>
      
      <div className="mosaic-toolbar-controls" style={{ display: 'flex', gap: '8px' }}>
        {/* Add panel dropdown */}
        {availablePanels.length > 0 && (
          <div className="mosaic-toolbar-dropdown">
            <select 
              onChange={(e) => {
                const value = e.target.value;
                if (value) {
                  handleAddPanel(value as PanelId);
                  e.target.value = ''; // Reset select
                }
              }}
              style={{
                padding: '4px 8px',
                borderRadius: '4px',
                border: '1px solid #ccc'
              }}
              defaultValue=""
            >
              <option value="" disabled>Add Panel</option>
              {availablePanels.map(panel => (
                <option key={panel.id} value={panel.id}>
                  {panel.title}
                </option>
              ))}
            </select>
          </div>
        )}
        
        {/* Position controls */}
        <div className="mosaic-toolbar-position-controls" style={{ display: 'flex', gap: '4px' }}>
          <button 
            onClick={() => handleAddPanel('chat', 'left')}
            disabled={isPanelVisible('chat')}
            style={{
              padding: '4px 8px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              background: '#fff',
              cursor: isPanelVisible('chat') ? 'not-allowed' : 'pointer',
              opacity: isPanelVisible('chat') ? 0.5 : 1
            }}
          >
            Add Left
          </button>
          <button 
            onClick={() => handleAddPanel('search', 'right')}
            disabled={isPanelVisible('search')}
            style={{
              padding: '4px 8px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              background: '#fff',
              cursor: isPanelVisible('search') ? 'not-allowed' : 'pointer',
              opacity: isPanelVisible('search') ? 0.5 : 1
            }}
          >
            Add Right
          </button>
        </div>
      </div>
    </div>
  );
}

export default MosaicToolbar;
