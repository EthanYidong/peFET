import { Show } from 'solid-js';
import { Link } from 'solid-app-router';
import { useToken } from '@/lib/api';

export default function Home() {
  const [token, _setToken, _clearToken] = useToken();

  return (
    <div class="flex flex-col p-8">
      <h1 class="text-2xl">Home</h1>
      <div class="flex gap-2">
        <Show when={token()} fallback={
          () => <>
            <Link class="bg-blue-600 text-white p-2 rounded-md" href='/login'>Login</Link>
            <Link class="bg-blue-600 text-white p-2 rounded-md" href='/signup'>Sign Up</Link>
          </>}>
          <Link class="bg-blue-600 text-white p-2 rounded-md" href='/logout'>Logout</Link>
        </Show>
        <Link class="bg-blue-600 text-white p-2 rounded-md" href='/create'>Create New Event Listing (Requires Login)</Link>
      </div>
    </div>
  );
};
