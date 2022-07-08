import getCrudifulAxios from './axios_config'
import { AxiosResponse } from 'axios';

export interface LoginResponse {
  authorization: string
}

export async function loginPost (username: string, password: string): Promise<LoginResponse> {
  const path = 'login';
  const response = await getCrudifulAxios().post<{
    username: string,
    password: string
  }, AxiosResponse<LoginResponse>>(path, {
    username,
    password
  });

  return response.data;
}

export async function loginEmailTokenPost (token: string): Promise<LoginResponse> {
  const path = 'login/email_token';
  const response = await getCrudifulAxios().post<null, AxiosResponse<LoginResponse>>(path, null, {
    params: { token: token }
  });
  return response.data
}

