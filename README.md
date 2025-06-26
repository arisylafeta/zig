# Ebisu AI - LangGraph + CopilotKit Integration

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app) that integrates a LangGraph AI agent with CopilotKit for prospect search functionality.

## ✨ Features

- **Real-time Agent State Rendering**: See live progress updates as the agent works
- **Interactive People Search**: Natural language prospect searching using Apollo API
- **Progress Tracking**: Visual indicators and logs of agent activities
- **Human-in-the-loop**: Chat interface for guided prospect discovery
- **Rich Data Display**: Comprehensive prospect information in an interactive table

## Environment Setup

Create a `.env.local` file in the root directory with the following variables:

```bash
# CopilotKit Configuration
NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL=http://localhost:8123
NEXT_PUBLIC_COPILOT_API_KEY=your_copilot_cloud_api_key_here
NEXT_PUBLIC_COPILOTKIT_AGENT_NAME=zig

# OpenAI API Key (for the agent)
OPENAI_API_KEY=your_openai_api_key_here
```

For the agent directory, create a `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
APOLLO_API_KEY=your_apollo_api_key_here
```

## Getting Started

First, start the LangGraph agent:

```bash
cd agent
langgraph up
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

Navigate to [http://localhost:3000/copilotkit](http://localhost:3000/copilotkit) to access the AI-powered prospect search interface.

## 🚀 How It Works

### State Emission & Real-time Updates
Following the [CopilotKit + LangGraph tutorial](https://dev.to/copilotkit/easily-build-a-ui-for-your-langgraph-ai-agent-in-minutes-with-copilotkit-1khj), this implementation features:

1. **Progress Logging**: Real-time updates during tool execution
2. **State Rendering**: Live progress display in the chat interface using `useCoAgentStateRender`
3. **Status Tracking**: Visual indicators showing current agent status
4. **Bidirectional State**: Synchronized state between agent and UI

### Agent Workflow
1. User makes a search request via chat
2. Agent processes the request and emits progress states
3. Apollo people search tool is executed with real-time logging
4. Results are processed and displayed in the table
5. User can refine search or start new queries

## Usage Examples

Try these search queries in the chat:

- "Search for software engineers at tech companies in San Francisco"
- "Find marketing managers at SaaS companies with 100-500 employees"
- "Look for sales directors in the healthcare industry in New York"
- "Search for product managers at startups in Austin"

## Architecture

- **Frontend**: Next.js with CopilotKit React components
- **Agent**: LangGraph with Python for workflow orchestration
- **Tools**: Apollo API for people search functionality
- **State Management**: CopilotKit's shared state system
- **Real-time Updates**: WebSocket-based state emission

## Learn More

To learn more about the technologies used:

- [CopilotKit Documentation](https://docs.copilotkit.ai/) - Building AI copilots and agents
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - Agent workflow orchestration
- [Next.js Documentation](https://nextjs.org/docs) - React framework features and API
- [Apollo API Documentation](https://docs.apollo.io/) - People and company search

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
