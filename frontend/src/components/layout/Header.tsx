import React, { useState } from "react";
import Link from "next/link";

export const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto">
        <nav className="px-4 py-3 md:py-0">
          {/* デスクトップ & モバイルの共通ヘッダー部分 */}
          <div className="flex items-center justify-between h-16">
            <Link
              href="/"
              className="text-xl md:text-2xl font-bold text-primary-600 hover:text-primary-700 transition-colors"
            >
              YourAppName
            </Link>

            {/* ハンバーガーメニューボタン（モバイルのみ） */}
            <button
              className="md:hidden p-2 rounded-md hover:bg-gray-100"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="メニュー"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isMenuOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>

            {/* デスクトップナビゲーション */}
            <div className="hidden md:flex items-center space-x-6">
              <Link
                href="/about"
                className="text-gray-600 hover:text-primary-600 transition-colors"
              >
                About
              </Link>
              <Link
                href="/contact"
                className="text-gray-600 hover:text-primary-600 transition-colors"
              >
                Contact
              </Link>
              <button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors">
                Login
              </button>
            </div>
          </div>

          {/* モバイルナビゲーション */}
          <div
            className={`${
              isMenuOpen ? "block" : "hidden"
            } md:hidden transition-all duration-300 ease-in-out`}
          >
            <div className="px-2 pt-2 pb-3 space-y-1">
              <Link
                href="/about"
                className="block px-3 py-2 rounded-md text-gray-600 hover:text-primary-600 hover:bg-gray-50 transition-colors"
              >
                About
              </Link>
              <Link
                href="/contact"
                className="block px-3 py-2 rounded-md text-gray-600 hover:text-primary-600 hover:bg-gray-50 transition-colors"
              >
                Contact
              </Link>
              <button className="w-full mt-2 px-3 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors">
                Login
              </button>
            </div>
          </div>
        </nav>
      </div>
    </header>
  );
};
