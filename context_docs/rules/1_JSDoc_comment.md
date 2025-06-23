When creating new files, add a JSDoc comment at the top of the file to describe the file's purpose and contents.

When updating existing files, update the JSDoc comment at the top of the file to describe the file's purpose and contents.

Example:

/**
 * @file ChatPanel.tsx
 * @description AI-driven chat panel component that integrates with CopilotKit.
 * This component provides a user interface for interacting with the AI assistant,
 * displaying messages, and sending user queries. It leverages CopilotKit's
 * headless UI approach for full control over the chat interface while using
 * CopilotKit's state management and message handling capabilities.
 * 
 * @component ChatPanel - Main component that renders the chat interface
 *   Uses CopilotKit's useCopilotChat hook to access message state and actions
 * 
 * @function scrollToBottom - Automatically scrolls the chat to the latest message
 *   Triggered when new messages are added or loading state changes
 * 
 * @function handleSendMessage - Processes user input and sends messages to the AI
 *   Creates a new TextMessage and appends it to the chat using appendMessage
 * 
 * @function handleKeyDown - Handles keyboard events for the input field
 *   Allows sending messages with Enter key (without Shift for new lines)
 * 
 * @function handleModelChange - Updates the selected AI model
 *   Changes the model selection state for potential API configuration
 */