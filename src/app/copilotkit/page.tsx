"use client";

import { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/components/table";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { Progress } from "@/components/progress";

type Person = {
  first_name: string;
  last_name: string;
  linkedin_url: string;
  email_status: string;
  email: string;
  title: string;
  organization: string;
  location: string;
};

type ProgressLog = {
  id: string;
  message: string;
  timestamp: string;
  type: 'info' | 'success' | 'error' | 'progress';
};

// AgentState type to match the backend
type AgentState = {
  people: Person[];
  logs: ProgressLog[];
  current_status: string;
};

const columns: ColumnDef<Person>[] = [
  {
    accessorKey: "first_name",
    header: "First Name",
  },
  {
    accessorKey: "last_name", 
    header: "Last Name",
  },
  {
    accessorKey: "title",
    header: "Title",
  },
  {
    accessorKey: "organization",
    header: "Company",
  },
  {
    accessorKey: "email",
    header: "Email",
    cell: ({ row }) => {
      const email = row.getValue("email") as string;
      return (
        <span className={email === "Unlock" ? "text-orange-500 font-medium" : ""}>
          {email}
        </span>
      );
    },
  },
  {
    accessorKey: "location",
    header: "Location",
  },
  {
    accessorKey: "linkedin_url",
    header: "LinkedIn",
    cell: ({ row }) => {
      const url = row.getValue("linkedin_url") as string;
      return url ? (
        <a 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800 underline"
        >
          Profile
        </a>
      ) : (
        <span className="text-gray-400">N/A</span>
      );
    },
  },
];

export default function AIPage() {
  // Connect to the LangGraph agent using useCoAgent
  const { state } = useCoAgent<AgentState>({
    name: "zig", // This should match the agent name in langgraph.json
    initialState: {
      people: [],
      logs: [],
      current_status: "Ready"
    }
  });

  // Render agent state in the chat UI (like in the tutorial)
  useCoAgentStateRender<AgentState>({
    name: "zig",
    render: ({ state }) => {
      if (state.logs?.length > 0) {
        // Convert timestamp strings back to Date objects for the Progress component
        const logsWithDates = state.logs.map(log => ({
          ...log,
          timestamp: new Date(log.timestamp)
        }));
        return <Progress logs={logsWithDates} />;
      }
      return null;
    },
  }, [state]);

  const peopleCount = state.people?.length || 0;
  const currentStatus = state.current_status || "Ready";

  return (
    <div className="flex h-screen">
      <div className="w-1/2 p-8 overflow-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">People Search Results</h1>
          <div className="flex items-center gap-3 mb-3">
            <p className="text-gray-600">
              {peopleCount > 0 
                ? `Showing ${peopleCount} people found` 
                : "No people found yet. Use the chat to search for prospects."
              }
            </p>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${
                currentStatus.includes("progress") || currentStatus.includes("Searching") || currentStatus.includes("Executing") 
                  ? "bg-blue-500 animate-pulse" 
                  : currentStatus.includes("completed") || currentStatus.includes("Ready")
                  ? "bg-green-500"
                  : "bg-gray-400"
              }`}></div>
              <span className="text-sm text-gray-500">{currentStatus}</span>
            </div>
          </div>
        </div>
        <DataTable columns={columns} data={state.people || []} />
      </div>
      <div className="w-1/2">
        <CopilotSidebar
            className="h-full"
            clickOutsideToClose={true}
            defaultOpen={true}
            labels={{
            title: "Ebisu AI",
            initial: "👋 Ready to supercharge your sales process? Try asking me to 'search for software engineers at tech companies in San Francisco' or similar queries to find prospects!"
            }}
        />
      </div>
    </div>
  );
}
