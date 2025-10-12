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
        // API-Aufrufe an Backend (z.B. /api/dealer/:id und /api/reviews?dealerId=id)
        const dealerResponse = await fetch(`/api/dealer/${id}`);
        const dealerData = await dealerResponse.json();

        const reviewsResponse = await fetch(`/api/reviews?dealerId=${id}`);
        const reviewsData = await reviewsResponse.json();

        setDealer(dealerData);
        setReviews(reviewsData);
      } catch (error) {
        console.error('Fehler beim Laden der Daten:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDealerData();
  }, [id]);

  if (loading) return <p>Lädt...</p>;
  if (!dealer) return <p>Händler nicht gefunden.</p>;

  return (
    <div>
      <h2>{dealer.name}</h2>
      <p>{dealer.address}</p>
      <p>{dealer.city}, {dealer.state}</p>

      <h3>Bewertungen</h3>
      {reviews.length === 0 ? (
        <p>Keine Bewertungen vorhanden.</p>
      ) : (
        <ul>
          {reviews.map((review) => (
            <li key={review.id}>
              <strong>{review.user}</strong>: {review.comment}
            </li>
          ))}
        </ul>
      )}

      <Link to={`/postreview/${id}`}>Bewertung hinzufügen</Link>
    </div>
  );
};

export default Dealer;
