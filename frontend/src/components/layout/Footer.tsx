import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="container mx-auto py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">About Us</h3>
            <p className="text-gray-600">
              Short description about your company or application.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a
                  href="#"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  Home
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  About
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  Services
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <ul className="space-y-2 text-gray-600">
              <li>Email: contact@example.com</li>
              <li>Phone: (123) 456-7890</li>
              <li>Address: Your Address Here</li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Follow Us</h3>
            <div className="flex space-x-4">
              {/* ソーシャルメディアアイコンをここに追加 */}
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 text-center text-gray-600">
          <p>© {new Date().getFullYear()} YourAppName. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};
