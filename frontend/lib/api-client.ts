const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000').replace(/\/$/, '')
let tokenProvider: (() => Promise<string | null>) | undefined

export function setApiTokenProvider(provider: (() => Promise<string | null>) | undefined) {
  tokenProvider = provider
}

export class ApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 30_000)
  try {
    const token = await tokenProvider?.()
    const headers = new Headers(init.headers)
    headers.set('Accept', 'application/json')
    if (!(init.body instanceof FormData) && init.body != null) headers.set('Content-Type', 'application/json')
    if (token) headers.set('Authorization', `Bearer ${token}`)
    const response = await fetch(`${API_URL}${path}`, {
      ...init,
      signal: init.signal ?? controller.signal,
      headers,
      credentials: 'omit',
    })
    if (!response.ok) {
      const payload: unknown = await response.json().catch(() => null)
      const detail = payload && typeof payload === 'object' && 'detail' in payload ? payload.detail : undefined
      const message = typeof detail === 'string' ? detail : `Request failed (${response.status})`
      throw new ApiError(message, response.status)
    }
    if (response.status === 204) return undefined as T
    if (response.status === 205 || response.headers.get('content-length') === '0') return undefined as T
    return await response.json() as T
  } catch (error) {
    if (error instanceof ApiError) throw error
    if (error instanceof DOMException && error.name === 'AbortError') throw new ApiError('Request timed out or was cancelled', 408)
    throw error
  } finally {
    clearTimeout(timeout)
  }
}

export type CvSummary = { id: string; title: string; updated_at?: string; status?: string; content?: Record<string, unknown>; has_pdf?: boolean }
export type CvListResponse = CvSummary[] | { items: CvSummary[]; total?: number }
export type UserProfile = { id: string; email: string | null; full_name: string | null; created_at?: string }

export function cvItems(payload: CvListResponse): CvSummary[] {
  return Array.isArray(payload) ? payload : payload.items
}
