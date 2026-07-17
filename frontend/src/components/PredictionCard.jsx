export default function PredictionCard({ prediction }) {
  if (!prediction) return null;

  return (
    <div
      style={{
        marginTop: 30,
        padding: 20,
        border: "1px solid #ddd",
        borderRadius: 10,
        background: "#f9fff8",
      }}
    >
      <h2>{prediction.disease}</h2>

      <p>
        <strong>Plant:</strong> {prediction.plant_type}
      </p>

      <p>
        <strong>Confidence:</strong> {prediction.confidence}%
      </p>

      <p>
        <strong>Description:</strong>
        <br />
        {prediction.description}
      </p>

      <p>
        <strong>Treatment:</strong>
        <br />
        {prediction.treatment}
      </p>

      <p>
        <strong>Fertilizer:</strong>
        <br />
        {prediction.fertilizer}
      </p>

      <p>
        <strong>Prevention:</strong>
        <br />
        {prediction.prevention}
      </p>
    </div>
  );
}