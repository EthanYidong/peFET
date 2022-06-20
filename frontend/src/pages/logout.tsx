import { useNavigate } from "solid-app-router";

import { useToken } from "@/lib/api";

export default function Logout() {
  const [_token, _setToken, clearToken] = useToken();
  const navigate = useNavigate();

  clearToken();
  navigate("/");

  return <></>;
}
