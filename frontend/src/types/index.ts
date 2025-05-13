export interface Company {
  id: string;
  company_name: string;
  address: string;
  phone_number: string;
  email: string;
  website: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Branch {
  id: string;
  branch_name: string;
  address: string;
  phone: string;
  email: string;
  notes: string;
  website: string;
  business_hours: string;
  created_at: string;
  updated_at: string;
}

export interface Reservation {
  id: string;
  user_id: string;
  company_id: string;
  branch_id: string;
  reservation_at: string;
  notes?: string;
  status: string;
  reception_number: number;
  created_at: string;
  updated_at: string;
}

export interface UserInfo {
  id: string;
  company_id: string;
  branch_id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
