import { Link } from 'solid-app-router';

export default function Home() {
  return (
    <div class="flex flex-col p-8">
      <h1 class="text-2xl">Home</h1>
      <div>
        <Link class="text-blue-600" href='/create'>Create New Event Listing</Link>
      </div>
    </div>
  );
};
