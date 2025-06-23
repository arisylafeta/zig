"use client";

/**
 * @file SearchPanel.tsx
 * @description Search panel component for finding and displaying search results.
 * This component provides a search interface that can be used to find information
 * and display results in a structured format. It can be controlled by both user
 * input and CopilotKit actions.
 * 
 * @component SearchPanel - Main component that renders the search interface
 * @function handleSearch - Processes search queries and fetches results
 * @function renderResults - Renders search results in a structured format
 */

import React, { useState } from 'react';
import { PanelProps } from '@/types/mosaic';

/**
 * Interface for search result items
 */
interface SearchResult {
  id: string;
  title: string;
  description: string;
  type: 'company' | 'person' | 'technology' | 'other';
  relevance: number;
}

/**
 * Search panel component for finding and displaying search results
 * 
 * @param id - ID of the panel
 * @param path - Path to the panel in the Mosaic tree
 */
export function SearchPanel(_props: PanelProps) {
  // State for the search query
  const [query, setQuery] = useState('');
  
  // State for search results
  const [results, setResults] = useState<SearchResult[]>([]);
  
  // State for loading indicator
  const [isLoading, setIsLoading] = useState(false);
  
  // State for selected result
  const [selectedResult, setSelectedResult] = useState<string | null>(null);

  /**
   * Handle search query submission
   * 
   * @param e - Form submit event
   */
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    setIsLoading(true);
    
    try {
      // Simulate API call with timeout
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock search results
      const mockResults: SearchResult[] = [
        {
          id: '1',
          title: 'Acme Corporation',
          description: 'Global technology company specializing in AI solutions',
          type: 'company',
          relevance: 0.95,
        },
        {
          id: '2',
          title: 'TechGiant Inc.',
          description: 'Leading provider of cloud infrastructure services',
          type: 'company',
          relevance: 0.87,
        },
        {
          id: '3',
          title: 'Neural Networks',
          description: 'Machine learning technology used in pattern recognition',
          type: 'technology',
          relevance: 0.82,
        },
        {
          id: '4',
          title: 'Jane Smith',
          description: 'CTO at Acme Corporation with expertise in AI',
          type: 'person',
          relevance: 0.78,
        },
        {
          id: '5',
          title: 'Quantum Computing',
          description: 'Next-generation computing technology',
          type: 'technology',
          relevance: 0.75,
        },
      ];
      
      setResults(mockResults);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Get the appropriate icon for a result type
   * 
   * @param type - Type of search result
   * @returns Icon element for the type
   */
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'company':
        return <span className="text-blue-500">🏢</span>;
      case 'person':
        return <span className="text-green-500">👤</span>;
      case 'technology':
        return <span className="text-purple-500">⚙️</span>;
      default:
        return <span className="text-gray-500">📄</span>;
    }
  };

  /**
   * Handle clicking on a search result
   * 
   * @param id - ID of the selected result
   */
  const handleResultClick = (id: string) => {
    setSelectedResult(id === selectedResult ? null : id);
    
    // Here you could trigger an action to show details in another panel
    // For example, using CopilotKit actions or direct panel communication
  };

  return (
    <div className="flex flex-col h-full">
      {/* Search form */}
      <div className="p-4 border-b">
        <form onSubmit={handleSearch} className="flex space-x-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search..."
            className="flex-1 p-2 border rounded-md"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md disabled:bg-blue-300"
          >
            {isLoading ? 'Searching...' : 'Search'}
          </button>
        </form>
      </div>
      
      {/* Results area */}
      <div className="flex-1 overflow-y-auto p-4">
        {results.length > 0 ? (
          <div className="space-y-3">
            {results.map((result) => (
              <div
                key={result.id}
                className={`p-3 border rounded-md cursor-pointer transition-colors ${
                  selectedResult === result.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => handleResultClick(result.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getTypeIcon(result.type)}
                    <span className="font-medium">{result.title}</span>
                  </div>
                  <span className="text-sm text-gray-500">
                    {Math.round(result.relevance * 100)}% match
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-1">{result.description}</p>
                
                {/* Tags for result type */}
                <div className="mt-2">
                  <span className="inline-block px-2 py-1 text-xs rounded-full bg-gray-200 text-gray-700">
                    {result.type}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            {isLoading ? (
              <div className="flex justify-center items-center space-x-2">
                <div className="w-4 h-4 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-4 h-4 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-4 h-4 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            ) : query ? (
              <p>No results found for &quot;{query}&quot;</p>
            ) : (
              <p>Enter a search query to find results</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
