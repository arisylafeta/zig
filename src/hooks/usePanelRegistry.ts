"use client";

/**
 * @file usePanelRegistry.ts
 * @description Hook for managing the registry of available panels.
 * This hook provides a way to register, unregister, and access panel
 * configurations throughout the application. It serves as a central
 * registry for all panels that can be displayed in the Mosaic layout.
 * 
 * @function usePanelRegistry - Hook to access and manage the panel registry
 * @function registerPanel - Register a new panel configuration
 * @function unregisterPanel - Remove a panel from the registry
 * @function getPanel - Get a panel configuration by ID
 */

import { useState, useCallback } from 'react';
import { PanelConfig, PanelId, PanelRegistry } from '@/types/mosaic';

/**
 * Hook for managing the registry of available panels
 * 
 * @param initialPanels - Initial panel configurations
 * @returns Object with panel registry and methods to manipulate it
 */
export function usePanelRegistry(initialPanels: PanelRegistry = {}) {
  // State for the panel registry
  const [panels, setPanels] = useState<PanelRegistry>(initialPanels);

  /**
   * Register a new panel configuration
   * 
   * @param config - Panel configuration to register
   */
  const registerPanel = useCallback((config: PanelConfig) => {
    setPanels((current) => ({
      ...current,
      [config.id]: config,
    }));
  }, []);

  /**
   * Register multiple panel configurations at once
   * 
   * @param configs - Array of panel configurations to register
   */
  const registerPanels = useCallback((configs: PanelConfig[]) => {
    setPanels((current) => {
      const newPanels = { ...current };
      
      configs.forEach((config) => {
        newPanels[config.id] = config;
      });
      
      return newPanels;
    });
  }, []);

  /**
   * Unregister a panel by ID
   * 
   * @param id - ID of the panel to unregister
   */
  const unregisterPanel = useCallback((id: PanelId) => {
    setPanels((current) => {
      const newPanels = { ...current };
      delete newPanels[id];
      return newPanels;
    });
  }, []);

  /**
   * Get a panel configuration by ID
   * 
   * @param id - ID of the panel to get
   * @returns Panel configuration or undefined if not found
   */
  const getPanel = useCallback((id: PanelId) => {
    return panels[id];
  }, [panels]);

  return {
    panels,
    registerPanel,
    registerPanels,
    unregisterPanel,
    getPanel,
  };
}
