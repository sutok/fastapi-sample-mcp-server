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
  company_id: string;
  branch_id: string;
  reservation_at: string;
  reception_number: string;
  created_at: string;
  updated_at: string;
}
