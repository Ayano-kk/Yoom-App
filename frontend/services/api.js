import { request, saveProfile, saveToken } from "../utils/request";

export async function login() {
  let loginCode = `mock_${Date.now()}`;
  try {
    const loginResult = await uni.login({ provider: "weixin" });
    if (loginResult.code) {
      loginCode = loginResult.code;
    }
  } catch (error) {}
  const payload = {
    code: loginCode,
    nickname: "微信用户",
    avatar_url: ""
  };
  const result = await request("/auth/login", {
    method: "POST",
    data: payload
  });
  saveToken(result.access_token);
  saveProfile(payload);
  return result;
}

export function fetchRecommendations() {
  return request("/admin/home/recommendations");
}

export function fetchAgents(params) {
  const query = Object.keys(params)
    .filter((key) => params[key] !== undefined && params[key] !== null && params[key] !== "")
    .map((key) => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join("&");
  return request(`/agents/?${query}`);
}

export function addFavorite(agent_id) {
  return request("/user/favorites", {
    method: "POST",
    data: { agent_id, action: "add" }
  });
}

export function removeFavorite(agent_id) {
  return request("/user/favorites", {
    method: "POST",
    data: { agent_id, action: "remove" }
  });
}

export function fetchFavorites() {
  return request("/user/favorites");
}

export function fetchRecent() {
  return request("/user/recent");
}
