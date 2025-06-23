# Vite to Next.js Migration Guide for Ebisu

## Overview
This guide outlines the process for migrating React components from a Vite project to a Next.js application. While both frameworks use React, there are important differences in project structure, routing, data fetching, and other areas that need to be addressed during migration.

## Project Structure Comparison

### Vite Project Structure (Typical)
```
/src
  /assets
  /components
  /pages
  /hooks
  /utils
  /styles
  main.jsx
  App.jsx
/public
vite.config.js
package.json
```

### Next.js Project Structure
```
/pages
  _app.js
  index.js
  /api
/public
/styles
/components
/hooks
/utils
/lib
next.config.js
package.json
```

## Step-by-Step Migration Process

### 1. Set Up Next.js Project

```bash
# Create a new Next.js project
npx create-next-app@latest ebisu-next
cd ebisu-next

# Install necessary dependencies
npm install @copilotkit/react-core @copilotkit/react-ui @copilotkit/react-textarea
npm install @supabase/supabase-js
```

### 2. Configure Next.js

Create or modify `next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['your-image-domains.com'],
  },
  // Add any other configuration needed
};

module.exports = nextConfig;
```

### 3. Set Up CopilotKit Provider

Modify `pages/_app.js`:

```javascript
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebarUIProvider } from "@copilotkit/react-ui";
import "../styles/globals.css";

function MyApp({ Component, pageProps }) {
  return (
    <CopilotKit 
      apiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY}
    >
      <CopilotSidebarUIProvider>
        <Component {...pageProps} />
      </CopilotSidebarUIProvider>
    </CopilotKit>
  );
}

export default MyApp;
```

### 4. Set Up Supabase Client

Create `lib/supabase.js`:

```javascript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### 5. Component Migration Guidelines

#### a. Basic Component Migration

Vite components can generally be copied directly to Next.js with minimal changes if they don't rely on Vite-specific features.

**Vite Component:**
```jsx
// src/components/ProspectCard.jsx
import React from 'react';
import './ProspectCard.css';

export function ProspectCard({ prospect }) {
  return (
    <div className="prospect-card">
      <h3>{prospect.name}</h3>
      <p>{prospect.company}</p>
    </div>
  );
}
```

**Next.js Component:**
```jsx
// components/ProspectCard.js
import React from 'react';
import styles from '../styles/ProspectCard.module.css';

export function ProspectCard({ prospect }) {
  return (
    <div className={styles.prospectCard}>
      <h3>{prospect.name}</h3>
      <p>{prospect.company}</p>
    </div>
  );
}
```

#### b. CSS Migration

Convert CSS imports to CSS modules or styled-components:

**CSS Module Approach:**
1. Rename `ProspectCard.css` to `ProspectCard.module.css`
2. Update class references to use the imported styles object
3. Convert kebab-case class names to camelCase in the JS code

**Styled Components Approach:**
```jsx
import styled from 'styled-components';

const Card = styled.div`
  padding: 1rem;
  border-radius: 8px;
  background-color: #1e1e1e;
  color: #ffffff;
`;

export function ProspectCard({ prospect }) {
  return (
    <Card>
      <h3>{prospect.name}</h3>
      <p>{prospect.company}</p>
    </Card>
  );
}
```

#### c. Routing Migration

**Vite (React Router):**
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/prospects/:id" element={<ProspectDetail />} />
      </Routes>
    </BrowserRouter>
  );
}
```

**Next.js:**
Create files in the pages directory:
- `pages/index.js` (Home)
- `pages/prospects/[id].js` (ProspectDetail)

```jsx
// pages/prospects/[id].js
import { useRouter } from 'next/router';

export default function ProspectDetail() {
  const router = useRouter();
  const { id } = router.query;
  
  return <div>Prospect ID: {id}</div>;
}
```

#### d. Data Fetching Migration

**Vite (React Query or useEffect):**
```jsx
import { useEffect, useState } from 'react';

function ProspectList() {
  const [prospects, setProspects] = useState([]);
  
  useEffect(() => {
    async function fetchProspects() {
      const res = await fetch('/api/prospects');
      const data = await res.json();
      setProspects(data);
    }
    fetchProspects();
  }, []);
  
  return (/* render prospects */);
}
```

**Next.js (getServerSideProps):**
```jsx
// pages/prospects/index.js
export default function ProspectList({ prospects }) {
  return (/* render prospects */);
}

export async function getServerSideProps() {
  // This runs on the server
  const res = await fetch('http://your-api-url/prospects');
  const prospects = await res.json();
  
  return {
    props: { prospects },
  };
}
```

