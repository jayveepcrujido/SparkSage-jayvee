"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { Loader2 } from "lucide-react";
import { api } from "@/lib/api";
import type { ChannelItem } from "@/lib/api";
import { ChannelList } from "@/components/conversations/channel-list";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";

export default function ConversationsPage() {
  const { data: session } = useSession();
  const [channels, setChannels] = useState<ChannelItem[]>([]);
  const [loading, setLoading] = useState(true);

  const token = (session as { accessToken?: string })?.accessToken;

  async function load() {
    if (!token) return;
    try {
      const result = await api.getConversations(token);
      setChannels(result.channels);
    } catch {
      toast.error("Failed to load conversations");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [token]);

  async function handleDelete(channelId: string) {
    if (!token) return;
    try {
      await api.deleteConversation(token, channelId);
      toast.success(`Cleared conversation for #${channelId}`);
      await load();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to delete");
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const codeReviewChannels = channels.filter(c => c.has_code_review);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Conversations</h1>
      
      <Tabs defaultValue="all" className="w-full">
        <TabsList className="mb-4">
          <TabsTrigger value="all">All Channels</TabsTrigger>
          <TabsTrigger value="reviews">Code Reviews</TabsTrigger>
        </TabsList>
        
        <TabsContent value="all">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">All Channels</CardTitle>
            </CardHeader>
            <CardContent>
              <ChannelList channels={channels} onDelete={handleDelete} />
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="reviews">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Code Review Sessions</CardTitle>
            </CardHeader>
            <CardContent>
              <ChannelList channels={codeReviewChannels} onDelete={handleDelete} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
