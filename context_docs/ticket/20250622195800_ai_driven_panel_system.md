# AI-Driven Panel System with CopilotKit Integration

**Ticket ID:** 20250622195800
**Created:** June 22, 2025, 19:58:00
**Status:** Draft
**Priority:** High
**Assignee:** Dev Team
**Tags:** #frontend #architecture #copilotkit #panels

## Objective

Design and implement an AI-driven panel system for the zig app that leverages CopilotKit's capabilities for dynamic content generation and panel management, allowing the AI to respond to user queries by spawning and manipulating appropriate panels.

## Background

The original ebisu-relationship-orchestrator project uses a sophisticated panel system that allows for flexible layouts and panel arrangements. We want to migrate this functionality to the zig app while enhancing it with CopilotKit's AI capabilities to create a more dynamic, responsive interface that adapts to user needs.

## Requirements

1. Create a main app shell with a flexible panel system
2. Implement AI-driven panel management through CopilotKit actions
3. Make the chat panel always accessible as a constant element
4. Support dynamic content generation in panels using CopilotKit's generative UI
5. Implement state management for panel visibility, size, and content
6. Ensure responsive design across different screen sizes
7. Support both horizontal and vertical panel layouts

## Implementation Plan

### 1. App Shell and Panel System Architecture

1. Create a main layout component that serves as the app shell:
   ```typescript
   // src/app/layout.tsx
   import { CopilotKit } from "@copilotkit/react-core";
   import { PanelProvider } from "@/components/panels/PanelProvider";
   
   export default function RootLayout({ children }) {
     return (
       <CopilotKit>
         <PanelProvider>
           {children}
         </PanelProvider>
       </CopilotKit>
     );
   }
   ```

2. Implement the core panel system components:
   - `PanelManager.tsx`: Main orchestrator for panel layout and rendering
   - `PanelProvider.tsx`: Context provider for panel state management
   - `PanelRegistry.ts`: Registry of all available panels and their configurations
   - `ModeConfigs.ts`: Defines different application modes and their associated panels

3. Define the panel state interface:
   ```typescript
   // src/components/panels/types.ts
   export interface PanelState {
     activeMode: string;           // Current application mode
     visiblePanels: string[];      // Currently visible panel IDs
     panelSizes: Record<string, number>; // Panel sizes as percentages
     viewMode: 'horizontal-split' | 'vertical-split';
     isChatVisible: boolean;       // Chat panel visibility
   }
   ```

### 2. AI-Driven Panel Management

1. Create CopilotKit actions for panel management:
   ```typescript
   // src/components/panels/usePanelActions.ts
   import { useCopilotAction } from "@copilotkit/react-core";
   import { usePanelContext } from "./PanelProvider";
   
   export function usePanelActions() {
     const { state, setState } = usePanelContext();
     
     // Show/hide panel action
     useCopilotAction({
       name: "togglePanel",
       description: "Show or hide a specific panel",
       parameters: [
         { name: "panelId", type: "string", description: "ID of the panel to toggle" },
         { name: "visible", type: "boolean", description: "Whether the panel should be visible" }
       ],
       handler: ({ panelId, visible }) => {
         const visiblePanels = visible 
           ? [...state.visiblePanels, panelId]
           : state.visiblePanels.filter(id => id !== panelId);
         
         setState({
           ...state,
           visiblePanels
         });
       }
     });
     
     // Change panel layout action
     useCopilotAction({
       name: "changeViewMode",
       description: "Change the panel layout between horizontal and vertical split",
       parameters: [
         { name: "mode", type: "string", enum: ["horizontal-split", "vertical-split"] }
       ],
       handler: ({ mode }) => {
         setState({
           ...state,
           viewMode: mode
         });
       }
     });
     
     // Change active mode action
     useCopilotAction({
       name: "changeMode",
       description: "Change the active application mode",
       parameters: [
         { name: "mode", type: "string", description: "The mode to activate" }
       ],
       handler: ({ mode }) => {
         const modeConfig = getModeConfig(mode);
         setState({
           ...state,
           activeMode: mode,
           visiblePanels: modeConfig.panels
         });
       }
     });
   }
   ```

### 3. Chat Panel as a Constant Element

