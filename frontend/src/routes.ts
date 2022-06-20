import { lazy } from "solid-js";
import type { RouteDefinition } from "solid-app-router";
import { EventData, EventsData } from "@/lib/route-data";

export const routes: RouteDefinition[] = [
  {
    path: "/",
    component: lazy(() => import("@/pages/home")),
  },
  {
    path: "/signup",
    component: lazy(() => import("@/pages/signup")),
  },
  {
    path: "/login",
    component: lazy(() => import("@/pages/login")),
  },
  {
    path: "/logout",
    component: lazy(() => import("@/pages/logout")),
  },
  {
    path: "/portal",
    children: [
      {
        path: "/",
        component: lazy(() => import("@/pages/portal/home")),
      }
    ]
  },
  {
    path: "/dashboard",
    component: lazy(() => import("@/pages/dashboard/layout-dashboard")),
    data: EventsData,
    children: [
      {
        path: "/",
        component: lazy(() => import("@/pages/dashboard/home")),
      },
      {
        path: "/event/:id",
        component: lazy(() => import("@/pages/dashboard/event/layout-event")),
        data: EventData,
        children: [
          {
            path: "/",
            component: lazy(() => import("@/pages/dashboard/event/home")),
          },
          {
            path: "/settings",
            component: lazy(() => import("@/pages/dashboard/event/settings")),
          },
        ],
      },
    ],
  },
];
