# CopilotKit Introduction

## What is CopilotKit?

CopilotKit is a framework for building AI copilots and integrating them into React applications. It provides a set of tools that make it easy to let users work alongside Large Language Models (LLMs) to accomplish generative tasks directly in your application. Instead of just using the LLM to generate content, you can let it take direct action alongside your users.

## Core Features

- **Generative UI**: Create UI components that adapt based on user queries and context
- **AI Chat Interfaces**: Multiple chat interface options (sidebar, popup, full-page)
- **Frontend Actions**: Allow AI to trigger actions in your UI
- **Backend Integration**: Connect to backend services and data sources
- **Human-in-the-Loop**: Support for interrupting AI processing to ask for user input
- **Context Awareness**: Provide rich context to the AI about the current application state

## Key Components

CopilotKit consists of several packages:

1. **@copilotkit/react-core**: Core functionality for React applications
2. **@copilotkit/react-ui**: Pre-built UI components for chat interfaces
3. **@copilotkit/react-textarea**: AI-powered text editing components
4. **@copilotkit/runtime**: Backend runtime for handling AI requests
5. **@copilotkit/sdk-js**: JavaScript SDK for building agents
6. **@copilotkit/shared**: Shared utilities and types

## Architecture Overview

CopilotKit follows a client-server architecture:

- **Frontend**: React components that provide the user interface and context
- **Backend**: Runtime that handles AI requests, manages agents, and connects to external services
- **Communication**: GraphQL-based communication between frontend and backend

## Use Cases

CopilotKit is designed for a wide range of applications:

1. **Customer Support**: AI assistants that can answer questions and take actions
2. **Data Analysis**: Interactive data exploration and visualization
3. **Content Creation**: AI-assisted writing and editing
4. **Workflow Automation**: Guiding users through complex processes
5. **Research**: Helping users gather and synthesize information

## Getting Started

To get started with CopilotKit:

1. Install the necessary packages:
   ```bash
   npm install @copilotkit/react-ui @copilotkit/react-core
   ```

2. Wrap your application with the CopilotKit provider:
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

3. Add a chat interface:
   ```jsx
   import { CopilotSidebar } from "@copilotkit/react-ui";

   function MyComponent() {
     return (
       <div>
         <CopilotSidebar />
         {/* Your component content */}
       </div>
     );
   }
   ```

## Examples and Templates

CopilotKit provides several example projects and templates to help you get started:

1. **coagents-starter**: Basic starter template for CoAgents
2. **saas-dynamic-dashboards**: Example of dynamic dashboards
3. **coagents-research-canvas**: Research canvas application
4. **coagents-ai-researcher**: AI researcher application
5. **coagents-shared-state**: Example of shared state between agents
6. **copilot-chat-with-your-data**: Chat with your data example

These examples can be found in the [CopilotKit GitHub repository](https://github.com/CopilotKit/CopilotKit/tree/main/examples).
