# Ebisu - Sales Relationship Orchestrator Project Plan

## Project Overview
Ebisu is a "Cursor for Sales Teams" application that transforms how sales professionals build and manage relationships. The application uses AI to assist sales teams in discovering prospects, qualifying leads, orchestrating outreach, managing responses, and monitoring pipeline health.

## Tech Stack
- **Frontend**: Next.js (React)
- **Backend**: FastAPI (Python)
- **Database**: Supabase
- **AI Integration**: CopilotKit.ai

## Current Status
- Some frontend components have been developed in Vite/React
- Planning to migrate these components to Next.js
- Will integrate with CopilotKit.ai for generative UI capabilities
- Backend architecture is being developed separately

## Migration Strategy: Vite to Next.js

### Phase 1: Project Setup
1. Set up a new Next.js project with the appropriate configuration
2. Configure Supabase client integration
3. Set up CopilotKit.ai integration
4. Establish folder structure following Next.js best practices

### Phase 2: Component Migration
1. Identify all components from the Vite project to be migrated
2. Adapt components to Next.js patterns (considering differences in routing, data fetching, etc.)
3. Ensure styling approaches are compatible (CSS modules, styled-components, etc.)
4. Test components in isolation to verify functionality

### Phase 3: CopilotKit.ai Integration
1. Implement CopilotKit provider at the application root
2. Create AI-powered UI components using CopilotKit
3. Develop generative UI patterns that adapt based on user queries
4. Implement context-aware AI assistance throughout the application

### Phase 4: Backend Integration
1. Connect frontend to FastAPI backend endpoints
2. Implement authentication and authorization flows
3. Set up data fetching and state management
4. Create API service layer for communication with backend

## Key Components to Implement

### Core UI Framework
- Three-panel adaptive layout (similar to VS Code)
- Dark theme (#0f0f0f background)
- AI Chat panel (left)
- Context-aware workspace (center/right)
- Dynamic panel configuration based on workflow

### Workflow-Specific Components
1. **Discover Module**
   - Prospect search interface
   - AI-powered research display
   - Company and contact information cards

2. **Qualify Module**
   - Lead scoring interface
   - Qualification criteria management
   - Data visualization for prospect evaluation

3. **Orchestrate Module**
   - Outreach composition with AI assistance
   - Timing and context suggestions
   - Template management with personalization

4. **Manage Module**
   - Response tracking
   - Conversation history
   - Relationship progression visualization

5. **Monitor Module**
   - Pipeline health dashboard
   - Performance metrics
   - Optimization suggestions

### CopilotKit.ai Integration Points
- AI chat interface for navigation and assistance
- Generative UI elements that adapt to user queries
- Context-aware suggestions and actions
- Document and conversation analysis
- Personalized outreach generation

## Implementation Considerations
1. Ensure components are modular and reusable
2. Implement responsive design for various screen sizes
3. Focus on performance optimization
4. Maintain accessibility standards
5. Establish consistent design language across the application

## Next Steps
1. Clone the Vite repository to extract components
2. Set up the Next.js project structure
3. Begin component migration process
4. Integrate CopilotKit.ai
5. Connect with backend services once available
