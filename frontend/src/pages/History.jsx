import { useEffect, useState } from "react";
import api from "../api/api";
import HistoryCard from "../components/HistoryCard";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get("/history/");
        console.log(response.data);
        setHistory(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h1>Prediction History</h1>

      {history.map((item) => (
        <HistoryCard key={item.id} item={item} />
      ))}
    </div>
  );
}