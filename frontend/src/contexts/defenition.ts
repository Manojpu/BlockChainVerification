// Define types for our context data
export interface User {
  id: string;
  username: string;
  email: string;
  // Add any other user properties
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterUserData) => Promise<void>;
  logout: () => void;
}

// Define types for function parameters
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterUserData {
  username: string;
  email: string;
  password: string;
}
