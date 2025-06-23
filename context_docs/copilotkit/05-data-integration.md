# CopilotKit Data Integration

One of the most powerful features of CopilotKit is its ability to integrate with your application's data. This allows the AI to access and understand the context of your application, making it more helpful and relevant to users.

## Frontend Data Integration with useCopilotReadable

The `useCopilotReadable` hook allows you to provide data from your frontend application to the AI.

```jsx
import { useCopilotReadable } from "@copilotkit/react-core";

function Dashboard({ user, projects, tasks }) {
  // Make user data available to the AI
  useCopilotReadable({
    description: "Current user information",
    value: user
  }, [user]);

  // Make projects data available to the AI
  useCopilotReadable({
    description: "User's projects",
    value: projects
  }, [projects]);

  // Make tasks data available to the AI
  useCopilotReadable({
    description: "User's tasks",
    value: tasks
  }, [tasks]);

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <div className="dashboard-content">
        {/* Dashboard UI */}
      </div>
    </div>
  );
}
```

### Best Practices for useCopilotReadable

1. **Descriptive Context**: Provide clear descriptions for each piece of data
2. **Dependency Array**: Use the dependency array to update the context when data changes
3. **Data Structure**: Keep data structures simple and avoid circular references
4. **Privacy**: Be mindful of sensitive data and only provide what's necessary
5. **Performance**: Avoid providing extremely large datasets that could impact performance

## Backend Data Integration

You can also provide data to the AI from your backend using the CopilotKit runtime.

```typescript
// pages/api/copilotkit.ts
import { CopilotRuntime } from "@copilotkit/runtime";

const runtime = new CopilotRuntime({
  // Define backend actions to fetch data
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
      }
    ];
  },
  
  // Provide context data to the AI
  context: async ({ properties, url }) => {
    // Get user ID from properties
    const userId = properties?.userId;
    
    if (!userId) {
      return {};
    }
    
    // Fetch user data and related information
    const [userData, userStats, recentActivity] = await Promise.all([
      db.users.findById(userId),
      db.stats.findByUserId(userId),
      db.activity.findRecentByUserId(userId, { limit: 10 })
    ]);
    
    return {
      user: userData,
      stats: userStats,
      recentActivity
    };
  }
});

export default runtime.createHandler();
```

## Document Integration

CopilotKit can integrate with your application's documents and content to provide more context to the AI.

```jsx
import { useCopilotReadable } from "@copilotkit/react-core";

function DocumentViewer({ document }) {
  // Make the document content available to the AI
  useCopilotReadable({
    description: `Current document: ${document.title}`,
    value: {
      title: document.title,
      content: document.content,
      metadata: document.metadata
    }
  }, [document]);

  return (
    <div className="document-viewer">
      <h1>{document.title}</h1>
      <div className="document-content">
        {document.content}
      </div>
    </div>
  );
}
```

## Vector Database Integration

For more advanced document retrieval, you can integrate CopilotKit with vector databases like Pinecone, Weaviate, or Supabase Vector.

```typescript
// pages/api/copilotkit.ts
import { CopilotRuntime } from "@copilotkit/runtime";
import { PineconeClient } from "@pinecone-database/pinecone";

// Initialize Pinecone client
const pinecone = new PineconeClient();
await pinecone.init({
  apiKey: process.env.PINECONE_API_KEY,
  environment: process.env.PINECONE_ENVIRONMENT
});
const index = pinecone.Index(process.env.PINECONE_INDEX);

const runtime = new CopilotRuntime({
  actions: ({ properties, url }) => {
    return [
      {
        name: "searchDocuments",
        description: "Searches for documents related to a query",
        parameters: [
          {
            name: "query",
            type: "string",
            description: "The search query",
            required: true
          },
          {
            name: "limit",
            type: "number",
            description: "Maximum number of results to return",
            required: false
          }
        ],
        handler: async ({ query, limit = 5 }) => {
          // Convert query to embedding using an embedding model
          const embedding = await getEmbedding(query);
          
          // Search Pinecone index
          const results = await index.query({
            vector: embedding,
            topK: limit,
            includeMetadata: true
          });
          
          // Return formatted results
          return results.matches.map(match => ({
            id: match.id,
            score: match.score,
            ...match.metadata
          }));
        }
      }
    ];
  }
});

export default runtime.createHandler();
```

