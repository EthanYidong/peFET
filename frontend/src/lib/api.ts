import { useStorage } from "@/lib/storage";

export const API_URL = import.meta.env.VITE_API_URL;

export function useToken(): [() => string, (newToken: string | null) => void, () => void] {
  const [storage, setStorage, clearStorage] = useStorage();
  return [() => storage.token, (value) => setStorage('token', value), clearStorage];
}
