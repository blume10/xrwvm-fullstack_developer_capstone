import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function Dealer() {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    // Händlerdetails abrufen
    fetch(`/djangoapp/get_dealer_details/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setDealer(data.dealer);
      })
      .catch((err) => console.error("Fehler beim Laden des Händlers:", err));

    // Bewertungen abrufen
    fetch(`/djangoapp/get_dealer_reviews/${id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.reviews) setReviews(data.reviews);
      })
      .catch((err) => console.error("Fehler beim Laden der Bewertungen:", err));
  }, [id]);

  return (
    <div className="p-6">
      {dealer ? (
        <>
          <h2 className="text-2xl font-bold mb-4">
            Händler: {dealer.full_name}
          </h2>
          <p className="mb-6">Bundesstaat: {dealer.state}</p>

          <h3 className="text-xl font-semibold mb-2">Bewertungen:</h3>
          {reviews.length > 0 ? (
            <ul className="space-y-3">
              {reviews.map((r, index) => (
                <li key={index} className="border p-3 rounded-xl">
                  <p><strong>{r.name}</strong>: {r.review}</p>
                  <p>🗓️ {r.purchase_date}</p>
                  <p>🚗 {r.car_make} {r.car_model} ({r.car_year})</p>
                  <p>💬 Sentiment: <strong>{r.sentiment}</strong></p>
                </li>
              ))}
            </ul>
          ) : (
            <p>Keine Bewertungen vorhanden.</p>
          )}
        </>
      ) : (
        <p>Lade Händlerinformationen...</p>
      )}
    </div>
  );
}

export default Dealer;
