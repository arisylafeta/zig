# React Mosaic Integration for Panel-Based UI

**Ticket ID:** 20250623095800
**Created:** June 23, 2025, 09:58 AM
**Status:** Draft
**Priority:** High
**Assignee:** Dev Team
**Tags:** #frontend #ui #panels #react-mosaic #copilotkit

## Objective

Integrate React Mosaic Components library to create a flexible, tiling window manager system for the application, with a focus on compatibility with CopilotKit for AI-driven panel management.

## Background

The current panel system implementation is complex and resource-intensive. React Mosaic provides a mature, well-tested solution for creating a tiling window manager in React applications. This integration aims to simplify our codebase while maintaining the functionality needed for AI-driven panel management through CopilotKit.

## Requirements

1. Replace the custom panel system with React Mosaic Components
2. Ensure compatibility with CopilotKit for AI-driven panel management
3. Implement a chat panel as the primary interface for user-AI interaction
4. Create at least one additional panel type to demonstrate AI-driven actions
5. Maintain responsive design and accessibility features
6. Reduce overall system complexity and resource usage

## Investigation

### React Mosaic Components Analysis

React Mosaic Components is a flexible windowing system that provides:
- Draggable and resizable panels
- Nested layout configurations
- Split views with adjustable dividers
- Window management with minimize/maximize functionality

The library is actively maintained (latest version 6.1.1 published 6 months ago) and has the following key dependencies:
- react-dnd (for drag and drop functionality)
- immutability-helper (for state management)
- classnames (for conditional CSS class application)

### CopilotKit Compatibility

CopilotKit can be integrated with React Mosaic through:
1. Custom actions that manipulate the Mosaic layout state
2. Event listeners that respond to user queries by modifying panel configurations
3. Direct manipulation of panel content based on AI responses

## Implementation Plan

### 1. Initial Setup and Dependencies

1. Install React Mosaic Components and its dependencies:
   ```bash
   npm install react-mosaic-component
   ```

2. Add required CSS imports:
   ```typescript
   // In _app.tsx or equivalent
   import 'react-mosaic-component/react-mosaic-component.css';
   ```

### 2. Create Basic Mosaic Layout Component

1. Create a MosaicLayout component:
   ```typescript
   // src/components/layout/MosaicLayout.tsx
   import React, { useState } from 'react';
   import { Mosaic, MosaicWindow } from 'react-mosaic-component';
   import { MosaicKey } from 'react-mosaic-component/lib/types';
   
   export interface PanelProps {
     id: string;
     title: string;
   }
   
   interface MosaicLayoutProps {
     initialLayout?: any;
     panels: Record<string, React.ComponentType<PanelProps>>;
   }
   
   export function MosaicLayout({ initialLayout, panels }: MosaicLayoutProps) {
     const [layout, setLayout] = useState(initialLayout || {
       direction: 'row',
       first: 'chat',
       second: 'workspace',
       splitPercentage: 30,
     });
     
     const renderTile = (id: MosaicKey, path: Array<MosaicKey>) => {
       const Panel = panels[id as string] || (() => <div>Panel not found</div>);
       
       return (
         <MosaicWindow<string>
           path={path}
           title={id as string}
           toolbarControls={[]}
         >
           <Panel id={id as string} title={id as string} />
         </MosaicWindow>
       );
     };
     
     return (
       <div className="mosaic-layout">
         <Mosaic<string>
           renderTile={renderTile}
           value={layout}
           onChange={setLayout}
           className="mosaic-blueprint-theme"
         />
       </div>
     );
   }
   ```

### 3. Create Basic Panel Components

1. Create a ChatPanel component:
   ```typescript
   // src/components/panels/ChatPanel.tsx
   import React, { useState } from 'react';
   import { useCopilotChat } from '@copilotkit/react-core';
   import { PanelProps } from '../layout/MosaicLayout';
   
   export function ChatPanel({ id, title }: PanelProps) {
     const [input, setInput] = useState('');
     const { messages, sendMessage, isLoading } = useCopilotChat();
     
     const handleSend = () => {
       if (input.trim()) {
         sendMessage(input);
         setInput('');
       }
     };
     
     return (
       <div className="chat-panel">
         <div className="messages">
           {messages.map((msg, i) => (
             <div key={i} className={`message ${msg.role}`}>
               {msg.content}
             </div>
           ))}
           {isLoading && <div className="loading">AI is thinking...</div>}
         </div>
         <div className="input-area">
           <input
             value={input}
             onChange={(e) => setInput(e.target.value)}
             onKeyDown={(e) => e.key === 'Enter' && handleSend()}
             placeholder="Ask the AI..."
           />
           <button onClick={handleSend} disabled={isLoading}>Send</button>
         </div>
       </div>
     );
   }
   ```

2. Create a WorkspacePanel component:
   ```typescript
   // src/components/panels/WorkspacePanel.tsx
   import React from 'react';
   import { PanelProps } from '../layout/MosaicLayout';
   
   export function WorkspacePanel({ id, title }: PanelProps) {
     return (
       <div className="workspace-panel">
         <h2>Workspace</h2>
         <p>This is a workspace panel that can be controlled by the AI.</p>
       </div>
     );
   }
   ```

