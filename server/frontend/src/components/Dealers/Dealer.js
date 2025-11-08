import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const Dealer = () => {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Beispiel: Funktion zum Laden der Händlerinformationen und Bewertungen
    const fetchDealerData = async () => {
        try {
          // Händler-Details von Django holen
          const dealerResponse = await fetch(`/djangoapp/get_dealer/${id}/`);
          const dealerJson = await dealerResponse.json();
          console.log("Dealer JSON:", dealerJson);
      
          // Bewertungen für diesen Händler holen
          const reviewsResponse = await fetch(`/djangoapp/get_dealer_reviews/${id}/`);
          const reviewsJson = await reviewsResponse.json();
          console.log("Reviews JSON:", reviewsJson);
      
          setDealer(dealerJson.dealer || dealerJson); // falls dealer verschachtelt ist
          setReviews(reviewsJson.reviews || []); // falls verschachtelt
        } catch (error) {
          console.error("Fehler beim Laden:", error);
        } finally {
          setLoading(false);
        }
      };
    fetchDealerData();
  }, [id]);

if (loading) return <p>Lädt...</p>;

if (!dealer) return <p>Händler nicht gefunden.</p>;

return (
  <div style={{ padding: '1rem' }}>
    <h2>{dealer.full_name || dealer.name}</h2>
    <p>{dealer.address}</p>
    <p>{dealer.city}, {dealer.state}</p>

    <h3>Bewertungen</h3>
    {reviews.length === 0 ? (
      <p>Keine Bewertungen vorhanden.</p>
    ) : (
      <ul>
        {reviews.map((r) => (
          <li key={r.id}>
            <strong>{r.name}</strong> ({r.sentiment}) – {r.review}
          </li>
        ))}
      </ul>
    )}

    <Link to={`/postreview/${id}`}>➕ Bewertung hinzufügen</Link>
  </div>
);
};

export default Dealer;
