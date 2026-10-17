const API_BASE_URL = 'http://10.67.190.187:8000';

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

export interface TeacherDashboardResponse {
  teacher_id: number;
  teacher_name: string;
  teacher_email: string;

  total_lessons: number;
  published_lessons: number;
  draft_lessons: number;
  archived_lessons: number;

  total_subjects: number;
  total_classes: number;
  total_topics: number;

  recent_lessons_count: number;
  last_updated_lesson: string | null;
  recent_lessons: LessonSummary[];
}

export interface LessonSummary {
  id: number;
  title: string;
  subject: string;
  class_name: string;
  topic: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export async function getTeacherDashboard(
  accessToken: string,
): Promise<TeacherDashboardResponse> {
  const response = await fetch(`${API_BASE_URL}/dashboard/`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      `Unable to load dashboard. Status: ${response.status}.`;

    throw new Error(
      typeof detail === 'string'
        ? detail
        : 'Unable to load teacher dashboard.',
    );
  }

  return data as TeacherDashboardResponse;
}
