# Ebisu Relationship Orchestrator Structure and Components

This document provides a comprehensive overview of the Ebisu Relationship Orchestrator frontend structure, components, and patterns that we'll need to migrate to the Zig project.

## Directory Structure

Let's first examine the high-level directory structure of the Ebisu frontend:

```
/ebisu-relationship-orchestrator
├── public/                # Static assets
├── src/                   # Source code
│   ├── components/        # React components
│   │   ├── chat/          # Chat components
│   │   ├── data/          # Data visualization components
│   │   ├── intelligence/  # AI-related components
│   │   ├── layout/        # Layout components
│   │   ├── navigation/    # Navigation components
│   │   ├── panels/        # Panel components for three-panel layout
│   │   ├── ui/            # UI components (shadcn/ui)
│   │   └── watchlist/     # Watchlist components
│   ├── contexts/          # React context providers
│   ├── hooks/             # Custom React hooks
│   ├── lib/               # Utility functions
│   ├── pages/             # Page components
│   ├── services/          # API service functions
│   └── types/             # TypeScript type definitions
├── index.html             # HTML entry point
├── vite.config.ts         # Vite configuration
└── package.json           # Node.js dependencies
```

## Key Components to Migrate

### Panel Components

The panel components form the core of the three-panel layout structure:

```
/src/components/panels
├── ModeConfigs.ts         # Configuration for different panel modes
├── PanelManager.tsx       # Manages panel layout and state
├── PanelProvider.tsx      # Context provider for panel state
├── PanelRegistry.ts       # Registry of available panels
├── center/                # Center panel components
└── right/                 # Right panel components
```

#### PanelManager.tsx

This is the main component that orchestrates the three-panel layout. It uses react-resizable-panels for resizable panels and manages the state of which components are displayed in each panel.

Key features:
- Resizable panels with drag handles
- Panel state management
- Panel content switching
- Responsive design for different screen sizes

```tsx
import { PanelGroup, Panel, PanelResizeHandle } from 'react-resizable-panels';
import { usePanelContext } from './PanelProvider';
import { panelRegistry } from './PanelRegistry';

export function PanelManager() {
  const { centerPanel, rightPanel, leftPanel } = usePanelContext();
  
  return (
    <PanelGroup direction="horizontal">
      {/* Left Panel - typically for chat */}
      <Panel minSize={15} defaultSize={20}>
        {leftPanel && panelRegistry[leftPanel.type]?.component(leftPanel.props)}
      </Panel>
      
      <PanelResizeHandle />
      
      {/* Center Panel - main workspace */}
      <Panel minSize={30} defaultSize={50}>
        {centerPanel && panelRegistry[centerPanel.type]?.component(centerPanel.props)}
      </Panel>
      
      <PanelResizeHandle />
      
      {/* Right Panel - context, details, etc. */}
      <Panel minSize={15} defaultSize={30}>
        {rightPanel && panelRegistry[rightPanel.type]?.component(rightPanel.props)}
      </Panel>
    </PanelGroup>
  );
}
```

#### PanelProvider.tsx

This component provides context for panel state management across the application:

```tsx
import { createContext, useContext, useState } from 'react';

export type PanelConfig = {
  type: string;
  props?: Record<string, any>;
};

type PanelContextType = {
  leftPanel: PanelConfig | null;
  centerPanel: PanelConfig | null;
  rightPanel: PanelConfig | null;
  setLeftPanel: (config: PanelConfig | null) => void;
  setCenterPanel: (config: PanelConfig | null) => void;
  setRightPanel: (config: PanelConfig | null) => void;
};

const PanelContext = createContext<PanelContextType | undefined>(undefined);

export function PanelProvider({ children }) {
  const [leftPanel, setLeftPanel] = useState<PanelConfig | null>(null);
  const [centerPanel, setCenterPanel] = useState<PanelConfig | null>(null);
  const [rightPanel, setRightPanel] = useState<PanelConfig | null>(null);
  
  return (
    <PanelContext.Provider value={{
      leftPanel,
      centerPanel,
      rightPanel,
      setLeftPanel,
      setCenterPanel,
      setRightPanel
    }}>
      {children}
    </PanelContext.Provider>
  );
}

export const usePanelContext = () => {
  const context = useContext(PanelContext);
  if (!context) {
    throw new Error('usePanelContext must be used within a PanelProvider');
  }
  return context;
};
```

### Chat Components

The chat components handle user interactions with the AI:

```
/src/components/chat
├── ChatBubble.tsx         # Individual chat message bubble
├── ChatInput.tsx          # Input field for chat
├── ChatPanel.tsx          # Container for chat interface
├── ChatThread.tsx         # Thread of chat messages
└── types.ts               # TypeScript types for chat
```

#### ChatPanel.tsx

This is the main chat interface component:

