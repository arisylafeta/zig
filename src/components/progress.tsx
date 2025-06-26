interface ProgressLog {
  id: string;
  message: string;
  timestamp: Date;
  type: 'info' | 'success' | 'error' | 'progress';
}

interface ProgressProps {
  logs: ProgressLog[];
}

export function Progress({ logs }: ProgressProps) {
  if (!logs || logs.length === 0) {
    return null;
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 my-4">
      <h3 className="text-sm font-semibold text-blue-900 mb-2">🤖 Agent Progress</h3>
      <div className="space-y-2">
        {logs.map((log) => (
          <div
            key={log.id}
            className={`text-sm flex items-center gap-2 ${
              log.type === 'success' ? 'text-green-700' :
              log.type === 'error' ? 'text-red-700' :
              log.type === 'progress' ? 'text-blue-700' :
              'text-gray-700'
            }`}
          >
            <span className="text-xs text-gray-500">
              {log.timestamp.toLocaleTimeString()}
            </span>
            <span className="flex-1">{log.message}</span>
            {log.type === 'progress' && (
              <div className="animate-spin h-3 w-3 border border-blue-600 border-t-transparent rounded-full"></div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
} 