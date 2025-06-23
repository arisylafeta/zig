/**
 * @file page.tsx
 * @description Main page component that renders the MosaicApp.
 * This component serves as the entry point for the application and
 * renders the MosaicApp component which integrates React Mosaic with CopilotKit.
 */

import { MosaicApp } from "@/components/layout/MosaicApp";

export default function Home() {
  return (
    <div className="h-screen w-full overflow-hidden">
      <MosaicApp />
    </div>
  );
}
