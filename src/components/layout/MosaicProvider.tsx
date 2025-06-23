"use client";

/**
 * @file MosaicProvider.tsx
 * @description Context provider for managing the Mosaic layout state.
 * This component provides the state and actions for manipulating the
 * panel layout throughout the application. It serves as the central
 * state management for the tiling window system.
 * 
 * @component MosaicProvider - Provides context for Mosaic layout management
 * @function useMosaic - Hook to access the Mosaic context
 * @function findNodeInTree - Helper to locate a node in the Mosaic tree
 * @function getVisiblePanelsFromTree - Helper to extract visible panel IDs
 */

import React, { createContext, useContext, useState, useCallback } from 'react';
import { MosaicNode, MosaicDirection, getNodeAtPath, updateTree } from 'react-mosaic-component';
import { MosaicContextType, PanelId, PanelPosition } from '@/types/mosaic';

// Create context with undefined default value
const MosaicContext = createContext<MosaicContextType | undefined>(undefined);

/**
 * Provider component for Mosaic layout state and actions
 * 
 * @param children - Child components that will have access to the context
 */
export function MosaicProvider({ children }: { children: React.ReactNode }) {
  // State for the Mosaic layout
  const [layout, setLayout] = useState<MosaicNode<PanelId>>({
    direction: 'row',
    first: {
      direction: 'column',
      first: 'peopleSearch',
      second: 'companySearch',
      splitPercentage: 50
    },
    second: {
      direction: 'column',
      first: 'peopleIntelligence',
      second: 'companyIntelligence',
      splitPercentage: 50
    },
    splitPercentage: 50,
  });
  
  /**
   * Helper function to find the path to a node in the tree
   * 
   * @param node - Current node to check
   * @param id - ID of the panel to find
   * @param currentPath - Current path being built
   * @returns Path to the node or null if not found
   */
  const findPathToNode = useCallback(
    (node: MosaicNode<PanelId>, id: PanelId, currentPath: ('first' | 'second')[] = []): ('first' | 'second')[] | null => {
      // If this is the node we're looking for, return the path
      if (node === id) {
        return currentPath;
      }
      
      // If this is a leaf node and not the one we're looking for, return null
      if (typeof node === 'string' || typeof node === 'number') {
        return null;
      }
      
      // Check first child
      const firstPath = findPathToNode(node.first, id, [...currentPath, 'first']);
      if (firstPath) {
        return firstPath;
      }
      
      // Check second child
      const secondPath = findPathToNode(node.second, id, [...currentPath, 'second']);
      if (secondPath) {
        return secondPath;
      }
      
      // Not found in this subtree
      return null;
    },
    []
  );
  
  /**
   * Helper function to extract visible panel IDs from a tree
   * 
   * @param node - Current node to check
   * @returns Array of visible panel IDs
   */
  const getVisiblePanelsFromTree = useCallback((node: MosaicNode<PanelId>): PanelId[] => {
    // If this is a leaf node, return it as an array
    if (typeof node === 'string' || typeof node === 'number') {
      return [node];
    }
    
    // Otherwise, recursively get panels from children
    return [
      ...getVisiblePanelsFromTree(node.first),
      ...getVisiblePanelsFromTree(node.second),
    ];
  }, []);
  
  /**
   * Helper function to remove a node from a tree
   * 
   * @param node - Current node to check
   * @param id - ID of the panel to remove
   * @returns Updated node with the panel removed
   */
  const removeNodeFromTree = useCallback(
    (node: MosaicNode<PanelId>, id: PanelId): MosaicNode<PanelId> | null => {
      // If this is the node to remove, return null
      if (node === id) {
        return null;
      }
      
      // If this is a leaf node and not the one to remove, return it
      if (typeof node === 'string' || typeof node === 'number') {
        return node;
      }
      
      // Check first child
      if (node.first === id) {
        return node.second;
      }
      
      // Check second child
      if (node.second === id) {
        return node.first;
      }
      
      // Recursively check children
      const first = typeof node.first === 'string' || typeof node.first === 'number'
        ? node.first
        : removeNodeFromTree(node.first, id);
        
      const second = typeof node.second === 'string' || typeof node.second === 'number'
        ? node.second
        : removeNodeFromTree(node.second, id);
        
      // If either child is null after removal, return the other child
      if (first === null) return second;
      if (second === null) return first;
      
      // Otherwise return the updated node
      return {
        ...node,
        first,
        second,
      };
    },
    []
  );

  /**
   * Get all visible panel IDs from the current layout
   * 
   * @returns Array of visible panel IDs
   */
  const getVisiblePanels = useCallback((): PanelId[] => {
    return getVisiblePanelsFromTree(layout);
  }, [layout, getVisiblePanelsFromTree]);

  /**
   * Add a panel to the layout at the specified position
   * 
   * @param id - ID of the panel to add
   * @param position - Position to add the panel (left, right, top, bottom)
   */
  const addPanel = useCallback((id: PanelId, position: PanelPosition) => {
    setLayout((currentLayout) => {
      // Determine direction based on position
      const direction: MosaicDirection = 
        position === 'left' || position === 'right' ? 'row' : 'column';
      
      // Create new layout with the panel at the specified position
      const newLayout: MosaicNode<PanelId> = {
        direction,
        first: position === 'left' || position === 'top' ? id : currentLayout,
        second: position === 'right' || position === 'bottom' ? id : currentLayout,
        splitPercentage: 30,
      };
      
      return newLayout;
    });
  }, []);

  /**
   * Remove a panel from the layout
   * 
   * @param id - ID of the panel to remove
   */
  const removePanel = useCallback((id: PanelId) => {
    setLayout((currentLayout) => {
      // If it's just the panel we want to remove, return a default panel
      if (currentLayout === id) {
        return 'peopleSearch' as PanelId; // Default to people search panel
      }

      // If the layout is a node, check its children
      if (typeof currentLayout !== 'string' && typeof currentLayout !== 'number') {
        // If first child is the panel to remove, replace with second child
        if (currentLayout.first === id) {
          return currentLayout.second;
        }
        
        // If second child is the panel to remove, replace with first child
        if (currentLayout.second === id) {
          return currentLayout.first;
        }
        
        // Otherwise, recursively check children
        return {
          ...currentLayout,
          first: typeof currentLayout.first === 'string' || typeof currentLayout.first === 'number'
            ? currentLayout.first
            : removeNodeFromTree(currentLayout.first, id) || 'chat',
          second: typeof currentLayout.second === 'string' || typeof currentLayout.second === 'number'
            ? currentLayout.second
            : removeNodeFromTree(currentLayout.second, id) || 'chat',
        };
      }
      
      // If we get here, the panel wasn't found
      return currentLayout;
    });
  }, [removeNodeFromTree]);

  /**
   * Resize a panel to the specified percentage
   * 
   * @param id - ID of the panel to resize
   * @param percentage - New size as percentage (1-100)
   */
  const resizePanel = useCallback((id: PanelId, percentage: number) => {
    setLayout((currentLayout) => {
      // Find the parent node containing this panel
      const path = findPathToNode(currentLayout, id);
      
      if (!path) {
        return currentLayout;
      }
      
      // Get the parent node
      const parentPath = path.slice(0, -1);
      const parentNode = getNodeAtPath(currentLayout, parentPath);
      
      if (!parentNode || typeof parentNode === 'string' || typeof parentNode === 'number') {
        return currentLayout;
      }
      
      // Update the split percentage
      const updates = [{
        path: parentPath,
        spec: {
          splitPercentage: { $set: percentage }
        }
      }];
      
      return updateTree(currentLayout, updates);
    });
  }, [findPathToNode]);

  /**
   * Check if a panel is currently visible in the layout
   * 
   * @param id - ID of the panel to check
   * @returns True if the panel is visible
   */
  const isPanelVisible = useCallback((id: PanelId): boolean => {
    return getVisiblePanels().includes(id);
  }, [getVisiblePanels]);

  // Create the context value
  const contextValue: MosaicContextType = {
    layout,
    setLayout: setLayout as (layout: MosaicNode<PanelId> | null) => void,
    addPanel,
    removePanel,
    resizePanel,
    getVisiblePanels,
    isPanelVisible,
  };

  return (
    <MosaicContext.Provider value={contextValue}>
      {children}
    </MosaicContext.Provider>
  );
}

/**
 * Hook to access the Mosaic context
 * 
 * @returns The Mosaic context
 * @throws Error if used outside of a MosaicProvider
 */
export function useMosaic(): MosaicContextType {
  const context = useContext(MosaicContext);
  
  if (!context) {
    throw new Error('useMosaic must be used within a MosaicProvider');
  }
  
  return context;
}
