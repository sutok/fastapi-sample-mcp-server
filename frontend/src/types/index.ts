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
  phone_number: string;
  email: string;
  website: string;
  description?: string;
  created_at: string;
  updated_at: string;
}
