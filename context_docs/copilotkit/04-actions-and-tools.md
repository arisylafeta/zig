# CopilotKit Actions and Tools

Actions and tools are a core feature of CopilotKit that allow the AI to interact with your application. They enable the AI to trigger functions in your frontend or backend code, creating a truly interactive experience.

## Frontend Actions with useCopilotAction

The `useCopilotAction` hook allows you to define actions that the AI can trigger in your frontend application.

```jsx
import { useCopilotAction } from "@copilotkit/react-core";

function TaskManager({ tasks, addTask, deleteTask, updateTask }) {
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
      },
      {
        name: "priority",
        type: "string",
        description: "The priority of the task (low, medium, high)",
        enum: ["low", "medium", "high"],
        required: false
      }
    ],
    handler: ({ title, priority = "medium" }) => {
      const newTask = { title, priority, id: Date.now() };
      addTask(newTask);
      return `Added task: ${title} with ${priority} priority`;
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
      const task = tasks.find(t => t.id === id);
      if (!task) {
        return `Task with ID ${id} not found`;
      }
      deleteTask(id);
      return `Deleted task: ${task.title}`;
    }
  });

  // Define an action to update a task
  useCopilotAction({
    name: "updateTask",
    description: "Updates a task in the list",
    parameters: [
      {
        name: "id",
        type: "number",
        description: "The ID of the task to update",
        required: true
      },
      {
        name: "title",
        type: "string",
        description: "The new title of the task",
        required: false
      },
      {
        name: "priority",
        type: "string",
        description: "The new priority of the task (low, medium, high)",
        enum: ["low", "medium", "high"],
        required: false
      },
      {
        name: "completed",
        type: "boolean",
        description: "Whether the task is completed",
        required: false
      }
    ],
    handler: ({ id, title, priority, completed }) => {
      const task = tasks.find(t => t.id === id);
      if (!task) {
        return `Task with ID ${id} not found`;
      }
      
      const updates = {};
      if (title !== undefined) updates.title = title;
      if (priority !== undefined) updates.priority = priority;
      if (completed !== undefined) updates.completed = completed;
      
      updateTask(id, updates);
      return `Updated task: ${task.title}`;
    }
  });

  return (
    <div>
      {/* Task list UI */}
    </div>
  );
}
```

### Action Definition Properties

- `name`: Unique name for the action (required)
- `description`: Description of what the action does (required)
- `parameters`: Array of parameter definitions (optional)
  - `name`: Name of the parameter
  - `type`: Type of the parameter (string, number, boolean, object, array)
  - `description`: Description of the parameter
  - `required`: Whether the parameter is required
  - `enum`: Array of allowed values (for string parameters)
- `handler`: Function that executes when the action is called (required)

## Backend Actions

Backend actions are defined in the CopilotKit runtime and allow the AI to interact with your backend services.

```typescript
// pages/api/copilotkit.ts
import { CopilotRuntime } from "@copilotkit/runtime";

const runtime = new CopilotRuntime({
  actions: ({ properties, url }) => {
    return [
      {
        name: "fetchUserData",
        description: "Fetches user data from the database",
        parameters: [
          {
            name: "userId",
            type: "string",
            description: "The ID of the user",
            required: true
          }
        ],
        handler: async ({ userId }) => {
          // Fetch user data from database
          const userData = await db.users.findById(userId);
          return userData;
        }
      },
      {
        name: "createOrder",
        description: "Creates a new order in the system",
        parameters: [
          {
            name: "userId",
            type: "string",
            description: "The ID of the user placing the order",
            required: true
          },
          {
            name: "products",
            type: "array",
            description: "Array of product IDs and quantities",
            required: true
          },
          {
            name: "shippingAddress",
            type: "object",
            description: "The shipping address for the order",
            required: true
          }
        ],
        handler: async ({ userId, products, shippingAddress }) => {
          // Create order in database
          const order = await db.orders.create({
            userId,
            products,
            shippingAddress,
            status: "pending"
          });
          return order;
        }
      }
    ];
  }
});

export default runtime.createHandler();
```

