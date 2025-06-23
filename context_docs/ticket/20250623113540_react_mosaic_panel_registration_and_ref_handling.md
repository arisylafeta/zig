# React Mosaic Panel Registration and Ref Handling

## Overview
This ticket documents the implementation of the panel registration system in our React Mosaic window management and addresses the React 19 ref warning that appears in the console.

## Panel Registration System

### How Panel Registration Works
1. **Panel Configuration**: Each panel has a unique configuration defined by the `PanelConfig` interface:
   ```typescript
   export interface PanelConfig {
     id: PanelId;
     title: string;
     component: React.ComponentType<PanelProps>;
     closable?: boolean;
     draggable?: boolean;
   }
   ```

2. **Panel Registry**: Panels are registered using the `usePanelRegistry` hook in `MosaicApp.tsx`. This creates a mapping from panel IDs to their configurations:
   ```typescript
   const { registerPanels } = usePanelRegistry();
   
   useEffect(() => {
     const availablePanels: PanelConfig[] = [
       {
         id: 'peopleSearch',
         title: 'People Search',
         component: PeopleSearchPanel,
         defaultSize: 30,
         closable: true,
         draggable: true,
       },
       // Other panel configurations...
     ];
     
     registerPanels(availablePanels);
   }, [registerPanels]);
   ```

3. **Panel Rendering**: In `MosaicLayout.tsx`, panels are rendered based on their ID using the `renderTile` function:
   ```typescript
   const renderTile = (id: string, path: MosaicBranch[]) => {
     // Get panel config from registry
     const panelConfig = panelRegistry[id];
     
     // Render the panel component with its configuration
     return (
       <MosaicWindow
         key={id}
         path={path}
         title={title}
         draggable={draggable}
         createNode={createNode}
         toolbarControls={[]}
         renderToolbar={(props, draggable) => renderToolbar(props, draggable, panelConfig)}
       >
         <Panel id={id} path={path} />
       </MosaicWindow>
     );
   };
   ```

### Issues Addressed

#### 1. Missing Key Props Error
- **Issue**: React was warning about missing unique "key" props for children in lists.
- **Solution**: Added `key={id}` to each `MosaicWindow` component to ensure each panel has a unique key.
- **Importance**: This prevents React from unnecessarily re-rendering components and improves performance.

#### 2. React 19 Element.ref Warning
- **Issue**: Console warning: "Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release."
- **Cause**: The `react-mosaic-component` library (v6.1.1) is using the legacy string ref API which has been removed in React 19.
- **Temporary Solution**: Added `toolbarControls={[]}` prop to `MosaicWindow` components to avoid reliance on string refs.
- **Long-term Solution**: Consider upgrading to a newer version of `react-mosaic-component` that supports React 19's ref API, or fork and maintain our own version.

## React 19 Ref Changes Explained

### What Changed in React 19
In React 19, the legacy string ref API (`<div ref="myRef" />`) was completely removed. This API had been deprecated for several versions already. React now only supports:

1. **Callback Refs**: `<div ref={(node) => this.myRef = node} />`
2. **createRef**: `this.myRef = React.createRef(); <div ref={this.myRef} />`
3. **useRef Hook**: `const myRef = useRef(null); <div ref={myRef} />`

### Impact on Our Application
The `react-mosaic-component` library internally uses string refs in some components. When these components render in React 19, they trigger warnings but still function. This is because React 19 maintains some backward compatibility while warning about deprecated patterns.

### Technical Details
- The warning appears because `MosaicWindow` component is trying to access `element.ref` which no longer exists in React 19.
- Our workaround uses the `toolbarControls` prop to provide an alternative way to customize the toolbar without relying on refs.
- This is a temporary solution until the `react-mosaic-component` library is updated or we fork it.

## Next Steps
1. Monitor the `react-mosaic-component` repository for updates that address React 19 compatibility.
2. Consider creating a fork of the library to fix the ref issues if no updates are forthcoming.
3. Evaluate alternative window management libraries if necessary.

## References
- [React Docs: Refs and the DOM](https://reactjs.org/docs/refs-and-the-dom.html)
- [React Mosaic Documentation](https://github.com/nomcopter/react-mosaic)
- [React 19 Release Notes](https://react.dev/blog/2024/04/25/react-19)
