import React from "react";
import { useParams } from "react-router-dom";
import DefaultLayout from "../components/layouts/DefaultLayout";

const Reservations: React.FC = () => {
  // URLパラメータからcompany_idとbranch_idを取得
  const { company_id, branch_id } = useParams<{ company_id: string; branch_id: string }>();

  return (
    <DefaultLayout>
      <div style={{ maxWidth: 900, margin: "40px auto" }}>
        <h2>予約一覧ページ</h2>
        <p>company_id: {company_id}</p>
        <p>branch_id: {branch_id}</p>
        {/* ここに予約一覧や予約機能を実装 */}
      </div>
    </DefaultLayout>
  );
};

export default Reservations;
