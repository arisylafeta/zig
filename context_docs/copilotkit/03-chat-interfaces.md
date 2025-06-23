# CopilotKit Chat Interfaces

CopilotKit provides several pre-built chat interface components that can be easily integrated into your application. These components offer different user experiences for interacting with the AI copilot.

## CopilotSidebar

The `CopilotSidebar` component provides a sidebar chat interface that can be toggled on and off. This is ideal for applications where the chat functionality should be accessible but not always visible.

```jsx
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function MyApp() {
  return (
    <div className="app-container">
      <CopilotSidebar />
      <main>
        {/* Your application content */}
      </main>
    </div>
  );
}
```

### Key Props

- `defaultOpen`: Boolean to control if the sidebar is open by default
- `buttonPosition`: Position of the toggle button ("top-left", "top-right", "bottom-left", "bottom-right")
- `buttonClassName`: CSS class for the toggle button
- `sidebarClassName`: CSS class for the sidebar container
- `systemPrompt`: System prompt for the AI

## CopilotPopup

The `CopilotPopup` component provides a popup chat interface that can be toggled on and off. This is useful for applications where the chat functionality should be minimally intrusive.

```jsx
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function MyApp() {
  return (
    <div className="app-container">
      <CopilotPopup />
      <main>
        {/* Your application content */}
      </main>
    </div>
  );
}
```

### Key Props

- `defaultOpen`: Boolean to control if the popup is open by default
- `buttonPosition`: Position of the toggle button ("top-left", "top-right", "bottom-left", "bottom-right")
- `buttonClassName`: CSS class for the toggle button
- `popupClassName`: CSS class for the popup container
- `systemPrompt`: System prompt for the AI

## CopilotChat

The `CopilotChat` component provides a full-page chat interface. This is suitable for applications where the chat functionality is the primary feature.

```jsx
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function ChatPage() {
  return (
    <div className="chat-page">
      <CopilotChat />
    </div>
  );
}
```

### Key Props

- `className`: CSS class for the chat container
- `systemPrompt`: System prompt for the AI
- `placeholder`: Placeholder text for the input field

## CopilotChatbox

The `CopilotChatbox` is a lower-level component that can be used within the `CopilotSidebar` or directly in your application. It provides the chat interface without the container.

```jsx
import { CopilotSidebar, CopilotChatbox } from "@copilotkit/react-ui";

function CustomSidebar() {
  return (
    <CopilotSidebar>
      <div className="custom-header">My Copilot</div>
      <CopilotChatbox
        placeholder="Ask me anything about your data..."
        defaultSystemPrompt="You are a helpful assistant focused on data analysis."
      />
    </CopilotSidebar>
  );
}
```

### Key Props

- `placeholder`: Placeholder text for the input field
- `defaultSystemPrompt`: System prompt for the AI
- `className`: CSS class for the chatbox container

## Custom Chat Interface

For complete control over the chat interface, you can use the `useCopilotChat` hook to build your own custom chat component.

```jsx
import { useCopilotChat } from "@copilotkit/react-core";
import { useState } from "react";

function CustomChatInterface() {
  const [inputValue, setInputValue] = useState("");
  const {
    visibleMessages,
    appendMessage,
    isLoading,
    stopGeneration
  } = useCopilotChat();

  const handleSend = () => {
    if (inputValue.trim()) {
      appendMessage({
        content: inputValue,
        role: "user"
      });
      setInputValue("");
    }
  };

  return (
    <div className="custom-chat">
      <div className="message-container">
        {visibleMessages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">{message.content}</div>
          </div>
        ))}
        {isLoading && <div className="loading-indicator">AI is typing...</div>}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSend();
          }}
          placeholder="Type your message..."
        />
        <button onClick={handleSend} disabled={isLoading}>
          Send
        </button>
        {isLoading && (
          <button onClick={stopGeneration}>Stop</button>
        )}
      </div>
    </div>
  );
}
```

## Styling Chat Interfaces

CopilotKit chat components can be styled using CSS classes or by overriding the default styles.

### Using CSS Classes

```jsx
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import "./custom-chat-styles.css";

function MyApp() {
  return (
    <div className="app-container">
      <CopilotSidebar 
        buttonClassName="custom-toggle-button"
        sidebarClassName="custom-sidebar"
      />
      <main>
        {/* Your application content */}
      </main>
    </div>
  );
}
```

### CSS Variables

CopilotKit components use CSS variables for theming. You can override these variables in your CSS:

```css
:root {
  --copilot-chat-bg: #1e1e1e;
  --copilot-chat-text: #ffffff;
  --copilot-chat-border: #333333;
  --copilot-chat-user-message-bg: #2b2b2b;
  --copilot-chat-assistant-message-bg: #383838;
  --copilot-chat-input-bg: #2b2b2b;
  --copilot-chat-input-text: #ffffff;
  --copilot-chat-input-border: #444444;
  --copilot-chat-button-bg: #0078d4;
  --copilot-chat-button-text: #ffffff;
  --copilot-chat-button-hover-bg: #106ebe;
}
```

## Best Practices

1. **Choose the Right Interface**: Select the chat interface that best fits your application's UX requirements.
2. **Provide Clear Context**: Use system prompts to guide the AI's behavior.
3. **Handle Loading States**: Always indicate when the AI is generating a response.
4. **Error Handling**: Implement error handling for failed requests.
5. **Responsive Design**: Ensure your chat interface works well on different screen sizes.
6. **Accessibility**: Make sure your chat interface is accessible to all users.
