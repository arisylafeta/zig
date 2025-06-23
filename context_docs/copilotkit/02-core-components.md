# CopilotKit Core Components

## CopilotKit Provider

The `CopilotKit` provider is the foundation of any CopilotKit application. It initializes the CopilotKit context and connects to the backend runtime.

```jsx
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

function App() {
  return (
    <CopilotKit 
      runtimeUrl="/api/copilotkit"
      agentName="your-agent-name"
    >
      {/* Your application */}
    </CopilotKit>
  );
}
```

### Key Props

- `runtimeUrl`: URL of the CopilotKit backend runtime
- `agentName`: Name of the agent to use
- `apiKey`: API key for authentication (if required)

## useCopilotReadable

The `useCopilotReadable` hook allows you to provide context to the AI about your application state. This context is "readable" by the AI but not modifiable.

```jsx
import { useCopilotReadable } from "@copilotkit/react-core";

function UserProfile({ user }) {
  // Make user data available to the AI
  useCopilotReadable({
    description: "Current user information",
    value: user
  }, [user]);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### Parameters

- `context`: Object containing a description and value
- `dependencies`: Array of dependencies (similar to useEffect)

## useCopilotAction

The `useCopilotAction` hook defines actions that the AI can take in your application. These actions are exposed to the AI as tools that it can call.

```jsx
import { useCopilotAction } from "@copilotkit/react-core";

function TaskList({ tasks, addTask, deleteTask }) {
  // Define an action to add a task
  useCopilotAction({
    name: "addTask",
    description: "Adds a new task to the list",
    parameters: [
      {
        name: "title",
        type: "string",
        description: "The title of the task",
        required: true
      }
    ],
    handler: ({ title }) => {
      addTask(title);
      return `Added task: ${title}`;
    }
  });

  // Define an action to delete a task
  useCopilotAction({
    name: "deleteTask",
    description: "Deletes a task from the list",
    parameters: [
      {
        name: "id",
        type: "number",
        description: "The ID of the task to delete",
        required: true
      }
    ],
    handler: ({ id }) => {
      deleteTask(id);
      return `Deleted task with ID: ${id}`;
    }
  });

  return (
    <ul>
      {tasks.map(task => (
        <li key={task.id}>{task.title}</li>
      ))}
    </ul>
  );
}
```

### Action Definition

- `name`: Unique name for the action
- `description`: Description of what the action does
- `parameters`: Array of parameter definitions (name, type, description, required)
- `handler`: Function that executes when the action is called

## useCopilotChat

The `useCopilotChat` hook provides access to the chat functionality for building custom chat interfaces.

```jsx
import { useCopilotChat } from "@copilotkit/react-core";

function CustomChatInterface() {
  const {
    visibleMessages,
    appendMessage,
    setMessages,
    deleteMessage,
    reloadMessages,
    stopGeneration,
    isLoading
  } = useCopilotChat();

  const sendMessage = (content) => {
    appendMessage({
      content,
      role: "user"
    });
  };

  return (
    <div>
      <div className="messages">
        {visibleMessages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            {message.content}
          </div>
        ))}
      </div>
      <input 
        type="text" 
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            sendMessage(e.target.value);
            e.target.value = "";
          }
        }} 
      />
    </div>
  );
}
```

### Available Methods

- `visibleMessages`: Array of messages to display
- `appendMessage`: Add a new message
- `setMessages`: Replace all messages
- `deleteMessage`: Remove a specific message
- `reloadMessages`: Reload the message history
- `stopGeneration`: Stop the AI from generating a response
- `isLoading`: Boolean indicating if the AI is generating a response

## CopilotTextarea

The `CopilotTextarea` component provides an AI-powered text editing experience.

```jsx
import { CopilotTextarea } from "@copilotkit/react-textarea";

function EmailComposer() {
  return (
    <div>
      <h2>Compose Email</h2>
      <CopilotTextarea
        placeholder="Start typing or ask AI to help compose an email..."
        defaultSystemPrompt="You are an email assistant helping to draft professional emails."
      />
    </div>
  );
}
```

### Key Props

- `placeholder`: Placeholder text for the textarea
- `defaultSystemPrompt`: System prompt for the AI
- `contextCategories`: Categories of context to include
- `className`: CSS class for styling

## CopilotSidebarUIProvider

The `CopilotSidebarUIProvider` component provides the UI context for the sidebar and other UI components.

```jsx
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebarUIProvider } from "@copilotkit/react-ui";

function App() {
  return (
    <CopilotKit>
      <CopilotSidebarUIProvider>
        {/* Your application */}
      </CopilotSidebarUIProvider>
    </CopilotKit>
  );
}
```

This provider is required when using UI components like `CopilotSidebar`, `CopilotPopup`, or `CopilotChat`.
