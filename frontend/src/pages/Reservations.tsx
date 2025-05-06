import React from "react";
import { useParams } from "react-router-dom";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { useReservationsList } from "../hooks/useReservationsList";

const Reservations: React.FC = () => {
  // URLパラメータからcompany_idとbranch_idを取得
  const { company_id, branch_id } = useParams<{
    company_id: string;
    branch_id: string;
  }>();
  // 一覧を取得
  const {
    data: reservations,
    isLoading,
    error,
  } = useReservationsList(company_id, branch_id);
  console.log("reservations", reservations);

  return (
    <DefaultLayout>
      <div style={{ maxWidth: 900, margin: "40px auto" }}>
        <h2>予約一覧ページ</h2>
        <p>company_id: {company_id}</p>
        <p>branch_id: {branch_id}</p>
        {/* ここに予約一覧や予約機能を実装 */}
        <ul>
          {reservations && reservations.length > 0 ? (
            reservations.map((r: any) => (
              <li key={r.id}>
                {r.created_at} - {r.status} - {r.branch_name}
              </li>
            ))
          ) : (
            <li>予約履歴がありません</li>
          )}
        </ul>
      </div>
    </DefaultLayout>
  );
};

export default Reservations;
