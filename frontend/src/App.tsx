import { useRoutes } from 'solid-app-router';
import { routes } from '@/routes';

export default function App() {
  const Route = useRoutes(routes);
  return (
    <>
      <Route/>
    </>
  );
};
