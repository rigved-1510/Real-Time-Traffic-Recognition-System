/* auth.js — User authentication helpers & workflows */

import { Api } from './api.js';
import { Auth, showToast } from './utils.js';

export async function loginUser(identifier, password) {
  const isEmail = identifier.includes('@');
  const body = isEmail ? { email: identifier, password } : { username: identifier, password };
  const res = await Api.login(body);

  if (res.requires_otp) {
    sessionStorage.setItem('tvision_pending_uid', res.user_id);
    window.location.href = 'verify-otp.html';
    return res;
  }

  Auth.setToken(res.token);
  Auth.setUser(res.user);
  return res;
}

export async function registerUser(username, email, password) {
  const res = await Api.register({ username, email, password });
  return res;
}

export async function verifyTwoFactorOtp(userId, token) {
  const res = await Api.verifyOtp({ user_id: userId, token });
  Auth.setToken(res.token);
  Auth.setUser(res.user);
  return res;
}

export async function logoutUser() {
  try {
    await Api.logout();
  } catch (_) {
    // Ignore network failure on logout
  } finally {
    Auth.clear();
    window.location.href = '/index.html';
  }
}
