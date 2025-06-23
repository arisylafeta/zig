When implementing changes in the app, whether big or small, conduct an investigation and ALWAYS create a ticket in the ticketing system.

The purpose of this is to have a record of the changes made and to be able to track the progress of the changes.

It serves as a communication tool between the team members and a record of the changes made, and helps captures important patterns, preferences, and project intelligence, living document that grows smarter as progress happens.

RULES:
1. Ticket should be timestamped with the format YYYYMMDDHHmmss
2. Ticket should be named descriptively and should be in the format <Ticket ID> <Ticket Title>
3. Ticket should be created in the ticketing system directory @context_docs/ticket
4. Tickets should include the following:
   - Ticket information
   - Objective
   - Background
   - Requirements
   - Investigation
   - Implementation Plan (with details)
   - Acceptance Criteria
   - Considerations (dependencies, constraints, etc.)
   - Notes, related files, references, resources, etc.
5. Ticket should ONLY be updated after the approval from the lead developer. DO NOT update the ticket without approval.
6. Sometimes the actual implementation of the ticket is different from the plan. In that case, update the ticket to reflect the actual implementation.


### EXAMPLE:

# Chat Panel Integration with CopilotKit

**Ticket ID:** 20250610103000
**Created:** June 10, 2025, 10:30 AM
**Status:** Draft
**Priority:** High
**Assignee:** Dev Team
**Tags:** #frontend #chat #copilotkit #integration

## Objective

Import and integrate the chat panel components from the ebisu-relationship-orchestrator project into the zig app, adapting them to work with CopilotKit's chat API and UI customization features.

## Background

The original ebisu-relationship-orchestrator project includes a robust chat interface with components like `ChatPanel`, `ChatThread`, `ChatBubble`, and `ChatInput`. These components need to be migrated to the zig app and integrated with CopilotKit's chat functionality, replacing the custom chat service with CopilotKit's hooks and ensuring UI consistency.

## Requirements

1. Import and adapt chat components from ebisu-relationship-orchestrator
2. Replace custom chat service with CopilotKit's chat hooks
3. Customize UI according to CopilotKit's guidelines
4. Ensure chat state and messages are compatible with CopilotKit
5. Maintain responsive design and accessibility features
6. Preserve existing UI features (avatars, timestamps, copy buttons)

## Implementation Plan

### 1. Component Import and Initial Setup

1. Create necessary directory structure in zig app:
   ```
   /components/chat/
     ChatPanel.tsx
     ChatThread.tsx
     ChatBubble.tsx
     ChatInput.tsx
     types.ts
     index.ts
   ```

2. Import and adapt component types from original project:
   ```typescript
   // types.ts
   export interface ChatMessage {
     id: string;
     content: string;
     role: 'user' | 'assistant';
     timestamp: string;
     // Add any CopilotKit-specific fields
   }

   export interface ChatSession {
     id: string;
     messages: ChatMessage[];
     // Add any CopilotKit-specific fields
   }
   ```

### 2. CopilotKit Integration

1. Replace custom `useChatService` hook with CopilotKit's `useCopilotChat`:
   ```typescript
   // In ChatPanel.tsx
   import { useCopilotChat } from '@copilotkit/react-core';
   
   // Replace:
   // const chatService = useChatService();
   // With:
   const { messages, sendMessage, isLoading } = useCopilotChat();
   ```

2. Adapt message handling to work with CopilotKit's message format:
   ```typescript
   // Convert between our ChatMessage format and CopilotKit's format as needed
   const handleSendMessage = (content: string) => {
     sendMessage(content);
   };
   ```

### 3. UI Customization with CopilotKit

1. Implement custom message components using CopilotKit's component override system:
   ```typescript
   // Custom assistant message component
   const CustomAssistantMessage = (props: AssistantMessageProps) => {
     const { message, isLoading, subComponent } = props;
     
     return (
       <div className="chat-message assistant">
         <div className="avatar">
           <AssistantAvatar />
         </div>
         <div className="message-content">
           <Markdown content={message || ""} />
           {isLoading && <LoadingIndicator />}
         </div>
         {subComponent && <div className="sub-component">{subComponent}</div>}
       </div>
     );
   };
   
   // Custom user message component
   const CustomUserMessage = (props: UserMessageProps) => {
     const { message } = props;
     
     return (
       <div className="chat-message user">
         <div className="avatar">
           <UserAvatar />
         </div>
         <div className="message-content">
           <Markdown content={message || ""} />
         </div>
       </div>
     );
   };
   ```

2. Configure CSS variables to match our design system:
   ```css
   :root {
     --copilot-kit-primary-color: #4f46e5; /* Indigo 600 */
     --copilot-kit-contrast-color: #ffffff;
     --copilot-kit-background-color: #f9fafb; /* Gray 50 */
     --copilot-kit-secondary-color: #ffffff;
     --copilot-kit-secondary-contrast-color: #111827; /* Gray 900 */
     --copilot-kit-separator-color: #e5e7eb; /* Gray 200 */
     --copilot-kit-muted-color: #9ca3af; /* Gray 400 */
   }
   ```

3. Apply custom components to CopilotKit:
   ```typescript
   <CopilotKit>
     <CopilotSidebar
       AssistantMessage={CustomAssistantMessage}
       UserMessage={CustomUserMessage}
     />
   </CopilotKit>
   ```

### 4. Panel Integration

1. Register the ChatPanel component with the PanelRegistry:
   ```typescript
   // In panel configuration
   import { ChatPanel } from '@/components/chat';
   
   panelRegistry.register('chat', {
     component: ChatPanel,
     defaultSize: 300,
     minSize: 200,
     maxSize: 500,
   });
   ```

2. Add chat panel to the default panel layout:
   ```typescript
   // In ModeConfigs
   const defaultMode = {
     id: 'default',
     panels: [
       { id: 'chat', type: 'chat', position: 'left' },
       { id: 'main', type: 'workspace', position: 'center' },
       { id: 'details', type: 'details', position: 'right' },
     ],
   };
   ```

### 5. Testing and Refinement

1. Test chat functionality with CopilotKit:
   - Message sending and receiving
   - UI rendering and responsiveness
   - Streaming message support
   - Error handling

2. Verify panel integration:
   - Panel resizing
   - Panel collapsing/expanding
   - Panel state persistence

## Acceptance Criteria

1. Chat panel renders correctly within the panel system
2. Messages can be sent and received using CopilotKit's chat API
3. UI matches design system and maintains all original features
4. Chat state is properly managed and persisted
5. Responsive design works on different screen sizes
6. All accessibility features are preserved

## Dependencies

1. CopilotKit React UI package (`@copilotkit/react-ui`)
2. CopilotKit React Core package (`@copilotkit/react-core`)
3. Panel system components from ebisu-relationship-orchestrator

## Notes

- Consider implementing a fallback mechanism if CopilotKit's API is unavailable
- Evaluate performance impact of real-time message streaming
- Document any CopilotKit-specific configuration for team reference

## References

1. [CopilotKit Custom UI Documentation](https://docs.copilotkit.ai/guides/custom-look-and-feel)
2. [Panel System Analysis](/Users/lobby/Desktop/apps/ebisu/zig/context_docs/lovable_components/panel_system.md)
3. [Chat Components Analysis](/Users/lobby/Desktop/apps/ebisu/zig/context_docs/lovable_components/chat_components.md)

   