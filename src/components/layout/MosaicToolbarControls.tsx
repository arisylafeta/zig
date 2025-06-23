/**
 * Custom toolbar controls for React Mosaic windows
 * Adds proper key props to fix React warnings
 */
import React from 'react';
import {
  ExpandButton,
  RemoveButton,
  ReplaceButton,
  SplitButton,
} from 'react-mosaic-component';

interface ToolbarControlsProps {
  closable?: boolean;
}

/**
 * Custom toolbar controls component that ensures each control has a unique key
 * 
 * @param props - Component props
 * @returns Toolbar controls with proper key props
 */
export const MosaicToolbarControls: React.FC<ToolbarControlsProps> = ({ 
  closable = true 
}) => {
  return (
    <>
      {closable && <SplitButton key="split-button" />}
      {closable && <ReplaceButton key="replace-button" />}
      <ExpandButton key="expand-button" />
      {closable && <RemoveButton key="remove-button" />}
    </>
  );
};

export default MosaicToolbarControls;
