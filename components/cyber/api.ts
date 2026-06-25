// ─── API base URL — points to your Cyber-SH backend. Override with
//     NEXT_PUBLIC_CYBERSH_API_URL to target a different host/port. ───
export const BASE_URL =
  process.env.NEXT_PUBLIC_CYBERSH_API_URL?.replace(/\/$/, "") || "http://localhost:8000"

type FetchOpts = RequestInit & { headers?: Record<string, string> }

export async function apiFetch(path: string, opts: FetchOpts = {}): Promise<Response> {
  const res = await fetch(BASE_URL + path, {
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
    ...opts,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res
}

export type ChatMessage = { role: string; content: string }

// ─── Streaming chat helper (SSE) ───
export async function streamChat(
  messages: ChatMessage[],
  mode: string,
  persona: string,
  onToken: (token: string) => void,
  onDone: () => void,
  onError: (msg: string) => void,
): Promise<void> {
  try {
    const res = await apiFetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ messages, mode, persona, stream: true, use_memory: true }),
    })
    const reader = res.body?.getReader()
    if (!reader) {
      onError("No response stream from backend.")
      return
    }
    const decoder = new TextDecoder()
    let buf = ""
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buf += decoder.decode(value, { stream: true })
      const lines = buf.split("\n")
      buf = lines.pop() || ""
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue
        const data = line.slice(6).trim()
        if (data === "[DONE]") {
          onDone()
          return
        }
        try {
          const j = JSON.parse(data)
          if (j.token) onToken(j.token)
          if (j.error) {
            onError(j.error)
            return
          }
        } catch {
          /* ignore malformed chunk */
        }
      }
    }
    onDone()
  } catch (e) {
    onError(e instanceof Error ? e.message : String(e))
  }
}
