const API_BASE_URL = 'http://172.25.154.187:8000';

export type UserRole = 'teacher' | 'student';

export interface LoginResponse {
  message: string;
  teacher_id?: number;
  student_id?: number;
  full_name: string;
  email: string;
  access_token: string;
}

export async function loginUser(
  role: UserRole,
  email: string,
  password: string,
): Promise<LoginResponse> {
  const endpoint =
    role === 'teacher' ? '/teachers/login' : '/students/login';

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({
      email: email.trim(),
      password,
    }),
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      `Login failed with status ${response.status}.`;

    throw new Error(
      typeof detail === 'string'
        ? detail
        : 'Login failed. Please check your credentials.',
    );
  }

  if (!data?.access_token) {
    throw new Error('The server did not return an access token.');
  }

  return data as LoginResponse;
}