## Accessing Actions in Agents

In LangGraph agents, you can access the frontend actions from the `copilotkit` property within your agent's state.

```python
# Python agent
async def agent_node(state: YourAgentState, config: RunnableConfig):
    # Access the actions from the copilotkit property
    actions = state.get("copilotkit", {}).get("actions", [])
    model = ChatOpenAI(model="gpt-4o").bind_tools(actions)
    
    # Use the model with the actions
    response = await model.invoke([
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Can you help me manage my tasks?")
    ])
    
    return {
        "messages": [*state.get("messages", []), response]
    }
```

```typescript
// TypeScript agent
async function agentNode(state: YourAgentState, config: RunnableConfig): Promise<YourAgentState> {
    // Access the actions from the copilotkit property
    const actions = state.copilotkit?.actions;
    const model = ChatOpenAI({ model: 'gpt-4o' }).bindTools(actions);
    
    // Use the model with the actions
    const response = await model.invoke([
        new SystemMessage("You are a helpful assistant."),
        new HumanMessage("Can you help me manage my tasks?")
    ]);
    
    return {
        messages: [...state.messages, response]
    };
}
```

## Human-in-the-Loop with Interrupts

CopilotKit provides a way for agents to interrupt their processing to ask for user input using the `copilotkit_interrupt` function.

```python
# Python agent
from copilotkit.langgraph import copilotkit_interrupt

async def agent_node(state: YourAgentState, config: RunnableConfig):
    # Check if we need user input
    if not state.get("user_name"):
        # Interrupt the agent to ask for the user's name
        answer, messages = await copilotkit_interrupt(
            action='AskName',
            args={"message": "Before we start, what would you like to call me?"}
        )
        
        # Update the state with the user's answer
        return {
            "user_name": answer,
            "messages": [*state.get("messages", []), *messages]
        }
    
    # Continue with normal processing
    # ...
```

```typescript
// TypeScript agent
import { copilotKitInterrupt } from "@copilotkit/sdk-js/langgraph";

async function agentNode(state: YourAgentState, config: RunnableConfig): Promise<YourAgentState> {
    // Check if we need user input
    if (!state.userName) {
        // Interrupt the agent to ask for the user's name
        const { answer, messages } = await copilotKitInterrupt({
            action: 'AskName',
            args: { message: 'Before we start, what would you like to call me?' }
        });
        
        // Update the state with the user's answer
        return {
            userName: answer,
            messages: [...state.messages, ...messages]
        };
    }
    
    // Continue with normal processing
    // ...
}
```

## Exiting Agent Sessions

You can explicitly exit an agent session using the `copilotkit_exit` function.

```python
# Python agent
from copilotkit.langgraph import copilotkit_exit

async def send_email_node(state: EmailAgentState, config: RunnableConfig):
    """Send an email."""
    
    await copilotkit_exit(config)
    
    # Process the email sending
    # ...
    
    return {
        "messages": [AIMessage(content="✅ Sent email.")]
    }
```

```typescript
// TypeScript agent
import { copilotkitExit } from "@copilotkit/sdk-js/langgraph";

async function sendEmailNode(state: EmailAgentState, config: RunnableConfig): Promise<{ messages: any[] }> {
    // Send an email.
    
    await copilotkitExit(config);
    
    // Process the email sending
    // ...
    
    return {
        messages: [new AIMessage("✅ Sent email.")]
    };
}
```

## Best Practices for Actions and Tools

1. **Clear Descriptions**: Provide clear descriptions for actions and parameters to help the AI understand when and how to use them.
2. **Validation**: Validate parameters in your handlers to prevent errors.
3. **Error Handling**: Return meaningful error messages when actions fail.
4. **Idempotency**: Design actions to be idempotent when possible to avoid duplicate operations.
5. **Security**: Implement proper authentication and authorization for backend actions.
6. **Feedback**: Provide clear feedback to the user when actions are executed.
7. **Logging**: Log action executions for debugging and monitoring.
8. **Rate Limiting**: Implement rate limiting for actions that could be expensive or potentially abused.
