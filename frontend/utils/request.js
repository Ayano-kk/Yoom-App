const API_BASE = "http://127.0.0.1:8000/api";
const TOKEN_KEY = "yoom_access_token";
const PROFILE_KEY = "yoom_profile";

export function getToken() {
  return uni.getStorageSync(TOKEN_KEY) || "";
}

export function saveToken(token) {
  uni.setStorageSync(TOKEN_KEY, token);
}

export function saveProfile(profile) {
  uni.setStorageSync(PROFILE_KEY, profile);
}

export function getProfile() {
  return uni.getStorageSync(PROFILE_KEY) || { nickname: "微信用户", avatar_url: "" };
}

export function request(path, options = {}) {
  const method = options.method || "GET";
  const header = {
    "Content-Type": "application/json",
    ...(options.header || {})
  };
  const token = getToken();
  if (token) {
    header.Authorization = `Bearer ${token}`;
  }
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE}${path}`,
      method,
      data: options.data || {},
      header,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
          return;
        }
        reject(new Error(res.data?.detail || `请求失败(${res.statusCode})`));
      },
      fail: (err) => reject(new Error(err.errMsg || "网络异常"))
    });
  });
}
