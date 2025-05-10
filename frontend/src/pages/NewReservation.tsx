import React, { useState } from "react";
import { useParams } from "react-router-dom";
import DefaultLayout from "../components/layouts/DefaultLayout";
import { useReservation } from "../hooks/useReservation";

const MAX_WAIT_COUNT = 10; // 仮の最大待ち人数

const NewReservation: React.FC = () => {
  const { branch_id } = useParams<{ branch_id: string }>();
  const { reservation, loading, error, createReservation, refreshReservation } =
    useReservation(branch_id ?? null);
  const [waitCount, setWaitCount] = useState(3); // 仮の現在待ち人数
  const [isOpen, setIsOpen] = useState(true); // 仮の営業時間内フラグ

  const handleReserve = async () => {
    await createReservation();
    refreshReservation();
  };

  // 仮の店舗名
  const branchName = "サンプル店舗";

  return (
    <DefaultLayout>
      <div style={{ maxWidth: 900, margin: "40px auto" }}>
        <h2>予約作成ページ（順番のみ）</h2>
        <p>店舗名: {branchName}</p>
        <p>現在の待ち人数: {waitCount}人</p>
        <p>最大待ち人数: {MAX_WAIT_COUNT}人</p>
        {loading && <p>読み込み中...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {reservation ? (
          <div>
            <p>あなたの予約番号: {reservation.number}</p>
            <p>予約状態: {reservation.status}</p>
          </div>
        ) : (
          <button
            onClick={handleReserve}
            disabled={waitCount >= MAX_WAIT_COUNT || !isOpen}
          >
            予約する
          </button>
        )}
        {/* 営業時間外や満席時のバリデーションメッセージ例 */}
        {!isOpen && <p style={{ color: "orange" }}>営業時間外です</p>}
        {waitCount >= MAX_WAIT_COUNT && (
          <p style={{ color: "orange" }}>満席です</p>
        )}
      </div>
    </DefaultLayout>
  );
};

export default NewReservation;
