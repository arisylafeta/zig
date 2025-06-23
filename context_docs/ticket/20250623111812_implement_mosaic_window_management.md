# Implement React Mosaic Window Management Controls

## Summary
Add window management functionality to the existing React Mosaic implementation to allow users to manually add, remove, resize, and drag panels in the Mosaic layout. This will leverage the built-in React Mosaic controls and functionality rather than creating custom components.

## Description
The current implementation of React Mosaic in the Zig application provides basic tiling window functionality, but lacks user-facing controls for adding, removing, and rearranging panels. This ticket aims to implement these controls using React Mosaic's built-in functionality to provide a complete window management experience.

## Requirements
1. Implement toolbar controls using React Mosaic's built-in `defaultToolbarControls`
2. Add ability to add new panels from a selection of available panel types
3. Enable drag-and-drop functionality for panel rearrangement
4. Support panel resizing through the existing Mosaic interface
5. Ensure all controls are properly styled and accessible

## Implementation Details

### 1. Update MosaicWindow Configuration
- Modify the `renderToolbar` function in `MosaicLayout.tsx` to include the default toolbar controls:
  ```typescript
  import { 
    ExpandButton, 
    RemoveButton, 
    SplitButton, 
    ReplaceButton 
  } from 'react-mosaic-component';

  // In the renderToolbar function:
  const renderToolbar = (props: any, draggable: boolean | undefined, panelConfig: PanelRegistry[string]) => {
    return (
      <div className="mosaic-window-toolbar">
        <div className="mosaic-window-title">
          {panelConfig.icon && (
            <span className="mosaic-window-icon mr-2">{panelConfig.icon}</span>
          )}
          <span>{panelConfig.title}</span>
        </div>
        <div className="mosaic-window-controls">
          {panelConfig.closable !== false && <SplitButton />}
          {panelConfig.closable !== false && <ReplaceButton />}
          <ExpandButton />
          {panelConfig.closable !== false && <RemoveButton />}
        </div>
      </div>
    );
  };
  ```

### 2. Implement createNode Function
- Add a `createNode` function to the `MosaicWindow` component to enable adding new panels:
  ```typescript
  const createNode = () => {
    // Show a panel selection dialog or return a default panel ID
    return 'search'; // Default to adding a search panel
  };
  
  // In the renderTile function:
  return (
    <MosaicWindow<string>
      path={path}
      title={title}
      draggable={draggable}
      createNode={createNode}
      renderToolbar={(props, draggable) => renderToolbar(props, draggable, panelConfig)}
    >
      <Panel id={id} path={path} />
    </MosaicWindow>
  );
  ```

### 3. Add Panel Selection UI (Optional Enhancement)
- Create a simple panel selection dialog that appears when clicking the Split or Replace buttons
- Allow users to choose which panel type to add to the layout

### 4. Update MosaicApp Component
- Ensure the MosaicApp component properly passes all necessary props to enable these features
- Add appropriate CSS classes to ensure proper styling of the controls

## Technical Considerations
- Use the existing panel registry for managing available panels
- Ensure proper TypeScript typing for all components and functions
- Maintain compatibility with CopilotKit integration
- Follow the "use client" directive pattern for all client-side components

## Testing
- Verify that panels can be added using the Split button
- Confirm that panels can be removed using the Remove button
- Test drag-and-drop functionality for rearranging panels
- Ensure panel resizing works correctly
- Validate that the layout state is properly preserved

## References
- [React Mosaic GitHub Repository](https://github.com/nomcopter/react-mosaic)
- [React Mosaic Demo](https://nomcopter.github.io/react-mosaic/)
- [MosaicWindow API Documentation](https://github.com/nomcopter/react-mosaic/blob/master/src/MosaicWindow.tsx)

## Estimated Effort
- Medium: 1-2 days of development work
