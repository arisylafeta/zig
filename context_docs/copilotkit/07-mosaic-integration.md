React Mosaic: First Principles Overview
Core Concepts
React Mosaic is built around a simple binary tree structure called MosaicNode<T>. Here's how it works at a fundamental level:

Binary Tree Structure: Each node in the layout is either:
A leaf (actual content panel)
A branch with two children and a divider between them
Node Identification: Each panel is identified by a unique key (T) which can be a string or number.
Rendering System:
The renderTile function converts your panel ID into an actual React component
The binary tree structure determines the layout arrangement
Window Management:
MosaicWindow component wraps your content with a toolbar and controls
Provides drag-and-drop functionality for rearranging panels
Supports splitting, expanding, and removing panels
Layout Organization
The layout is organized as a nested binary tree where:

typescript
type MosaicNode<T> = T | {
  direction: 'row' | 'column';
  first: MosaicNode<T>;
  second: MosaicNode<T>;
  splitPercentage?: number;
}
For example, a layout with three panels might be structured as:

typescript
{
  direction: 'row',
  first: 'chat-panel',
  second: {
    direction: 'column',
    first: 'search-panel',
    second: 'details-panel',
    splitPercentage: 50
  },
  splitPercentage: 30
}
This creates a layout with a chat panel on the left (30% width) and two vertically stacked panels on the right (search on top, details on bottom).

CopilotKit Integration
CopilotKit can be integrated with React Mosaic through custom actions that manipulate the Mosaic layout. Here's how it works:

State Management:
Store the Mosaic layout in React state
Register actions with CopilotKit that modify this state
Panel Actions:
Create actions for adding, removing, and rearranging panels
Define actions for changing panel content based on user queries
Context Access:
Use the MosaicContext to access tree manipulation methods
Create wrappers around these methods for CopilotKit actions
Mermaid Diagram: FinTech Payment Providers Flow
Here's a diagram showing how a user interaction would flow through the system for your FinTech use case:

mermaid
sequenceDiagram
    participant User
    participant ChatPanel
    participant CopilotKit
    participant MosaicLayout
    participant SearchPanel
    participant DetailsPanel
    participant Apollo

    User->>ChatPanel: "Find international payment providers"
    ChatPanel->>CopilotKit: Process user query
    CopilotKit->>MosaicLayout: Show search panel (addPanel action)
    MosaicLayout-->>SearchPanel: Create and display
    CopilotKit->>Apollo: Query payment providers data
    Apollo-->>CopilotKit: Return provider list
    CopilotKit->>SearchPanel: Display provider list
    User->>SearchPanel: Select a provider
    SearchPanel->>CopilotKit: Process selection
    CopilotKit->>MosaicLayout: Show details panel (addPanel action)
    MosaicLayout-->>DetailsPanel: Create and display
    CopilotKit->>Apollo: Query detailed provider info
    Apollo-->>CopilotKit: Return provider details
    CopilotKit->>DetailsPanel: Display provider details
Example Implementation
Here's how you would implement this flow:

Basic Layout Setup:
typescript
const [layout, setLayout] = useState({
  direction: 'row',
  first: 'chat',
  second: null,
  splitPercentage: 30
});

// Panel components map
const panels = {
  'chat': ChatPanel,
  'search': SearchPanel,
  'details': DetailsPanel
};
CopilotKit Actions:
typescript
// Register actions with CopilotKit
useCopilotAction({
  name: "findPaymentProviders",
  description: "Search for payment providers based on criteria",
  parameters: [
    { name: "international", type: "boolean", description: "Whether to find international providers" },
    { name: "region", type: "string", description: "Specific region to filter by" }
  ],
  handler: async ({ international, region }) => {
    // 1. Show search panel if not visible
    setLayout(current => ({
      direction: 'row',
      first: 'chat',
      second: {
        direction: 'column',
        first: 'search',
        second: null,
        splitPercentage: 100
      },
      splitPercentage: 30
    }));
    
    // 2. Query data using Apollo
    const { data } = await apolloClient.query({
      query: PAYMENT_PROVIDERS_QUERY,
      variables: { international, region }
    });
    
    // 3. Update search panel state with results
    setSearchResults(data.paymentProviders);
    
    return { 
      success: true, 
      message: `Found ${data.paymentProviders.length} payment providers`
    };
  }
});

// Action to show provider details
useCopilotAction({
  name: "showProviderDetails",
  description: "Show detailed information about a payment provider",
  parameters: [
    { name: "providerId", type: "string", description: "ID of the provider to show details for" }
  ],
  handler: async ({ providerId }) => {
    // 1. Update layout to include details panel if not already visible
    setLayout(current => {
      // If search panel is already visible
      if (current.second && typeof current.second !== 'string') {
        return {
          ...current,
          second: {
            direction: 'column',
            first: 'search',
            second: 'details',
            splitPercentage: 50
          }
        };
      }
      
      // If no panels are visible yet
      return {
        direction: 'row',
        first: 'chat',
        second: {
          direction: 'column',
          first: 'search',
          second: 'details',
          splitPercentage: 50
        },
        splitPercentage: 30
      };
    });
    
    // 2. Query provider details using Apollo
    const { data } = await apolloClient.query({
      query: PROVIDER_DETAILS_QUERY,
      variables: { providerId }
    });
    
    // 3. Update details panel state
    setProviderDetails(data.provider);
    
    return { 
      success: true, 
      message: `Showing details for ${data.provider.name}`
    };
  }
});
Mosaic Layout Component:
typescript
function AppLayout() {
  return (
    <div className="app-container">
      <Mosaic<string>
        renderTile={(id, path) => {
          const Panel = panels[id] || (() => <div>Panel not found</div>);
          
          return (
            <MosaicWindow<string>
              path={path}
              title={id.charAt(0).toUpperCase() + id.slice(1)}
            >
              <Panel id={id} />
            </MosaicWindow>
          );
        }}
        value={layout}
        onChange={setLayout}
        className="mosaic-blueprint-theme"
      />
    </div>
  );
}
Advantages for Your Use Case
Flexibility: React Mosaic provides a flexible layout system that can adapt to different user needs.
User Control: Users can resize and rearrange panels based on their preferences.
AI-Driven Layout: CopilotKit can dynamically modify the layout based on user queries.
Focused Workflows: Each panel can focus on a specific task (search, details, chat) while maintaining context.
Simplified Implementation: Using React Mosaic eliminates the need to build a custom panel system.
This approach would work well for your FinTech use case, allowing users to search for international payment providers through the chat interface, view results in a search panel, and examine details in a separate panel - all orchestrated by CopilotKit based on natural language queries.