"use client";

/**
 * @file MosaicLayout.tsx
 * @description Main layout component using React Mosaic for tiling window management.
 * This component renders the Mosaic interface with all registered panels and
 * handles the rendering of each panel based on its ID. It uses the MosaicContext
 * for state management and panel registration.
 * 
 * @component MosaicLayout - Renders the tiling window manager interface
 * @function renderTile - Renders a specific panel based on its ID
 * @function renderToolbar - Renders the toolbar for a panel
 */

import React, { useCallback } from 'react';
import {
  Mosaic,
  MosaicBranch,
  MosaicWindow,
} from 'react-mosaic-component';
import { useMosaic } from './MosaicProvider';
import { PanelId, PanelRegistry } from '@/types/mosaic';
import MosaicToolbarControls from './MosaicToolbarControls';
import MosaicToolbar from './MosaicToolbar';
import 'react-mosaic-component/react-mosaic-component.css';

interface MosaicLayoutProps {
  /** Registry of available panels */
  panelRegistry: PanelRegistry;
  /** Additional CSS class names */
  className?: string;
}

/**
 * Main layout component that renders the Mosaic tiling window manager
 * 
 * @param panelRegistry - Registry of available panels
 * @param className - Additional CSS class names
 */
export function MosaicLayout({ panelRegistry, className = '' }: MosaicLayoutProps) {
  const { layout, setLayout } = useMosaic();

  /**
   * Render a specific panel based on its ID
   * 
   * @param id - ID of the panel to render
   * @param path - Path to the panel in the Mosaic tree
   * @returns Rendered panel component
   */
  const renderTile = (id: string, path: MosaicBranch[]) => {
    // Get panel config from registry
    const panelConfig = panelRegistry[id];
    
    // If panel doesn't exist in registry, render placeholder
    if (!panelConfig) {
      return (
        <MosaicWindow
          key={id}
          path={path}
          title={`Unknown Panel: ${id}`}
          createNode={createNode}
        >
          <div className="p-4">
            <p>Panel not found in registry</p>
          </div>
        </MosaicWindow>
      );
    }
    
    // Get panel component and props
    const Panel = panelConfig.component;
    const title = panelConfig.title || id;
    const draggable = panelConfig.draggable !== false;
    
    return (
      <MosaicWindow
        key={id}
        path={path}
        title={title}
        draggable={draggable}
        createNode={createNode}
        renderToolbar={(props, draggable) => renderToolbar(props, draggable, panelConfig)}
      >
        <Panel id={id} path={path} />
      </MosaicWindow>
    );
  };

  /**
   * Create a new node/panel when requested by Split or Replace actions
   * 
   * @returns ID of the new panel to create
   */
  const createNode = useCallback((): PanelId => {
    // Return a panel from our registry that we want to add by default
    // We'll update this later to show a selection dialog
    return 'peopleSearch';
  }, []);

  /**
   * Render the toolbar for a panel
   * 
   * @param props - MosaicWindow props
   * @param draggable - Whether the panel is draggable
   * @param panelConfig - Configuration for the panel
   * @returns Rendered toolbar component
   */
  // Define a more specific type for MosaicWindow props
  interface MosaicWindowProps {
    title: string;
    path: MosaicBranch[];
    // Add other properties as needed
  }
  
  const renderToolbar = (props: MosaicWindowProps, draggable: boolean | undefined, panelConfig: PanelRegistry[string]) => {
    return (
      <div className="mosaic-window-toolbar">
        <div className="mosaic-window-title">
          {panelConfig.icon && (
            <span className="mosaic-window-icon mr-2">{panelConfig.icon}</span>
          )}
          <span>{panelConfig.title}</span>
        </div>
        <div className="mosaic-window-controls">
          {/* Use our custom toolbar controls with proper key props */}
          <MosaicToolbarControls 
            closable={panelConfig.closable !== false} 
          />
        </div>
      </div>
    );
  };

  return (
    <div className={`mosaic-layout ${className}`} style={{ height: '100vh', width: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Add the toolbar at the top */}
      <MosaicToolbar />
      
      {/* Mosaic layout takes remaining height */}
      <div style={{ flex: 1, position: 'relative' }}>
        <Mosaic<PanelId>
          renderTile={renderTile}
          value={layout}
          onChange={setLayout}
          className="mosaic-blueprint-theme"
        />
      </div>
    </div>
  );
}
