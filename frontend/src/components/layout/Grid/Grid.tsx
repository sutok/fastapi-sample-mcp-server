import React from "react";

interface GridProps {
  children: React.ReactNode;
  columns?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };
  gap?: number;
  className?: string;
}

export const Grid: React.FC<GridProps> = ({
  children,
  columns = { sm: 1, md: 2, lg: 3, xl: 4 },
  gap = 4,
  className = "",
}) => {
  const getGridCols = () => {
    return `
      grid
      grid-cols-${columns.sm || 1}
      ${columns.md ? `md:grid-cols-${columns.md}` : ""}
      ${columns.lg ? `lg:grid-cols-${columns.lg}` : ""}
      ${columns.xl ? `xl:grid-cols-${columns.xl}` : ""}
      gap-${gap}
    `;
  };

  return <div className={`${getGridCols()} ${className}`}>{children}</div>;
};
