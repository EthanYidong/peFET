import { createSignal, createContext, createMemo, useContext, createEffect } from "solid-js";
import { useRouteData, RouteContextObj } from "solid-app-router";

const EventContext = createContext<() => any>();

export function EventContextProvider(props) {
  const route: any = useContext(RouteContextObj);
  const routeData: any = useRouteData();

  const eventId = createMemo(() => {
    let cur = route;
    let eventId = cur.params.id;
    while (!eventId && cur.child) {
      cur = cur.child;
      eventId = parseInt(cur.params.id);
    }
    return eventId;
  });

  const event = createMemo(() => {
    if (routeData.events()) {
      for (const event of routeData.events().events) {
        if (event.id === eventId()) return event;
      }
    }
    return null;
  });

  return (
    <EventContext.Provider value={event}>
      {props.children}
    </EventContext.Provider>
  );
}

export function useEvent() {
  return useContext(EventContext);
}
