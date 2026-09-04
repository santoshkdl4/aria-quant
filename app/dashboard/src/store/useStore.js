import { create } from 'zustand'

export const useStore = create((set, get) => ({
  socket: null,
  isConnected: false,
  terminalMessages: [
    { id: 1, sender: 'aria', text: 'System initialized. I am ARIA. How can I assist with your research today?' }
  ],
  
  connectWebSocket: () => {
    // Prevent multiple connections
    if (get().socket) return;
    
    // In dev mode, we connect to localhost:8000. In production, this would be dynamic based on window.location
    const wsUrl = `ws://127.0.0.1:8000/api/ws/stream`;
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      set({ isConnected: true });
      get().addTerminalMessage('aria', 'WebSocket connected. Ready for commands.');
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'terminal_response' || data.type === 'log') {
          get().addTerminalMessage(data.sender || 'system', data.text);
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err);
      }
    };
    
    ws.onclose = () => {
      set({ isConnected: false, socket: null });
      setTimeout(() => get().connectWebSocket(), 3000); // Reconnect loop
    };
    
    set({ socket: ws });
  },
  
  addTerminalMessage: (sender, text) => {
    set(state => ({
      terminalMessages: [...state.terminalMessages, { id: Date.now() + Math.random(), sender, text }]
    }));
  },
  
  sendTerminalCommand: (text) => {
    const { socket, isConnected } = get();
    get().addTerminalMessage('user', text);
    
    if (isConnected && socket) {
      socket.send(JSON.stringify({ text }));
    } else {
      get().addTerminalMessage('aria', 'Error: Not connected to backend. Please wait for reconnection.');
    }
  }
}))
