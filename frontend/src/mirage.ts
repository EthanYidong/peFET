import { createServer, Model } from "miragejs";

createServer({
  models: {
    events: Model,
  },
  routes() {
    this.urlPrefix = 'http://localhost:8000';

    this.post("/api/account/login", () => {
      return {
        token: "token"
      }
    });

    this.post("/api/account/signup", () => {
      return {
        token: "token"
      }
    });

    this.post("/api/account/validate", () => {
      return {
        email: "test@example.com"
      }
    });

    this.get("/api/event/all", (schema, request) => {
      return schema.all("events");
    });

    this.post("/api/event/create", (schema, request) => {
      const body = JSON.parse(request.requestBody);
      
      schema.create("events", body);

      return {
        name: body.name
      }
    });
  },
});
