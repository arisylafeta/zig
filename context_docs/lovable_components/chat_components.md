# Chat Component Architecture

This document provides a detailed analysis of the chat components in the Ebisu Relationship Orchestrator, which will need to be integrated with CopilotKit in the Zig project.

## Core Components

The chat system consists of several key components:

1. **ChatPanel**: Main container for the chat interface
2. **ChatThread**: Displays the conversation history
3. **ChatBubble**: Renders individual chat messages
4. **ChatInput**: Handles user input and message submission
5. **ChatTypes**: TypeScript types for chat functionality

Let's examine each component in detail.

## ChatPanel.tsx

The ChatPanel is the main container component that orchestrates the chat interface. It manages the chat state and handles sending/receiving messages.

```tsx
import { useState, useEffect } from 'react';
import { ChatThread } from './ChatThread';
import { ChatInput } from './ChatInput';
import { Message, ChatSession } from './types';
import { useChatService } from '../../hooks/useChatService';

interface ChatPanelProps {
  sessionId?: string;
  contextData?: Record<string, any>;
  onNewInsight?: (insight: any) => void;
}

export function ChatPanel({ sessionId, contextData, onNewInsight }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [session, setSession] = useState<ChatSession | null>(null);
  const chatService = useChatService();
  
  // Initialize or load existing chat session
  useEffect(() => {
    const initChat = async () => {
      if (sessionId) {
        // Load existing session
        const existingSession = await chatService.getSession(sessionId);
        if (existingSession) {
          setSession(existingSession);
          setMessages(existingSession.messages || []);
        }
      } else {
        // Create new session
        const newSession = await chatService.createSession({
          contextData,
          type: 'sales-assistant'
        });
        setSession(newSession);
      }
    };
    
    initChat();
  }, [sessionId, contextData]);
  
  // Handle sending a new message
  const handleSendMessage = async (content: string) => {
    if (!session) return;
    
    // Add user message to UI immediately
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // Send message to backend
      const response = await chatService.sendMessage(session.id, content, contextData);
      
      // Add assistant response to UI
      const assistantMessage: Message = {
        id: response.messageId || `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.content,
        timestamp: new Date(),
        metadata: response.metadata
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
      // If there are insights, pass them to the parent component
      if (response.insights && onNewInsight) {
        onNewInsight(response.insights);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'system',
        content: 'Sorry, there was an error processing your message. Please try again.',
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex flex-col h-full bg-background">
      <div className="flex-none border-b p-4">
        <h2 className="text-lg font-semibold">Sales Assistant</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        <ChatThread messages={messages} />
      </div>
      
      <div className="flex-none border-t p-4">
        <ChatInput 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading} 
          placeholder="Ask me anything about your sales relationships..."
        />
      </div>
    </div>
  );
}
```

## ChatThread.tsx

The ChatThread component renders the conversation history as a scrollable list of messages.

```tsx
import { useRef, useEffect } from 'react';
import { ChatBubble } from './ChatBubble';
import { Message } from './types';

interface ChatThreadProps {
  messages: Message[];
}

export function ChatThread({ messages }: ChatThreadProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Group consecutive messages from the same sender
  const groupedMessages = messages.reduce((groups: Message[][], message, index) => {
    const prevMessage = messages[index - 1];
    
    // Start a new group if:
    // - This is the first message
    // - Previous message was from a different role
    // - Previous message was more than 2 minutes ago
    const shouldStartNewGroup = 
      index === 0 || 
      prevMessage.role !== message.role ||
      (message.timestamp.getTime() - prevMessage.timestamp.getTime() > 2 * 60 * 1000);
    
    if (shouldStartNewGroup) {
      groups.push([message]);
    } else {
      groups[groups.length - 1].push(message);
    }
    
    return groups;
  }, []);
  
  return (
    <div className="space-y-6">
      {groupedMessages.map((group, groupIndex) => (
        <div key={`group-${groupIndex}`} className="space-y-2">
          {group.map((message, messageIndex) => (
            <ChatBubble 
              key={message.id} 
              message={message} 
              isFirstInGroup={messageIndex === 0}
              isLastInGroup={messageIndex === group.length - 1}
            />
          ))}
        </div>
      ))}
      
      {/* Empty div for auto-scrolling */}
      <div ref={messagesEndRef} />
    </div>
  );
}
```

## ChatBubble.tsx

The ChatBubble component renders individual chat messages with appropriate styling based on the sender.

```tsx
import { useState } from 'react';
import { Message } from './types';
import { Avatar } from '../ui/avatar';
import { Button } from '../ui/button';
import { formatDistanceToNow } from 'date-fns';
import { Copy, Check } from 'lucide-react';

