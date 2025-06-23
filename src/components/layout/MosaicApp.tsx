/**
 * @file MosaicApp.tsx
 * @description Main application component that integrates React Mosaic with CopilotKit.
 * This component brings together the MosaicProvider, MosaicLayout, panel registry,
 * and CopilotKit actions to create a complete tiling window manager with AI-driven
 * panel management. It serves as the entry point for the Mosaic integration.
 * 
 * @component MosaicApp - Main component that integrates all Mosaic pieces
 * @function initializePanelRegistry - Sets up the initial panel registry
 */

'use client'

import React, { useEffect } from 'react';
import { MosaicProvider } from './MosaicProvider';
import { MosaicLayout } from './MosaicLayout';
import { usePanelRegistry } from '@/hooks/usePanelRegistry';
import { useMosaicActions } from '@/hooks/useMosaicActions';
import { 
  ChatPanel, 
  SearchPanel, 
  DetailsPanel, 
  PeopleSearchPanel,
  CompanySearchPanel,
  ICPSearchPanel,
  PeopleIntelligencePanel,
  CompanyIntelligencePanel 
} from '@/components/panels';
import { PanelConfig } from '@/types/mosaic';

interface MosaicAppProps {
  /** Additional CSS class names */
  className?: string;
}

/**
 * Main application component that integrates React Mosaic with CopilotKit
 * 
 * @param className - Additional CSS class names
 */
export function MosaicApp({ className = '' }: MosaicAppProps) {
  // Initialize panel registry
  const { panels, registerPanels } = usePanelRegistry();
  
  // Register Mosaic actions with CopilotKit
  useMosaicActions();
  
  // Initialize panel registry with available panels
  useEffect(() => {
    const availablePanels: PanelConfig[] = [
      {
        id: 'chat',
        title: 'AI Chat',
        component: ChatPanel,
        defaultSize: 30,
        closable: false,
        draggable: true,
      },
      {
        id: 'search',
        title: 'Search',
        component: SearchPanel,
        defaultSize: 40,
        closable: true,
        draggable: true,
      },
      {
        id: 'details',
        title: 'Details',
        component: DetailsPanel,
        defaultSize: 30,
        closable: true,
        draggable: true,
      },
      // New panel types
      {
        id: 'peopleSearch',
        title: 'People Search',
        component: PeopleSearchPanel,
        defaultSize: 30,
        closable: true,
        draggable: true,
      },
      {
        id: 'companySearch',
        title: 'Company Search',
        component: CompanySearchPanel,
        defaultSize: 30,
        closable: true,
        draggable: true,
      },
      {
        id: 'icpSearch',
        title: 'ICP Search',
        component: ICPSearchPanel,
        defaultSize: 30,
        closable: true,
        draggable: true,
      },
      {
        id: 'peopleIntelligence',
        title: 'People Intelligence',
        component: PeopleIntelligencePanel,
        defaultSize: 40,
        closable: true,
        draggable: true,
      },
      {
        id: 'companyIntelligence',
        title: 'Company Intelligence',
        component: CompanyIntelligencePanel,
        defaultSize: 40,
        closable: true,
        draggable: true,
      },
    ];
    
    registerPanels(availablePanels);
  }, [registerPanels]);
  
  return (
    <MosaicProvider>
      <div className={`mosaic-app ${className}`} style={{ height: '100vh', width: '100%' }}>
        <MosaicLayout panelRegistry={panels} />
      </div>
    </MosaicProvider>
  );
}
