
"use client";

import { useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { setApiTokenProvider } from "@/lib/api-client";

export function ApiTokenProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { getToken, isLoaded, isSignedIn } = useAuth();

  useEffect(() => {
    if (!isLoaded) return;

    if (!isSignedIn) {
      setApiTokenProvider(undefined);
      return;
    }

    setApiTokenProvider(() => getToken());

    return () => setApiTokenProvider(undefined);
  }, [getToken, isLoaded, isSignedIn]);

  return children;
}
