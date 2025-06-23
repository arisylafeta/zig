/**
 * @file mosaic.ts
 * @description Type definitions for the React Mosaic integration.
 * This file contains type definitions for panel IDs, panel configurations,
 * and layout structures used throughout the Mosaic implementation.
 * These types ensure consistency across the application when working
 * with the tiling window manager.
 */

import { MosaicNode, MosaicPath } from 'react-mosaic-component';
import { ReactNode } from 'react';

/**
 * Unique identifier for a panel
 */
export type PanelId = string;

/**
 * Position where a panel can be placed
 */
export type PanelPosition = 'left' | 'right' | 'top' | 'bottom';

/**
 * Configuration for a panel
 */
export interface PanelConfig {
  /** Unique identifier for the panel */
  id: PanelId;
  /** Display title for the panel */
  title: string;
  /** React component to render inside the panel */
  component: React.ComponentType<PanelProps>;
  /** Default size of the panel as a percentage (1-100) */
  defaultSize?: number;
  /** Minimum size of the panel as a percentage (1-100) */
  minSize?: number;
  /** Maximum size of the panel as a percentage (1-100) */
  maxSize?: number;
  /** Icon to display in the panel toolbar */
  icon?: ReactNode;
  /** Whether the panel can be closed */
  closable?: boolean;
  /** Whether the panel can be dragged */
  draggable?: boolean;
}

/**
 * Props passed to panel components
 */
export interface PanelProps {
  /** ID of the panel */
  id: PanelId;
  /** Path to the panel in the Mosaic tree */
  path?: MosaicPath;
}

/**
 * Registry of available panels
 */
export type PanelRegistry = Record<PanelId, PanelConfig>;

/**
 * Context for the Mosaic layout
 */
export interface MosaicContextType {
  /** Current layout structure */
  layout: MosaicNode<PanelId> | null;
  /** Set the layout structure */
  setLayout: (layout: MosaicNode<PanelId> | null) => void;
  /** Add a panel to the layout */
  addPanel: (id: PanelId, position: PanelPosition) => void;
  /** Remove a panel from the layout */
  removePanel: (id: PanelId) => void;
  /** Resize a panel */
  resizePanel: (id: PanelId, percentage: number) => void;
  /** Get all visible panel IDs */
  getVisiblePanels: () => PanelId[];
  /** Check if a panel is visible */
  isPanelVisible: (id: PanelId) => boolean;
}