1. Implement a persistent chat panel using CopilotKit's chat hooks:
   ```typescript
   // src/components/chat/ChatPanel.tsx
   import { useCopilotChat } from "@copilotkit/react-core";
   import { ChatThread } from "./ChatThread";
   import { ChatInput } from "./ChatInput";
   
   export function ChatPanel() {
     const { messages, sendMessage, isLoading } = useCopilotChat();
     
     const handleSendMessage = (content: string) => {
       sendMessage(content);
     };
     
     return (
       <div className="chat-panel">
         <div className="chat-header">
           <h2>Ebisu AI</h2>
         </div>
         <ChatThread messages={messages} isLoading={isLoading} />
         <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
       </div>
     );
   }
   ```

2. Register the chat panel with the panel system:
   ```typescript
   // src/components/panels/PanelRegistry.ts
   import { ChatPanel } from "@/components/chat/ChatPanel";
   
   export const panelRegistry = {
     panels: {
       chat: {
         id: 'chat',
         component: ChatPanel,
         defaultSize: 25,
         minSize: 15,
         maxSize: 100,
         position: 'left'
       },
       // Other panels...
     },
     
     register(id, config) {
       this.panels[id] = config;
     },
     
     getPanel(id) {
       return this.panels[id];
     }
   };
   ```

### 4. Generative UI for Dynamic Content

1. Create a dynamic content panel that can be populated by AI:
   ```typescript
   // src/components/panels/DynamicContentPanel.tsx
   import { useEffect, useState } from "react";
   import { useCopilotAction } from "@copilotkit/react-core";
   
   export function DynamicContentPanel({ panelId }) {
     const [content, setContent] = useState(null);
     
     useCopilotAction({
       name: "updatePanelContent",
       description: `Update the content of panel ${panelId}`,
       parameters: [
         { name: "panelId", type: "string" },
         { name: "contentType", type: "string", enum: ["company", "chart", "table", "form"] },
         { name: "data", type: "object" }
       ],
       handler: ({ panelId: targetPanelId, contentType, data }) => {
         if (targetPanelId === panelId) {
           setContent({
             type: contentType,
             data
           });
         }
       }
     });
     
     return (
       <div className="dynamic-panel">
         {content ? (
           renderContent(content)
         ) : (
           <div className="empty-state">
             <p>Ask the AI to display information here</p>
           </div>
         )}
       </div>
     );
   }
   
   function renderContent({ type, data }) {
     switch (type) {
       case "company":
         return <CompanyCard company={data} />;
       case "chart":
         return <Chart data={data} />;
       case "table":
         return <DataTable data={data} />;
       case "form":
         return <DynamicForm schema={data} />;
       default:
         return <div>Unknown content type</div>;
     }
   }
   ```

2. Implement generative UI components for specific use cases:
   ```typescript
   // src/components/generative/CompanyVisualization.tsx
   import { useCopilotAction } from "@copilotkit/react-core";
   
   export function useCompanyVisualization() {
     useCopilotAction({
       name: "visualizeCompanyData",
       description: "Visualize company data in the appropriate panel",
       parameters: [
         { name: "companyId", type: "string" },
         { name: "visualizationType", type: "string", enum: ["overview", "financials", "competitors"] }
       ],
       render: ({ status, args }) => {
         if (status === "inProgress") {
           return <LoadingVisualization type={args.visualizationType} />;
         }
         
         return (
           <CompanyVisualization 
             companyId={args.companyId}
             type={args.visualizationType} 
           />
         );
       },
       handler: ({ companyId, visualizationType }) => {
         // Fetch data and return it
         return fetchCompanyData(companyId, visualizationType);
       }
     });
   }
   ```

### 5. State Management

1. Implement the panel context provider:
   ```typescript
   // src/components/panels/PanelProvider.tsx
   import { createContext, useContext, useState } from "react";
   import { PanelState } from "./types";
   import { defaultModeConfig } from "./ModeConfigs";
   
   const PanelContext = createContext(null);
   
   export function PanelProvider({ children }) {
     const [state, setState] = useState<PanelState>({
       activeMode: 'default',
       visiblePanels: defaultModeConfig.panels.map(p => p.id),
       panelSizes: defaultModeConfig.panels.reduce((acc, p) => {
         acc[p.id] = p.defaultSize;
         return acc;
       }, {}),
       viewMode: 'horizontal-split',
       isChatVisible: true
     });
     
     // Make panel state accessible to CopilotKit
     useCopilotReadable({
       description: "Current panel system state",
       value: state
     });
     
     return (
       <PanelContext.Provider value={{ state, setState }}>
         {children}
       </PanelContext.Provider>
     );
   }
   
   export function usePanelContext() {
     const context = useContext(PanelContext);
     if (!context) {
       throw new Error("usePanelContext must be used within a PanelProvider");
     }
     return context;
   }
   ```

