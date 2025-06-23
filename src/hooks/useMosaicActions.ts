"use client";

/**
 * @file useMosaicActions.ts
 * @description Hook for registering Mosaic-related actions with CopilotKit.
 * This hook provides actions for manipulating the panel layout through
 * CopilotKit, allowing the AI to control the UI based on user queries.
 * The actions include adding, removing, and resizing panels, as well as
 * checking panel visibility.
 * 
 * @function useMosaicActions - Hook to register Mosaic actions with CopilotKit
 * @action addPanel - Add a new panel to the layout
 * @action removePanel - Remove a panel from the layout
 * @action resizePanel - Resize a panel
 * @action checkPanelVisibility - Check if a panel is visible
 */

import { useCopilotAction } from '@copilotkit/react-core';
import { useMosaic } from '@/components/layout/MosaicProvider';
import { PanelId, PanelPosition } from '@/types/mosaic';

/**
 * Hook to register Mosaic-related actions with CopilotKit
 * 
 * @returns void
 */
export function useMosaicActions() {
  const { addPanel, removePanel, resizePanel, isPanelVisible } = useMosaic();

  // Add panel action
  useCopilotAction({
    name: "addPanel",
    description: "Add a new panel to the layout",
    parameters: [
      { 
        name: "panelId", 
        type: "string", 
        description: "ID of the panel to add" 
      },
      { 
        name: "position", 
        type: "string", 
        enum: ["left", "right", "top", "bottom"], 
        description: "Position to add the panel" 
      }
    ],
    handler: ({ panelId, position }) => {
      // Validate position
      const validPosition = ['left', 'right', 'top', 'bottom'].includes(position) 
        ? position as PanelPosition 
        : 'right';
      
      // Add the panel
      addPanel(panelId as PanelId, validPosition);
      
      return { 
        success: true, 
        message: `Added panel ${panelId} at ${position}` 
      };
    }
  });

  // Remove panel action
  useCopilotAction({
    name: "removePanel",
    description: "Remove a panel from the layout",
    parameters: [
      { 
        name: "panelId", 
        type: "string", 
        description: "ID of the panel to remove" 
      }
    ],
    handler: ({ panelId }) => {
      // Check if panel is visible before removing
      if (!isPanelVisible(panelId as PanelId)) {
        return { 
          success: false, 
          message: `Panel ${panelId} is not currently visible` 
        };
      }
      
      // Remove the panel
      removePanel(panelId as PanelId);
      
      return { 
        success: true, 
        message: `Removed panel ${panelId}` 
      };
    }
  });

  // Resize panel action
  useCopilotAction({
    name: "resizePanel",
    description: "Resize a panel",
    parameters: [
      { 
        name: "panelId", 
        type: "string", 
        description: "ID of the panel to resize" 
      },
      { 
        name: "percentage", 
        type: "number", 
        description: "New size as percentage (1-100)" 
      }
    ],
    handler: ({ panelId, percentage }) => {
      // Validate percentage
      const validPercentage = Math.min(Math.max(1, percentage), 100);
      
      // Check if panel is visible before resizing
      if (!isPanelVisible(panelId as PanelId)) {
        return { 
          success: false, 
          message: `Panel ${panelId} is not currently visible` 
        };
      }
      
      // Resize the panel
      resizePanel(panelId as PanelId, validPercentage);
      
      return { 
        success: true, 
        message: `Resized panel ${panelId} to ${validPercentage}%` 
      };
    }
  });

  // Check panel visibility action
  useCopilotAction({
    name: "checkPanelVisibility",
    description: "Check if a panel is currently visible in the layout",
    parameters: [
      { 
        name: "panelId", 
        type: "string", 
        description: "ID of the panel to check" 
      }
    ],
    handler: ({ panelId }) => {
      // Check if panel is visible
      const isVisible = isPanelVisible(panelId as PanelId);
      
      return { 
        success: true, 
        message: `Panel ${panelId} is ${isVisible ? 'visible' : 'not visible'}`,
        isVisible
      };
    }
  });
}
