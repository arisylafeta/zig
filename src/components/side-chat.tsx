import { CopilotSidebar, CopilotKitCSSProperties } from '@copilotkit/react-ui'
import React from 'react'

const SideChat = ({themeColor}: {themeColor: string}) => {
  return (
    <div 
      className="fixed top-3 right-3 bottom-3 w-[400px] bg-[#1C1C1F] text-white rounded-xl shadow-2xl flex flex-col overflow-hidden"
      style={{ "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties}>
        <CopilotSidebar
        clickOutsideToClose={true}
        defaultOpen={true}
        labels={{
          title: "Ebisu AI",
          initial: "👋 Ready to supercharge your sales process with Find & research prospects? What would you like to work on today?"
        }}
      />
    </div>
  )
}

export default SideChat