interface ChatBubbleProps {
  message: Message;
  isFirstInGroup: boolean;
  isLastInGroup: boolean;
}

export function ChatBubble({ message, isFirstInGroup, isLastInGroup }: ChatBubbleProps) {
  const [copied, setCopied] = useState(false);
  
  const isUser = message.role === 'user';
  const isAssistant = message.role === 'assistant';
  const isSystem = message.role === 'system';
  
  // Copy message content to clipboard
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  // Format timestamp as relative time (e.g., "5 minutes ago")
  const formattedTime = formatDistanceToNow(message.timestamp, { addSuffix: true });
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`
        flex max-w-[80%] 
        ${isUser ? 'flex-row-reverse' : 'flex-row'}
      `}>
        {/* Avatar - only show for first message in group */}
        {isFirstInGroup && (
          <div className="flex-shrink-0 mt-1">
            {isUser ? (
              <Avatar className="h-8 w-8 bg-primary text-primary-foreground">
                <span>U</span>
              </Avatar>
            ) : isAssistant ? (
              <Avatar className="h-8 w-8 bg-secondary text-secondary-foreground">
                <span>AI</span>
              </Avatar>
            ) : (
              <Avatar className="h-8 w-8 bg-muted text-muted-foreground">
                <span>S</span>
              </Avatar>
            )}
          </div>
        )}
        
        {/* Message content */}
        <div className={`
          px-4 py-2 rounded-lg mx-2
          ${isUser ? 'bg-primary text-primary-foreground' : ''}
          ${isAssistant ? 'bg-secondary text-secondary-foreground' : ''}
          ${isSystem ? 'bg-muted text-muted-foreground' : ''}
          ${message.isError ? 'bg-destructive text-destructive-foreground' : ''}
        `}>
          <div className="prose prose-sm dark:prose-invert">
            {message.content}
          </div>
          
          {/* Message metadata */}
          <div className={`
            text-xs mt-1 flex items-center
            ${isUser ? 'justify-end' : 'justify-start'}
          `}>
            <span className="opacity-70">{formattedTime}</span>
            
            {/* Copy button - only for assistant messages */}
            {isAssistant && (
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-6 w-6 ml-2 opacity-70 hover:opacity-100"
                onClick={handleCopy}
              >
                {copied ? <Check size={14} /> : <Copy size={14} />}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

## ChatInput.tsx

The ChatInput component handles user input and message submission.

```tsx
import { useState, useRef, KeyboardEvent } from 'react';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export function ChatInput({ onSendMessage, isLoading = false, placeholder = 'Type a message...' }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  const handleSubmit = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !isLoading) {
      onSendMessage(trimmedMessage);
      setMessage('');
      
      // Focus back on textarea after sending
      setTimeout(() => {
        textareaRef.current?.focus();
      }, 0);
    }
  };
  
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };
  
  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };
  
  return (
    <div className="flex items-end gap-2">
      <Textarea
        ref={textareaRef}
        value={message}
        onChange={handleTextareaChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="min-h-[40px] max-h-[200px] resize-none"
        disabled={isLoading}
      />
      
      <Button 
        onClick={handleSubmit} 
        disabled={!message.trim() || isLoading}
        className="flex-shrink-0"
      >
        {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
      </Button>
    </div>
  );
}
```

## types.ts

TypeScript types for the chat functionality.

```tsx
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
  isError?: boolean;
}

export interface ChatSession {
  id: string;
  type: 'sales-assistant' | 'research' | 'general';
  messages: Message[];
  contextData?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatResponse {
  messageId: string;
  content: string;
  metadata?: Record<string, any>;
  insights?: any;
}
```

## useChatService.ts

A custom hook for interacting with the chat API.

```tsx
import { useCallback } from 'react';
import { ChatSession, ChatResponse } from '../components/chat/types';

export function useChatService() {
  // Create a new chat session
  const createSession = useCallback(async (options: {
    contextData?: Record<string, any>;
    type: 'sales-assistant' | 'research' | 'general';
  }): Promise<ChatSession> => {
    try {
      const response = await fetch('/api/chat/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(options),
      });
      
      if (!response.ok) {
        throw new Error('Failed to create chat session');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error creating chat session:', error);
      throw error;
    }
  }, []);
  
  // Get an existing chat session
  const getSession = useCallback(async (sessionId: string): Promise<ChatSession | null> => {
    try {
      const response = await fetch(`/api/chat/sessions/${sessionId}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        throw new Error('Failed to get chat session');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error getting chat session:', error);
      throw error;
    }
  }, []);
  
  // Send a message in a chat session
  const sendMessage = useCallback(async (
    sessionId: string, 
    content: string, 
    contextData?: Record<string, any>
  ): Promise<ChatResponse> => {
    try {
      const response = await fetch(`/api/chat/sessions/${sessionId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          contextData,
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to send message');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }, []);
  
  return {
    createSession,
    getSession,
    sendMessage,
  };
}
```

## Integration with CopilotKit

When integrating these chat components with CopilotKit, we'll need to replace the custom chat service with CopilotKit's chat functionality. Here's how we can adapt the components:

### ChatPanel with CopilotKit

```tsx
import { useState } from 'react';
import { ChatThread } from './ChatThread';
import { ChatInput } from './ChatInput';
import { Message } from './types';
import { useCopilotChat } from '@copilotkit/react-core';

interface ChatPanelProps {
  contextData?: Record<string, any>;
  onNewInsight?: (insight: any) => void;
}

export function ChatPanel({ contextData, onNewInsight }: ChatPanelProps) {
  const [isLoading, setIsLoading] = useState(false);
  
  // Use CopilotKit's chat hook
  const { messages, sendMessage } = useCopilotChat({
    id: "sales-assistant",
    onMessageReceive: (message) => {
      // Extract insights if available
      const insights = message.metadata?.insights;
      if (insights && onNewInsight) {
        onNewInsight(insights);
      }
    }
  });
  
  // Convert CopilotKit messages to our format
  const formattedMessages: Message[] = messages.map(msg => ({
    id: msg.id,
    role: msg.role as 'user' | 'assistant' | 'system',
    content: msg.content,
    timestamp: new Date(msg.createdAt),
    metadata: msg.metadata
  }));
  
  // Handle sending a new message
  const handleSendMessage = async (content: string) => {
    setIsLoading(true);
    
    try {
      // Send message using CopilotKit
      await sendMessage({
        content,
        context: contextData
      });
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="flex flex-col h-full bg-background">
      <div className="flex-none border-b p-4">
        <h2 className="text-lg font-semibold">Sales Assistant</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        <ChatThread messages={formattedMessages} />
      </div>
      
      <div className="flex-none border-t p-4">
        <ChatInput 
          onSendMessage={handleSendMessage} 
          isLoading={isLoading} 
          placeholder="Ask me anything about your sales relationships..."
        />
      </div>
    </div>
  );
}
```

## Migration Strategy

When migrating these chat components to the Zig project:

1. **Create the core chat components** in the Zig project
2. **Integrate with CopilotKit** for chat functionality
3. **Adapt to Next.js App Router** patterns
4. **Ensure responsive design** works across devices
5. **Implement chat persistence** using CopilotKit's storage options

These chat components will form the foundation of the AI interaction interface for the Ebisu application in the Zig project.
