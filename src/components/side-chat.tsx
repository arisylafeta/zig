import { CopilotSidebar, CopilotKitCSSProperties } from '@copilotkit/react-ui'
import React from 'react'

const SideChat = ({themeColor}: {themeColor: string}) => {
  return (
    <div style={{ "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties}>
        <CopilotSidebar
        clickOutsideToClose={true}
        defaultOpen={true}
        labels={{
          title: "Popup Assistant",
          initial: "👋 Hi, there! You're chatting with an agent. This agent comes with a few tools to get you started.\n\nFor example you can try:\n- **Frontend Tools**: \"Set the theme to orange\"\n- **Shared State**: \"Write a proverb about AI\"\n- **Generative UI**: \"Get the weather in SF\"\n\nAs you interact with the agent, you'll see the UI update in real-time to reflect the agent's **state**, **tool calls**, and **progress**."
        }}
      />
    </div>
  )
}

export default SideChat