# Zig Project Structure and Architecture

This document provides a comprehensive overview of the Zig project structure, patterns, and architecture.

## Directory Structure

Let's first examine the high-level directory structure of the Zig project:

```
/zig
├── agent/                 # Python backend with LangGraph integration
│   ├── zig/               # Python agent code
│   ├── poetry.lock        # Python dependencies lock file
│   └── pyproject.toml     # Python project configuration
├── public/                # Static assets
├── src/                   # Frontend source code
│   ├── app/               # Next.js App Router structure
│   ├── components/        # React components
│   └── lib/               # Utility functions and shared code
├── next.config.ts         # Next.js configuration
├── package.json           # Node.js dependencies
└── tsconfig.json          # TypeScript configuration
```

## Frontend Architecture (Next.js)

The frontend is built with Next.js 15.3.4 using the App Router pattern. Here's a breakdown of the key directories and files:

### App Directory Structure

```
/src/app
├── api/                   # API routes
│   └── copilotkit/        # CopilotKit API endpoint
├── copilotkit/            # CopilotKit integration
│   ├── layout.tsx         # CopilotKit provider wrapper
│   └── page.tsx           # CopilotKit demo page
├── globals.css            # Global CSS styles
├── layout.tsx             # Root layout with font configuration
└── page.tsx               # Home page component
```

### Key Patterns

1. **App Router**: Uses Next.js App Router for file-based routing
2. **Layout Nesting**: Uses nested layouts for shared UI across routes
3. **Server Components**: Default to React Server Components
4. **Client Components**: Uses "use client" directive when needed
5. **Font Optimization**: Uses Next.js font optimization with Geist font

## CopilotKit Integration

CopilotKit is integrated throughout the application with the following structure:

### Provider Setup

The CopilotKit provider is set up in `/src/app/copilotkit/layout.tsx`:

```tsx
import "@copilotkit/react-ui/styles.css";
import React, { ReactNode } from "react";
import { CopilotKit } from "@copilotkit/react-core";

// Where CopilotKit will proxy requests to
const runtimeUrl = process.env.NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL
// When using Copilot Cloud, all we need is the publicApiKey
const publicApiKey = process.env.NEXT_PUBLIC_COPILOT_API_KEY;
// The name of the agent that we'll be using
const agentName = process.env.NEXT_PUBLIC_COPILOTKIT_AGENT_NAME

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <CopilotKit 
      runtimeUrl={runtimeUrl}
      publicApiKey={publicApiKey}
      agent={agentName}
    >
      {children}
    </CopilotKit>
  );
}
```

### API Endpoint

The CopilotKit API endpoint is set up in `/src/app/api/copilotkit/route.ts`:

```tsx
import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  ExperimentalEmptyAdapter,
  langGraphPlatformEndpoint,
} from "@copilotkit/runtime";

const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  remoteEndpoints: [
    langGraphPlatformEndpoint({
      deploymentUrl: process.env.LANGGRAPH_DEPLOYMENT_URL || "",
      langsmithApiKey: process.env.LANGSMITH_API_KEY || "",
      agents: [{
          name: process.env.NEXT_PUBLIC_COPILOTKIT_AGENT_NAME || "",
          description: process.env.NEXT_PUBLIC_COPILOTKIT_AGENT_DESCRIPTION || 'A helpful LLM agent.'
      }]
    }),
  ],
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

### Demo Page

The CopilotKit demo page in `/src/app/copilotkit/page.tsx` demonstrates:

1. **Frontend Actions**: Using `useCopilotAction` to define actions the AI can perform
2. **Shared State**: Using `useCoAgent` to maintain shared state between UI and agent
3. **Generative UI**: Implementing components that can be rendered by the AI
4. **Side Chat**: Custom chat component implementation

## Backend Architecture (Python)

The backend is built with Python using LangGraph for agent orchestration:

### Agent Directory Structure

```
/agent
├── zig/                   # Main agent code
│   ├── demo.py            # Demo script
│   ├── agent.py           # Agent implementation
│   └── utils/             # Utility functions
├── pyproject.toml         # Python dependencies
└── poetry.lock            # Locked dependencies
```

### Key Dependencies

1. **LangGraph**: For agent orchestration and state management
2. **LangChain**: For LLM chains and tools
3. **OpenAI**: For LLM integration
4. **CopilotKit**: For connecting with the frontend

## Environment Configuration

The project uses environment variables for configuration:

1. **NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL**: URL for the CopilotKit runtime
2. **NEXT_PUBLIC_COPILOT_API_KEY**: API key for Copilot Cloud
3. **NEXT_PUBLIC_COPILOTKIT_AGENT_NAME**: Name of the agent
4. **LANGGRAPH_DEPLOYMENT_URL**: URL for LangGraph deployment
5. **LANGSMITH_API_KEY**: API key for LangSmith

## Component Architecture

The project uses a minimal component structure:

1. **SideChat**: A custom chat component in `/src/components/side-chat.tsx`
2. **UI Components**: Simple UI components for the demo page

## Styling Approach

The project uses:

1. **Tailwind CSS**: For utility-first styling
2. **CSS Variables**: For theme customization
3. **CopilotKit CSS**: Imported from `@copilotkit/react-ui/styles.css`

## Key Implementation Patterns

1. **Theme Customization**: Using CSS variables for theming
2. **State Management**: Using React's useState and CopilotKit's useCoAgent
3. **Action Registration**: Using useCopilotAction to register actions
4. **Generative UI**: Using render functions to create AI-driven UI
5. **Environment Variables**: Using Next.js environment variables

## API Layer

The API layer is minimal and consists of:

1. **CopilotKit API**: Endpoint for CopilotKit communication
2. **LangGraph Integration**: Connection to LangGraph for agent orchestration

This structure provides a foundation for building AI-powered applications with CopilotKit and Next.js.
