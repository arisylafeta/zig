# Panel System Architecture

This document provides a detailed analysis of the panel system in the Ebisu Relationship Orchestrator, which implements the three-panel layout inspired by VS Code.

## Core Components

The panel system consists of several key components:

1. **PanelManager**: Orchestrates the overall layout
2. **PanelProvider**: Provides context for panel state
3. **PanelRegistry**: Registers available panel components
4. **ModeConfigs**: Defines different panel configurations

Let's examine each component in detail.

## PanelManager.tsx

The PanelManager is responsible for rendering the three-panel layout and handling resizing. It uses `react-resizable-panels` for the resizable panel functionality.

```tsx
import { PanelGroup, Panel, PanelResizeHandle } from 'react-resizable-panels';
import { usePanelContext } from './PanelProvider';
import { panelRegistry } from './PanelRegistry';
import { ResizeHandleIcon } from '../ui/icons';

export function PanelManager() {
  const { leftPanel, centerPanel, rightPanel, panelLayout } = usePanelContext();
  
  // Determine if panels should be shown based on layout mode
  const showLeftPanel = panelLayout.includes('left');
  const showCenterPanel = panelLayout.includes('center');
  const showRightPanel = panelLayout.includes('right');
  
  return (
    <div className="h-screen w-screen overflow-hidden">
      <PanelGroup direction="horizontal" className="h-full">
        {/* Left Panel - typically for chat */}
        {showLeftPanel && (
          <>
            <Panel minSize={15} defaultSize={20} className="bg-background">
              <div className="h-full overflow-auto">
                {leftPanel && panelRegistry[leftPanel.type]?.component(leftPanel.props)}
              </div>
            </Panel>
            <PanelResizeHandle className="w-1 bg-border hover:bg-primary hover:w-1.5 transition-all">
              <ResizeHandleIcon />
            </PanelResizeHandle>
          </>
        )}
        
        {/* Center Panel - main workspace */}
        {showCenterPanel && (
          <>
            <Panel minSize={30} defaultSize={showLeftPanel && showRightPanel ? 50 : 70} className="bg-background">
              <div className="h-full overflow-auto">
                {centerPanel && panelRegistry[centerPanel.type]?.component(centerPanel.props)}
              </div>
            </Panel>
            {showRightPanel && (
              <PanelResizeHandle className="w-1 bg-border hover:bg-primary hover:w-1.5 transition-all">
                <ResizeHandleIcon />
              </PanelResizeHandle>
            )}
          </>
        )}
        
        {/* Right Panel - context, details, etc. */}
        {showRightPanel && (
          <Panel minSize={15} defaultSize={30} className="bg-background">
            <div className="h-full overflow-auto">
              {rightPanel && panelRegistry[rightPanel.type]?.component(rightPanel.props)}
            </div>
          </Panel>
        )}
      </PanelGroup>
    </div>
  );
}
```

## PanelProvider.tsx

The PanelProvider manages the state of which components are displayed in each panel and provides this state through React context.

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';
import { defaultPanelConfig } from './ModeConfigs';

export type PanelConfig = {
  type: string;
  props?: Record<string, any>;
};

export type PanelLayout = ('left' | 'center' | 'right')[];

type PanelContextType = {
  leftPanel: PanelConfig | null;
  centerPanel: PanelConfig | null;
  rightPanel: PanelConfig | null;
  panelLayout: PanelLayout;
  setLeftPanel: (config: PanelConfig | null) => void;
  setCenterPanel: (config: PanelConfig | null) => void;
  setRightPanel: (config: PanelConfig | null) => void;
  setPanelLayout: (layout: PanelLayout) => void;
  setMode: (mode: string) => void;
};

const PanelContext = createContext<PanelContextType | undefined>(undefined);

interface PanelProviderProps {
  children: ReactNode;
  initialMode?: string;
}

