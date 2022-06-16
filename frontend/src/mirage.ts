import { belongsTo, createServer, hasMany, Model } from "miragejs";
import type { BelongsTo, HasMany } from "miragejs/-types";

interface Event {
  name: string;
  date: string;
  participants: HasMany<string>;
}

interface Participant {
  name: string;
  email: string;
  event: BelongsTo<string>;
  status: "not submitted" | "submitted";
}

const mirageModels = {
  event: Model.extend<Partial<Event>>({ participants: hasMany() }),
  participant: Model.extend<Partial<Participant>>({ event: belongsTo() }),
};

const mirageFactories = {};

createServer<typeof mirageModels, typeof mirageFactories>({
  models: mirageModels,
  routes() {
    this.urlPrefix = "http://localhost:8000";

    this.post("/api/account/login", () => {
      return {
        token: "token",
      };
    });

    this.post("/api/account/signup", () => {
      return {
        token: "token",
      };
    });

    this.post("/api/account/validate", () => {
      return {
        email: "test@example.com",
      };
    });

    this.get("/api/event/all", (schema, request) => {
      return schema.all("event");
    });

    this.post("/api/event/create", (schema, request) => {
      const body = JSON.parse(request.requestBody);

      const newEvent = schema.create("event", body);

      return {
        id: newEvent.id,
      };
    });

    this.post("/api/event/:id/update", (schema, request) => {
      const body = JSON.parse(request.requestBody);

      const oldEvent = schema.find("event", request.params.id);

      oldEvent.update(body);
      return {};
    });

    this.get("/api/event/:id/participants", (schema, request) => {
      const event = schema.find("event", request.params.id);
      return event.participants;
    });

    this.post("/api/event/:id/participants/create", (schema, request) => {
      const body = JSON.parse(request.requestBody);
      const event = schema.find("event", request.params.id);

      schema.create("participant", {event: event, status: "not submitted", ...body});
      return {};
    });

  },
  seeds(server) {
    const placeholderEvent = server.create("event", {
      name: "Placeholder Event",
      date: "2023-01-01",
    });
    server.create("participant", {
      event: placeholderEvent,
      name: "Placeholder Participant 1",
      email: "test1@example.com",
      status: "not submitted",
    });
    server.create("participant", {
      event: placeholderEvent,
      name: "Placeholder Participant 2",
      email: "test2@example.com",
      status: "submitted",
    });
  },
});
