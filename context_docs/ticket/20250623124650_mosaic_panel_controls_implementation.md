# Ticket: Mosaic Panel Controls Implementation

## Overview
Implement enhanced panel controls for the React Mosaic layout, including maximize, minimize, and close functionality for each panel. The controls should be integrated with the existing MosaicToolbarControls component and provide a smooth user experience.

## Requirements

### Panel Controls
1. **Maximize Button**
   - Expand a panel to fill the entire mosaic layout area
   - Store the previous layout state to restore when minimizing
   - Visual indicator when a panel is maximized

2. **Minimize Button**
   - Restore a maximized panel to its previous size and position
   - Only active/visible when a panel is in maximized state
   - Smooth transition between states

3. **Close Button**
   - Remove a panel from the layout
   - Confirm before closing if panel has unsaved changes
   - Update available panels list in toolbar

### Implementation Details

#### Technical Approach
1. Extend the MosaicToolbarControls component to include the new controls
2. Use React Mosaic's built-in functionality where possible:
   - `ExpandButton` for maximize
   - `RemoveButton` for close
3. Implement custom state management for minimize functionality:
   - Store previous layout state in context
   - Create custom minimize button component

#### State Management
1. Add to MosaicProvider:
   - `maximizedPanel` - ID of currently maximized panel (null if none)
   - `previousLayout` - Layout state before maximization
   - `maximizePanel(id)` - Function to maximize a panel
   - `minimizePanel()` - Function to restore previous layout

#### UI/UX Considerations
1. Use consistent icons for controls (suggested: Material Icons)
2. Add tooltips for each control
3. Implement smooth transitions between states
4. Consider keyboard shortcuts for common actions

## Research Notes

### React Mosaic API
The react-mosaic-component library provides several useful components:

```tsx
import {
  Mosaic,
  MosaicWindow,
  MosaicNode,
  getNodeAtPath,
  updateTree,
  Corner,
  MosaicDirection,
  MosaicBranch,
  MosaicZeroState,
  ExpandButton,
  RemoveButton,
  SplitButton,
  ReplaceButton
} from 'react-mosaic-component';
```

### Maximize/Minimize Implementation
The built-in `ExpandButton` component can be used for maximization, but it doesn't store the previous state for minimization. We'll need to:

1. Create a custom maximize function:
```tsx
const maximizePanel = (id: PanelId) => {
  // Store current layout
  setPreviousLayout(layout);
  
  // Set new layout with just the maximized panel
  setLayout(id);
  
  // Track which panel is maximized
  setMaximizedPanel(id);
};
```

2. Create a custom minimize function:
```tsx
const minimizePanel = () => {
  // Restore previous layout
  setLayout(previousLayout);
  
  // Clear maximized panel tracking
  setMaximizedPanel(null);
};
```

### Custom Controls Component
We'll need to create a custom controls component that extends the current MosaicToolbarControls:

```tsx
interface EnhancedToolbarControlsProps {
  panelId: PanelId;
  path: MosaicBranch[];
  closable?: boolean;
}

export const EnhancedToolbarControls: React.FC<EnhancedToolbarControlsProps> = ({
  panelId,
  path,
  closable = true
}) => {
  const { maximizedPanel, maximizePanel, minimizePanel } = useMosaic();
  const isMaximized = maximizedPanel === panelId;
  
  return (
    <>
      {isMaximized ? (
        <MinimizeButton onClick={() => minimizePanel()} />
      ) : (
        <ExpandButton onClick={() => maximizePanel(panelId)} />
      )}
      {closable && <RemoveButton />}
    </>
  );
};
```

## Acceptance Criteria
1. Users can maximize any panel to fill the entire layout area
2. Users can minimize a maximized panel to restore the previous layout
3. Users can close panels they no longer need
4. The toolbar updates to show only available panels
5. Controls have appropriate tooltips and visual indicators
6. Transitions between states are smooth and visually pleasing

## Estimated Effort
- Research: 2 hours
- Implementation: 6 hours
- Testing: 2 hours
- Documentation: 1 hour
- Total: 11 hours
