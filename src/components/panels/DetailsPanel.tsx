"use client";

/**
 * @file DetailsPanel.tsx
 * @description Details panel component for displaying detailed information about selected items.
 * This component shows comprehensive information about an entity (company, person, technology)
 * selected from another panel such as the SearchPanel. It provides a rich, structured view
 * of the entity's attributes, relationships, and relevant data.
 * 
 * @component DetailsPanel - Main component that renders detailed information
 * @function renderCompanyDetails - Renders company-specific details
 * @function renderPersonDetails - Renders person-specific details
 * @function renderTechnologyDetails - Renders technology-specific details
 * 
 TODO:update based on the data from apollo
 */

import React, { useState, useEffect } from 'react';
import { PanelProps } from '@/types/mosaic';

/**
 * Interface for entity details
 */
interface EntityDetails {
  id: string;
  name: string;
  type: 'company' | 'person' | 'technology' | 'other';
  description: string;
  attributes: Record<string, string | number | boolean>;
  relationships: Array<{
    type: string;
    entity: {
      id: string;
      name: string;
      type: string;
    };
  }>;
}

/**
 * Details panel component for displaying comprehensive information
 * 
 * @param id - ID of the panel
 * @param path - Path to the panel in the Mosaic tree
 */
export function DetailsPanel(_props: PanelProps) {
  // State for the entity being displayed
  const [entity, setEntity] = useState<EntityDetails | null>(null);
  
  // State for loading indicator
  const [isLoading, setIsLoading] = useState(false);

  // Mock function to fetch entity details
  // In a real implementation, this would be connected to your data source
  const fetchEntityDetails = async (_entityId: string) => {
    setIsLoading(true);
    
    try {
      // Simulate API call with timeout
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Mock entity details
      const mockEntity: EntityDetails = {
        id: '1',
        name: 'Acme Corporation',
        type: 'company',
        description: 'Global technology company specializing in AI solutions and cloud infrastructure. Founded in 2010, Acme has grown to become a leader in enterprise AI applications.',
        attributes: {
          founded: '2010',
          headquarters: 'San Francisco, CA',
          employees: 5200,
          revenue: '$1.2B',
          industry: 'Technology',
          publiclyTraded: true,
          stockSymbol: 'ACME',
        },
        relationships: [
          {
            type: 'CEO',
            entity: {
              id: '101',
              name: 'John Doe',
              type: 'person',
            },
          },
          {
            type: 'CTO',
            entity: {
              id: '102',
              name: 'Jane Smith',
              type: 'person',
            },
          },
          {
            type: 'Subsidiary',
            entity: {
              id: '201',
              name: 'Acme Cloud Services',
              type: 'company',
            },
          },
          {
            type: 'Technology',
            entity: {
              id: '301',
              name: 'Neural Networks',
              type: 'technology',
            },
          },
        ],
      };
      
      setEntity(mockEntity);
    } catch (error) {
      console.error('Error fetching entity details:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch details when the component mounts
  // In a real implementation, this would be triggered by selection in another panel
  useEffect(() => {
    fetchEntityDetails('1');
  }, []);

  /**
   * Render company-specific details
   * 
   * @param company - Company entity details
   * @returns JSX for company details
   */
  const renderCompanyDetails = (company: EntityDetails) => {
    const { attributes } = company;
    
    return (
      <>
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Company Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-2 bg-gray-50 rounded">
              <span className="text-sm text-gray-500">Founded</span>
              <p>{attributes.founded}</p>
            </div>
            <div className="p-2 bg-gray-50 rounded">
              <span className="text-sm text-gray-500">Headquarters</span>
              <p>{attributes.headquarters}</p>
            </div>
            <div className="p-2 bg-gray-50 rounded">
              <span className="text-sm text-gray-500">Employees</span>
              <p>{attributes.employees.toLocaleString()}</p>
            </div>
            <div className="p-2 bg-gray-50 rounded">
              <span className="text-sm text-gray-500">Revenue</span>
              <p>{attributes.revenue}</p>
            </div>
            <div className="p-2 bg-gray-50 rounded">
              <span className="text-sm text-gray-500">Industry</span>
              <p>{attributes.industry}</p>
            </div>
            {attributes.publiclyTraded && (
              <div className="p-2 bg-gray-50 rounded">
                <span className="text-sm text-gray-500">Stock Symbol</span>
                <p>{attributes.stockSymbol}</p>
              </div>
            )}
          </div>
        </div>
        
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Key People</h3>
          <div className="space-y-2">
            {company.relationships
              .filter(rel => rel.entity.type === 'person')
              .map((rel, index) => (
                <div key={index} className="flex justify-between p-2 bg-gray-50 rounded">
                  <span>{rel.entity.name}</span>
                  <span className="text-gray-500">{rel.type}</span>
                </div>
              ))}
          </div>
        </div>
        
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Technologies</h3>
          <div className="flex flex-wrap gap-2">
            {company.relationships
              .filter(rel => rel.entity.type === 'technology')
              .map((rel, index) => (
                <span 
                  key={index} 
                  className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm"
                >
                  {rel.entity.name}
                </span>
              ))}
          </div>
        </div>
      </>
    );
  };

  /**
   * Render person-specific details
   * 
   * @param person - Person entity details
   * @returns JSX for person details
   */
  const renderPersonDetails = (_person: EntityDetails) => {
    // Implementation for person details
    return (
      <div>
        <p>Person details would be displayed here</p>
      </div>
    );
  };

  /**
   * Render technology-specific details
   * 
   * @param technology - Technology entity details
   * @returns JSX for technology details
   */
  const renderTechnologyDetails = (_technology: EntityDetails) => {
    // Implementation for technology details
    return (
      <div>
        <p>Technology details would be displayed here</p>
      </div>
    );
  };

  /**
   * Render the appropriate details based on entity type
   * 
   * @param entity - Entity details
   * @returns JSX for entity details
   */
  const renderEntityDetails = (entity: EntityDetails) => {
    switch (entity.type) {
      case 'company':
        return renderCompanyDetails(entity);
      case 'person':
        return renderPersonDetails(entity);
      case 'technology':
        return renderTechnologyDetails(entity);
      default:
        return <p>Details not available for this entity type</p>;
    }
  };

  return (
    <div className="flex flex-col h-full overflow-y-auto p-6">
      {isLoading ? (
        <div className="flex justify-center items-center h-full">
          <div className="flex space-x-2">
            <div className="w-4 h-4 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-4 h-4 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-4 h-4 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      ) : entity ? (
        <>
          <div className="mb-6">
            <h2 className="text-2xl font-bold">{entity.name}</h2>
            <div className="flex items-center mt-1">
              <span className="px-2 py-1 text-xs rounded-full bg-gray-200 text-gray-700">
                {entity.type}
              </span>
            </div>
            <p className="mt-3 text-gray-600">{entity.description}</p>
          </div>
          
          {renderEntityDetails(entity)}
        </>
      ) : (
        <div className="flex justify-center items-center h-full text-gray-500">
          <p>Select an item to view details</p>
        </div>
      )}
    </div>
  );
}
