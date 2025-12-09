'use client';

import { useState } from 'react';
import { apiClient, ChatMessage } from '@/lib/api';
import { Language } from '@/lib/i18n';

export type SearchMode = 'fast' | 'normal' | 'deep';

interface UseChatReturn {
    messages: ChatMessage[];
    isLoading: boolean;
    error: string | null;
    sendMessage: (message: string, mode?: SearchMode) => Promise<void>;
    clearMessages: () => void;
}

export function useChat(language: Language): UseChatReturn {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const sendMessage = async (message: string, mode: SearchMode = 'normal') => {
        if (!message.trim()) return;

        // Add user message
        const userMessage: ChatMessage = {
            role: 'user',
            content: message,
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        try {
            const response = await apiClient.chat({
                message,
                language,
                conversation_history: messages,
                search_mode: mode,  // Pass search mode to API
            });

            // Add assistant response
            const assistantMessage: ChatMessage = {
                role: 'assistant',
                content: response.response,
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error');
            console.error('Chat error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const clearMessages = () => {
        setMessages([]);
        setError(null);
    };

    return {
        messages,
        isLoading,
        error,
        sendMessage,
        clearMessages,
    };
}