export function PanelProvider({ children, initialMode = 'default' }: PanelProviderProps) {
  const initialConfig = defaultPanelConfig[initialMode] || defaultPanelConfig.default;
  
  const [leftPanel, setLeftPanel] = useState<PanelConfig | null>(initialConfig.left);
  const [centerPanel, setCenterPanel] = useState<PanelConfig | null>(initialConfig.center);
  const [rightPanel, setRightPanel] = useState<PanelConfig | null>(initialConfig.right);
  const [panelLayout, setPanelLayout] = useState<PanelLayout>(initialConfig.layout || ['left', 'center', 'right']);
  
  const setMode = (mode: string) => {
    const config = defaultPanelConfig[mode] || defaultPanelConfig.default;
    setLeftPanel(config.left);
    setCenterPanel(config.center);
    setRightPanel(config.right);
    setPanelLayout(config.layout || ['left', 'center', 'right']);
  };
  
  return (
    <PanelContext.Provider value={{
      leftPanel,
      centerPanel,
      rightPanel,
      panelLayout,
      setLeftPanel,
      setCenterPanel,
      setRightPanel,
      setPanelLayout,
      setMode
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

## PanelRegistry.ts

The PanelRegistry maintains a mapping of panel types to their corresponding components, allowing for dynamic panel content.

```tsx
import { ReactNode } from 'react';
import { ChatPanel } from '../chat/ChatPanel';
import { AccountsPanel } from './center/AccountsPanel';
import { ContactsPanel } from './center/ContactsPanel';
import { OpportunitiesPanel } from './center/OpportunitiesPanel';
import { DashboardPanel } from './center/DashboardPanel';
import { AccountDetailPanel } from './right/AccountDetailPanel';
import { ContactDetailPanel } from './right/ContactDetailPanel';
import { OpportunityDetailPanel } from './right/OpportunityDetailPanel';
import { AIInsightsPanel } from './right/AIInsightsPanel';

type PanelComponent = (props?: Record<string, any>) => ReactNode;

interface PanelRegistryItem {
  component: PanelComponent;
  title: string;
  description?: string;
}

export const panelRegistry: Record<string, PanelRegistryItem> = {
  // Left panel components
  'chat': {
    component: (props) => <ChatPanel {...props} />,
    title: 'Chat',
    description: 'AI assistant chat interface'
  },
  
  // Center panel components
  'accounts': {
    component: (props) => <AccountsPanel {...props} />,
    title: 'Accounts',
    description: 'Manage customer accounts'
  },
  'contacts': {
    component: (props) => <ContactsPanel {...props} />,
    title: 'Contacts',
    description: 'Manage customer contacts'
  },
  'opportunities': {
    component: (props) => <OpportunitiesPanel {...props} />,
    title: 'Opportunities',
    description: 'Manage sales opportunities'
  },
  'dashboard': {
    component: (props) => <DashboardPanel {...props} />,
    title: 'Dashboard',
    description: 'Sales performance dashboard'
  },
  
  // Right panel components
  'account-detail': {
    component: (props) => <AccountDetailPanel {...props} />,
    title: 'Account Details',
    description: 'View account details'
  },
  'contact-detail': {
    component: (props) => <ContactDetailPanel {...props} />,
    title: 'Contact Details',
    description: 'View contact details'
  },
  'opportunity-detail': {
    component: (props) => <OpportunityDetailPanel {...props} />,
    title: 'Opportunity Details',
    description: 'View opportunity details'
  },
  'ai-insights': {
    component: (props) => <AIInsightsPanel {...props} />,
    title: 'AI Insights',
    description: 'AI-generated insights'
  }
};
```

## ModeConfigs.ts

ModeConfigs defines different panel configurations for various application modes.

```tsx
import { PanelConfig, PanelLayout } from './PanelProvider';

interface PanelModeConfig {
  left: PanelConfig | null;
  center: PanelConfig | null;
  right: PanelConfig | null;
  layout: PanelLayout;
}

export const defaultPanelConfig: Record<string, PanelModeConfig> = {
  // Default three-panel layout
  'default': {
    left: { type: 'chat' },
    center: { type: 'dashboard' },
    right: { type: 'ai-insights' },
    layout: ['left', 'center', 'right']
  },
  
  // Account-focused layout
  'accounts': {
    left: { type: 'chat' },
    center: { type: 'accounts' },
    right: { type: 'account-detail' },
    layout: ['left', 'center', 'right']
  },
  
  // Contact-focused layout
  'contacts': {
    left: { type: 'chat' },
    center: { type: 'contacts' },
    right: { type: 'contact-detail' },
    layout: ['left', 'center', 'right']
  },
  
  // Opportunity-focused layout
  'opportunities': {
    left: { type: 'chat' },
    center: { type: 'opportunities' },
    right: { type: 'opportunity-detail' },
    layout: ['left', 'center', 'right']
  },
  
  // Chat-focused layout (expanded chat)
  'chat-focus': {
    left: { type: 'chat' },
    center: null,
    right: { type: 'ai-insights' },
    layout: ['left', 'right']
  },
  
  // Dashboard-focused layout (no chat)
  'dashboard-focus': {
    left: null,
    center: { type: 'dashboard' },
    right: { type: 'ai-insights' },
    layout: ['center', 'right']
  }
};
```

## Panel Components

The panel system includes various panel components for different sections of the application:

### Center Panel Components

Center panel components typically display lists or grids of data:

```
/src/components/panels/center
├── AccountsPanel.tsx      # List of accounts
├── ContactsPanel.tsx      # List of contacts
├── DashboardPanel.tsx     # Dashboard with metrics and charts
├── OpportunitiesPanel.tsx # List of opportunities
```

### Right Panel Components

Right panel components typically display details or context:

```
/src/components/panels/right
├── AccountDetailPanel.tsx     # Account details
├── AIInsightsPanel.tsx        # AI insights for the selected item
├── ContactDetailPanel.tsx     # Contact details
├── OpportunityDetailPanel.tsx # Opportunity details
```

## Usage Example

Here's how the panel system is used in the application:

```tsx
import { PanelProvider } from './components/panels/PanelProvider';
import { PanelManager } from './components/panels/PanelManager';
import { AppHeader } from './components/layout/AppHeader';

function App() {
  return (
    <PanelProvider initialMode="default">
      <div className="flex flex-col h-screen">
        <AppHeader />
        <div className="flex-1">
          <PanelManager />
        </div>
      </div>
    </PanelProvider>
  );
}
```

To change the panel mode:

```tsx
import { usePanelContext } from './components/panels/PanelProvider';

function Navigation() {
  const { setMode } = usePanelContext();
  
  return (
    <nav>
      <button onClick={() => setMode('accounts')}>Accounts</button>
      <button onClick={() => setMode('contacts')}>Contacts</button>
      <button onClick={() => setMode('opportunities')}>Opportunities</button>
      <button onClick={() => setMode('dashboard-focus')}>Dashboard</button>
    </nav>
  );
}
```

To update an individual panel:

```tsx
import { usePanelContext } from './components/panels/PanelProvider';

function AccountList({ accounts }) {
  const { setRightPanel } = usePanelContext();
  
  const handleAccountClick = (account) => {
    setRightPanel({
      type: 'account-detail',
      props: { accountId: account.id }
    });
  };
  
  return (
    <ul>
      {accounts.map(account => (
        <li key={account.id} onClick={() => handleAccountClick(account)}>
          {account.name}
        </li>
      ))}
    </ul>
  );
}
```

## Integration with CopilotKit

When integrating with CopilotKit, we'll need to:

1. Make panel components readable by CopilotKit using `useCopilotReadable`
2. Allow CopilotKit to control panels using `useCopilotAction`
3. Provide context about the current panel state to the AI

Example integration:

```tsx
import { useCopilotReadable, useCopilotAction } from '@copilotkit/react-core';
import { usePanelContext } from './PanelProvider';

function PanelManager() {
  const { leftPanel, centerPanel, rightPanel, panelLayout, setMode } = usePanelContext();
  
  // Make panel state readable by CopilotKit
  useCopilotReadable({
    description: "Current panel layout configuration",
    value: {
      leftPanel,
      centerPanel,
      rightPanel,
      panelLayout
    }
  }, [leftPanel, centerPanel, rightPanel, panelLayout]);
  
  // Allow CopilotKit to change panel mode
  useCopilotAction({
    name: "changePanelMode",
    description: "Change the panel layout mode",
    parameters: [{
      name: "mode",
      description: "The mode to switch to (default, accounts, contacts, opportunities, chat-focus, dashboard-focus)",
      required: true
    }],
    handler: ({ mode }) => {
      setMode(mode);
      return `Panel mode changed to ${mode}`;
    }
  });
  
  // Rest of the component...
}
```

## Migration Strategy

When migrating this panel system to the Zig project:

1. **Create the core panel components** in the Zig project
2. **Integrate with CopilotKit** for AI-driven panel control
3. **Adapt to Next.js App Router** patterns
4. **Ensure responsive design** works across devices
5. **Implement panel persistence** using local storage or server state

This panel system will form the foundation of the UI for the Ebisu application in the Zig project.
