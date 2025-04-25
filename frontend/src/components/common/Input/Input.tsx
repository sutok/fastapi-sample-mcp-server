import React from "react";

interface InputProps {
  label?: string;
  type?: string;
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  type = "text",
  placeholder,
  value,
  onChange,
  error,
  required = false,
}) => {
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-gray-700 text-sm font-bold mb-2">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`
          w-full px-3 py-2 border rounded-lg
          focus:outline-none focus:ring-2
          ${error ? "border-red-500" : "border-gray-300"}
          ${error ? "focus:ring-red-200" : "focus:ring-blue-200"}
        `}
      />
      {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
    </div>
  );
};
