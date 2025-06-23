"use client";

/**
 * @file ChatPanel.tsx
 * @description AI-driven chat panel component that integrates with CopilotKit.
 * This component provides a user interface for interacting with the AI assistant,
 * displaying messages, and sending user queries. It leverages CopilotKit's
 * headless UI approach for full control over the chat interface while using
 * CopilotKit's state management and message handling capabilities.
 * 
 * @component ChatPanel - Main component that renders the chat interface
 * @function handleSendMessage - Processes user input and sends messages to the AI
 * @function handleKeyDown - Handles keyboard events for the input field
 */

import React, { useRef, useState, useEffect, useMemo } from 'react';
import { useCopilotChat } from '@copilotkit/react-core';
import { PanelProps } from '@/types/mosaic';

/**
 * Chat panel component for interacting with the AI assistant
 * 
 * @param id - ID of the panel
 * @param path - Path to the panel in the Mosaic tree
 */
export function ChatPanel(_props: PanelProps) {
  // State for the input field
  const [input, setInput] = useState('');
  
  // Reference to the messages container for auto-scrolling
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Get chat state and methods from CopilotKit
  const chat = useCopilotChat();
  
  // TODO: Update these once proper CopilotKit typings are available
  // For now, we're using type assertions to work around TypeScript errors
  const messages = useMemo(() => {
    return (chat as any).messages || [];
  }, [chat]);
  const sendMessage = (chat as any).sendMessage || (() => {});
  const isLoading = chat.isLoading || false;

  /**
   * Automatically scroll to the bottom when new messages are added
   */
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  /**
   * Handle sending a message to the AI
   */
  const handleSendMessage = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  /**
   * Handle keyboard events for the input field
   * 
   * @param e - Keyboard event
   */
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Send message on Enter (without Shift for new lines)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message: {role: string, content: string}, index: number) => (
          <div
            key={index}
            className={`p-3 rounded-lg ${
              message.role === 'user'
                ? 'bg-blue-100 ml-8'
                : 'bg-gray-100 mr-8'
            }`}
          >
            <div className="font-semibold mb-1">
              {message.role === 'user' ? 'You' : 'AI'}
            </div>
            <div className="whitespace-pre-wrap">{message.content}</div>
          </div>
        ))}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="bg-gray-100 p-3 rounded-lg mr-8">
            <div className="font-semibold mb-1">AI</div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        )}
        
        {/* Auto-scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input area */}
      <div className="border-t p-4">
        <div className="flex items-start space-x-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask the AI..."
            className="flex-1 p-2 border rounded-md resize-none"
            rows={3}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md disabled:bg-blue-300"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