### 4. CopilotKit Integration

1. Create custom actions for panel management:
   ```typescript
   // src/hooks/usePanelActions.ts
   import { useCopilotAction } from '@copilotkit/react-core';
   
   export function usePanelActions(setLayout: (layout: any) => void) {
     // Add panel action
     useCopilotAction({
       name: "addPanel",
       description: "Add a new panel to the layout",
       parameters: [
         { name: "panelId", type: "string", description: "ID of the panel to add" },
         { name: "position", type: "string", enum: ["left", "right", "top", "bottom"], description: "Position to add the panel" }
       ],
       handler: ({ panelId, position }) => {
         setLayout((currentLayout: any) => {
           // Logic to add panel at specified position
           // This is simplified; actual implementation would be more complex
           const newLayout = {
             direction: position === 'left' || position === 'right' ? 'row' : 'column',
             first: position === 'left' || position === 'top' ? panelId : currentLayout,
             second: position === 'right' || position === 'bottom' ? panelId : currentLayout,
             splitPercentage: 50
           };
           
           return newLayout;
         });
         
         return { success: true, message: `Added panel ${panelId} at ${position}` };
       }
     });
     
     // Remove panel action
     useCopilotAction({
       name: "removePanel",
       description: "Remove a panel from the layout",
       parameters: [
         { name: "panelId", type: "string", description: "ID of the panel to remove" }
       ],
       handler: ({ panelId }) => {
         setLayout((currentLayout: any) => {
           // Logic to remove panel
           // This is simplified; actual implementation would be more complex
           // Would need to traverse the layout tree to find and remove the panel
           
           return currentLayout; // Placeholder
         });
         
         return { success: true, message: `Removed panel ${panelId}` };
       }
     });
     
     // Resize panel action
     useCopilotAction({
       name: "resizePanel",
       description: "Resize a panel",
       parameters: [
         { name: "panelId", type: "string", description: "ID of the panel to resize" },
         { name: "percentage", type: "number", description: "New size as percentage (1-100)" }
       ],
       handler: ({ panelId, percentage }) => {
         setLayout((currentLayout: any) => {
           // Logic to resize panel
           // This is simplified; actual implementation would be more complex
           // Would need to traverse the layout tree to find and resize the panel
           
           return currentLayout; // Placeholder
         });
         
         return { success: true, message: `Resized panel ${panelId} to ${percentage}%` };
       }
     });
   }
   ```

### 5. Main Application Integration

1. Update the main application component:
   ```typescript
   // src/app/page.tsx
   import React, { useState } from 'react';
   import { CopilotKit } from '@copilotkit/react-core';
   import { MosaicLayout } from '@/components/layout/MosaicLayout';
   import { ChatPanel } from '@/components/panels/ChatPanel';
   import { WorkspacePanel } from '@/components/panels/WorkspacePanel';
   import { usePanelActions } from '@/hooks/usePanelActions';
   
   export default function Home() {
     const [layout, setLayout] = useState({
       direction: 'row',
       first: 'chat',
       second: 'workspace',
       splitPercentage: 30,
     });
     
     // Register panel actions with CopilotKit
     usePanelActions(setLayout);
     
     const panels = {
       'chat': ChatPanel,
       'workspace': WorkspacePanel,
     };
     
     return (
       <CopilotKit>
         <div className="app-container">
           <MosaicLayout
             layout={layout}
             panels={panels}
           />
         </div>
       </CopilotKit>
     );
   }
   ```

### 6. Styling and Responsiveness

1. Add responsive styles:
   ```css
   /* src/styles/mosaic.css */
   .mosaic-layout {
     height: 100vh;
     width: 100%;
   }
   
   .mosaic {
     height: 100%;
   }
   
   /* Mobile responsiveness */
   @media (max-width: 768px) {
     .mosaic-layout {
       height: calc(100vh - 60px); /* Adjust for mobile header */
     }
     
     /* Additional mobile-specific styles */
   }
   ```

## Acceptance Criteria

1. React Mosaic Components successfully integrated into the application
2. Chat panel renders and functions correctly with CopilotKit
3. At least one additional panel type is implemented and can be controlled by the AI
4. Panel actions (add, remove, resize) work correctly through CopilotKit
5. Layout is responsive and works on different screen sizes
6. System resource usage is reduced compared to the previous implementation

## Dependencies

1. React Mosaic Components (`react-mosaic-component`)
2. CopilotKit React Core (`@copilotkit/react-core`)
3. CopilotKit React UI (`@copilotkit/react-ui`)

## Notes

- React Mosaic requires React DnD for drag and drop functionality, which may add some complexity
- Consider implementing a state persistence mechanism to save user's panel configurations
- Document the panel action API for future reference

## References

1. [React Mosaic GitHub Repository](https://github.com/nomcopter/react-mosaic)
2. [React Mosaic Documentation](https://github.com/nomcopter/react-mosaic#readme)
3. [CopilotKit Documentation](https://docs.copilotkit.ai)