```tsx
import { useState } from 'react';
import { ChatBubble } from './ChatBubble';
import { ChatInput } from './ChatInput';
import { ChatThread } from './ChatThread';
import { Message } from './types';

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // In Vite, this would call an API
      // In Next.js with CopilotKit, we'll use CopilotKit's chat functionality
      const response = await fetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ message: content }),
      });
      
      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4">
        <ChatThread messages={messages} />
      </div>
      <div className="border-t p-4">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}
```

### Data Visualization Components

These components handle data display and visualization:

```
/src/components/data
├── AccountCard.tsx        # Card displaying account information
├── ContactCard.tsx        # Card displaying contact information
├── DataGrid.tsx           # Grid for displaying tabular data
├── DataTable.tsx          # Table component for structured data
├── MetricCard.tsx         # Card displaying key metrics
├── OpportunityCard.tsx    # Card for sales opportunities
├── PipelineChart.tsx      # Chart for sales pipeline visualization
├── RevenueChart.tsx       # Chart for revenue visualization
├── StatusBadge.tsx        # Badge showing status information
├── Timeline.tsx           # Timeline visualization
└── TrendChart.tsx         # Chart showing trends over time
```

### Intelligence Components

These components handle AI-powered features:

```
/src/components/intelligence
├── AIAssistant.tsx        # AI assistant interface
├── AIInsights.tsx         # AI-generated insights
├── AIRecommendations.tsx  # AI-generated recommendations
├── EntityAnalysis.tsx     # AI analysis of entities
├── SentimentAnalysis.tsx  # Sentiment analysis visualization
└── SmartSuggestions.tsx   # AI-powered suggestions
```

### UI Components

The UI components are based on shadcn/ui and provide the basic building blocks:

```
/src/components/ui
├── accordion.tsx          # Accordion component
├── alert-dialog.tsx       # Alert dialog component
├── avatar.tsx             # Avatar component
├── badge.tsx              # Badge component
├── button.tsx             # Button component
├── calendar.tsx           # Calendar component
├── card.tsx               # Card component
├── checkbox.tsx           # Checkbox component
├── dialog.tsx             # Dialog component
├── dropdown-menu.tsx      # Dropdown menu component
├── input.tsx              # Input component
├── label.tsx              # Label component
├── popover.tsx            # Popover component
├── select.tsx             # Select component
├── separator.tsx          # Separator component
├── sheet.tsx              # Sheet component
├── tabs.tsx               # Tabs component
├── textarea.tsx           # Textarea component
├── toast.tsx              # Toast notification component
└── tooltip.tsx            # Tooltip component
```

## Key TypeScript Types

Important types that will need to be migrated:

```
/src/types
├── account.ts             # Account-related types
├── contact.ts             # Contact-related types
├── opportunity.ts         # Opportunity-related types
├── panel.ts               # Panel-related types
├── user.ts                # User-related types
└── common.ts              # Common shared types
```

## Hooks and Context

Custom hooks and context providers that will need to be migrated:

```
/src/hooks
├── useAuth.ts             # Authentication hook
├── useData.ts             # Data fetching hook
├── useDebounce.ts         # Debounce hook
├── useLocalStorage.ts     # Local storage hook
├── useMediaQuery.ts       # Media query hook
├── usePanels.ts           # Panel management hook
└── useToast.ts            # Toast notification hook

/src/contexts
├── AuthContext.tsx        # Authentication context
└── ThemeContext.tsx       # Theme context
```

## Key Implementation Patterns

1. **Panel System**: Three-panel layout with resizable panels
2. **Context Providers**: React context for state management
3. **Custom Hooks**: Abstraction of common functionality
4. **Component Composition**: Building complex UIs from smaller components
5. **Shadcn/UI**: Using shadcn/ui for consistent design system
6. **TypeScript**: Strong typing throughout the application
7. **Data Fetching**: API service functions for data retrieval

## Styling Approach

The project uses:

1. **Tailwind CSS**: For utility-first styling
2. **CSS Modules**: For component-specific styles
3. **CSS Variables**: For theme customization

## Migration Considerations

When migrating these components to the Zig project, we'll need to:

1. **Adapt to Next.js**: Convert components to work with Next.js App Router
2. **Integrate with CopilotKit**: Replace custom AI implementations with CopilotKit
3. **Server vs. Client Components**: Decide which components should be server or client components
4. **Data Fetching**: Update data fetching to use Next.js patterns
5. **Routing**: Update routing to use Next.js App Router
6. **Authentication**: Implement authentication with Supabase as planned

## Migration Priority

1. **Panel System**: The foundation for the UI layout
2. **Chat Components**: Core functionality for AI interaction
3. **UI Components**: Basic building blocks
4. **Data Visualization**: For displaying sales data
5. **Intelligence Components**: AI-powered features
6. **Contexts and Hooks**: Supporting functionality