## State Machine Pattern for Complex Interactions

For complex interactions that involve multiple steps and different data contexts, you can use the state machine pattern.

```jsx
import { useState } from "react";
import { CopilotKit, useCopilotReadable } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

function StateMachineChat() {
  // Track the current stage and user data
  const [stage, setStage] = useState("initial");
  const [userData, setUserData] = useState({});
  
  // Make the current stage available to the AI
  useCopilotReadable({
    description: "Current interaction stage",
    value: stage
  }, [stage]);
  
  // Make user data available to the AI
  useCopilotReadable({
    description: "User data collected so far",
    value: userData
  }, [userData]);
  
  // Define stage-specific hooks
  useInitialStage(stage, setStage, setUserData);
  useDataCollectionStage(stage, setStage, setUserData);
  useRecommendationStage(stage, setStage, userData);
  useConfirmationStage(stage, setStage, userData);
  
  return (
    <CopilotKit>
      <CopilotChat />
    </CopilotKit>
  );
}

// Example of a stage-specific hook
function useInitialStage(stage, setStage, setUserData) {
  useCopilotAction({
    name: "collectBasicInfo",
    description: "Collect basic information from the user",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "User's name",
        required: true
      },
      {
        name: "email",
        type: "string",
        description: "User's email",
        required: true
      }
    ],
    handler: ({ name, email }) => {
      setUserData(prev => ({ ...prev, name, email }));
      setStage("dataCollection");
      return `Thank you, ${name}. Let's continue with more specific questions.`;
    }
  }, [stage === "initial"]);
}
```

## Dynamic Context Based on User Interactions

You can dynamically update the context provided to the AI based on user interactions.

```jsx
import { useState, useEffect } from "react";
import { useCopilotReadable } from "@copilotkit/react-core";

function ProductBrowser({ products, categories }) {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [filteredProducts, setFilteredProducts] = useState(products);
  const [viewedProducts, setViewedProducts] = useState([]);
  
  // Update filtered products when category changes
  useEffect(() => {
    if (selectedCategory) {
      setFilteredProducts(products.filter(p => p.category === selectedCategory));
    } else {
      setFilteredProducts(products);
    }
  }, [selectedCategory, products]);
  
  // Make selected category available to the AI
  useCopilotReadable({
    description: "Currently selected product category",
    value: selectedCategory
  }, [selectedCategory]);
  
  // Make filtered products available to the AI
  useCopilotReadable({
    description: "Products in the current view",
    value: filteredProducts
  }, [filteredProducts]);
  
  // Make viewed products history available to the AI
  useCopilotReadable({
    description: "Products the user has viewed",
    value: viewedProducts
  }, [viewedProducts]);
  
  const handleProductView = (product) => {
    setViewedProducts(prev => [...prev, product]);
  };
  
  return (
    <div className="product-browser">
      <div className="categories">
        {categories.map(category => (
          <button 
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={selectedCategory === category.id ? "active" : ""}
          >
            {category.name}
          </button>
        ))}
      </div>
      <div className="products">
        {filteredProducts.map(product => (
          <div 
            key={product.id} 
            className="product-card"
            onClick={() => handleProductView(product)}
          >
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p>${product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Best Practices for Data Integration

1. **Relevant Context**: Only provide data that's relevant to the current user interaction
2. **Data Freshness**: Keep context data up-to-date by using the dependency array with `useCopilotReadable`
3. **Progressive Disclosure**: Start with basic context and add more as the interaction progresses
4. **Data Transformation**: Transform complex data structures into simpler formats for the AI
5. **Error Handling**: Handle cases where data might be unavailable or incomplete
6. **Performance**: Be mindful of the amount of data you're providing to avoid performance issues
7. **Privacy**: Never expose sensitive user data that shouldn't be accessible to the AI
8. **Documentation**: Document the structure and purpose of each piece of context data
