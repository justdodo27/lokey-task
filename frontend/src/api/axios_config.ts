import axios from 'axios';
import { useUserStore } from '../stores/userStore';

export const BASE_URL = 'http://localhost:5000/api/'
// export const BASE_URL = String(process.env.API_URL);  // works only when app served by backend server, for local set to full url

export default function getCrudifulAxios () {
  const headers: Record<string, string> = {}
  const store = useUserStore();
  const token = store.authorization;
  headers['Content-Type'] = 'application/json';
  headers['Access-Control-Allow-Origin'] = '*';
  if (!!token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return axios.create({
    baseURL: BASE_URL,
    timeout: 60 * 1000,  // 60 seconds
    headers: headers
  })
}