2. Implement panel resize handling:
   ```typescript
   // src/components/panels/PanelManager.tsx
   import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
   import { usePanelContext } from "./PanelProvider";
   import { panelRegistry } from "./PanelRegistry";
   
   export function PanelManager() {
     const { state, setState } = usePanelContext();
     
     const handleResize = (panelId, size) => {
       setState({
         ...state,
         panelSizes: {
           ...state.panelSizes,
           [panelId]: size
         }
       });
     };
     
     return (
       <PanelGroup direction={state.viewMode === 'horizontal-split' ? "horizontal" : "vertical"}>
         {state.visiblePanels.map((panelId, index) => (
           <>
             <Panel 
               key={panelId}
               defaultSize={state.panelSizes[panelId]}
               minSize={panelRegistry.getPanel(panelId).minSize}
               onResize={(size) => handleResize(panelId, size)}
             >
               {renderPanel(panelId)}
             </Panel>
             {index < state.visiblePanels.length - 1 && (
               <PanelResizeHandle />
             )}
           </>
         ))}
       </PanelGroup>
     );
   }
   
   function renderPanel(panelId) {
     const panelConfig = panelRegistry.getPanel(panelId);
     const Component = panelConfig.component;
     return <Component panelId={panelId} />;
   }
   ```

### 6. Main App Page

1. Implement the main app page that brings everything together:
   ```typescript
   // src/app/page.tsx
   "use client";
   
   import { PanelManager } from "@/components/panels/PanelManager";
   import { usePanelActions } from "@/components/panels/usePanelActions";
   import { useCompanyVisualization } from "@/components/generative/CompanyVisualization";
   
   export default function Home() {
     // Initialize panel actions
     usePanelActions();
     
     // Initialize generative UI components
     useCompanyVisualization();
     
     return (
       <main className="h-screen w-screen overflow-hidden">
         <PanelManager />
       </main>
     );
   }
   ```

## Testing Plan

1. **Panel System Tests**:
   - Verify panels render correctly in both horizontal and vertical split modes
   - Test panel resizing, ensuring minimum and maximum constraints are respected
   - Verify panel visibility toggling works correctly

2. **CopilotKit Integration Tests**:
   - Test chat functionality with message sending and receiving
   - Verify AI can control panels through actions
   - Test generative UI rendering in panels

3. **Responsive Design Tests**:
   - Test on different screen sizes to ensure panels adapt correctly
   - Verify mobile experience with appropriate panel stacking

4. **State Management Tests**:
   - Verify panel state is properly maintained across interactions
   - Test mode switching and its effect on panel configuration

## Acceptance Criteria

1. Users can interact with the AI through the chat panel
2. AI can dynamically show/hide panels based on user queries
3. AI can populate panels with relevant content using generative UI
4. Panel layouts can switch between horizontal and vertical splits
5. Panel state persists during the session
6. System is responsive across different screen sizes
7. All panel interactions (resize, collapse, expand) work smoothly

## Dependencies

1. CopilotKit React Core (`@copilotkit/react-core`)
2. CopilotKit React UI (`@copilotkit/react-ui`)
3. React Resizable Panels (`react-resizable-panels`)

## References

1. [CopilotKit Documentation](https://docs.copilotkit.ai)
2. [Panel System Analysis](/Users/lobby/Desktop/apps/ebisu/zig/context_docs/lovable_components/panel_system.md)
3. [Chat Components Analysis](/Users/lobby/Desktop/apps/ebisu/zig/context_docs/lovable_components/chat_components.md)
4. [PANEL_README.md](/Users/lobby/Desktop/apps/ebisu/ebisu-relationship-orchestrator/PANEL_README.md)
