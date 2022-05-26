import { lazy } from 'solid-js';
import type { RouteDefinition } from 'solid-app-router';

export const routes: RouteDefinition[] = [
  {
    path: '/',
    component: lazy(() => import('@/pages/home')),
  },
  {
    path: '/create',
    component: lazy(() => import('@/pages/create')),
  }
];