**Next.js (SWR for client-side data fetching):**
```jsx
import useSWR from 'swr';

const fetcher = (...args) => fetch(...args).then(res => res.json());

function ProspectList() {
  const { data: prospects, error } = useSWR('/api/prospects', fetcher);
  
  if (error) return <div>Failed to load</div>;
  if (!prospects) return <div>Loading...</div>;
  
  return (/* render prospects */);
}
```

### 6. API Routes Migration

In Next.js, create API routes in the `pages/api` directory:

```jsx
// pages/api/prospects.js
export default async function handler(req, res) {
  const { method } = req;
  
  switch (method) {
    case 'GET':
      // Get data from your database
      res.status(200).json({ prospects: [] });
      break;
    case 'POST':
      // Create new prospect
      res.status(201).json({ message: 'Prospect created' });
      break;
    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${method} Not Allowed`);
  }
}
```

### 7. Environment Variables

**Vite:**
```
VITE_API_URL=https://api.example.com
```

**Next.js:**
```
NEXT_PUBLIC_API_URL=https://api.example.com
```

Note: In Next.js, only variables prefixed with `NEXT_PUBLIC_` are accessible in the browser.

### 8. Image Handling

**Vite:**
```jsx
import logo from '../assets/logo.png';

function Header() {
  return <img src={logo} alt="Logo" />;
}
```

**Next.js:**
```jsx
import Image from 'next/image';

function Header() {
  return <Image src="/images/logo.png" width={100} height={50} alt="Logo" />;
}
```

### 9. Three-Panel Layout Implementation

For Ebisu's VS Code-inspired layout:

```jsx
// components/Layout.js
import { useState } from 'react';
import { CopilotSidebar } from "@copilotkit/react-ui";
import styles from '../styles/Layout.module.css';

export default function Layout({ children }) {
  const [leftPanelWidth, setLeftPanelWidth] = useState(300);
  const [rightPanelWidth, setRightPanelWidth] = useState(300);
  
  return (
    <div className={styles.layout}>
      <div 
        className={styles.leftPanel} 
        style={{ width: `${leftPanelWidth}px` }}
      >
        <CopilotSidebar />
        {/* Resizer component */}
      </div>
      
      <div className={styles.centerPanel}>
        {children}
      </div>
      
      <div 
        className={styles.rightPanel}
        style={{ width: `${rightPanelWidth}px` }}
      >
        {/* Context panel content */}
        {/* Resizer component */}
      </div>
    </div>
  );
}
```

## Common Challenges and Solutions

### 1. Handling Global State

If using Redux or Context API, these can be migrated with minimal changes:

```jsx
// pages/_app.js
import { Provider } from 'react-redux';
import { store } from '../store';
import { CopilotKit } from "@copilotkit/react-core";

function MyApp({ Component, pageProps }) {
  return (
    <Provider store={store}>
      <CopilotKit apiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY}>
        <Component {...pageProps} />
      </CopilotKit>
    </Provider>
  );
}
```

### 2. Authentication

Implement authentication using Next.js middleware and Supabase:

```jsx
// middleware.js
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';

export async function middleware(req) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });
  
  const { data: { session } } = await supabase.auth.getSession();
  
  if (!session && req.nextUrl.pathname !== '/login') {
    return NextResponse.redirect(new URL('/login', req.url));
  }
  
  return res;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico|login).*)'],
};
```

### 3. Build Performance

Next.js has different build optimizations than Vite. To improve build performance:

- Use dynamic imports for large components
- Implement code splitting with `next/dynamic`
- Optimize images with `next/image`

```jsx
import dynamic from 'next/dynamic';

const DynamicComponent = dynamic(() => import('../components/HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false, // If the component uses browser-only features
});
```

## Testing the Migration

1. Start with core components and test them individually
2. Implement the layout structure and test responsiveness
3. Add routing and navigation
4. Integrate with backend APIs
5. Add authentication and authorization
6. Implement CopilotKit features
7. Perform end-to-end testing of complete workflows

## Deployment Considerations

Next.js applications can be deployed to Vercel for optimal performance, or to any platform that supports Node.js applications.

For Vercel deployment:

```bash
npm install -g vercel
vercel login
vercel
```

## Conclusion

While migrating from Vite to Next.js requires some work, the benefits for Ebisu include:

1. Server-side rendering for improved performance and SEO
2. API routes for backend functionality
3. Built-in image optimization
4. Improved routing with file-system based routing
5. Better production optimization

The migration process should be incremental, starting with core components and gradually building up to a complete application.
