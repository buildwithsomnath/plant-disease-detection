export default function HistoryCard({ item }) {
  const confidence = (Number(item.confidence) * 100).toFixed(2);

  return (
    <div className="card border-0 shadow-sm rounded-4 h-100 overflow-hidden">
      {item.image && (
        <img
          src={item.image}
          alt={item.predicted_disease}
          className="card-img-top"
          style={{
            height: "220px",
            objectFit: "cover",
          }}
        />
      )}

      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <h5 className="fw-bold text-success mb-0">
            🌿{" "}
            {item.predicted_disease
              .replaceAll("__", ": ")
              .replaceAll("_", " ")}
          </h5>
        </div>

        <p className="text-muted mb-2">
          <strong>🌱 Plant:</strong> {item.plant_type}
        </p>

        <div className="mb-3">
          <div className="d-flex justify-content-between mb-1">
            <small className="fw-semibold"><b>Confidence : </b></small>
            <small>{confidence}%</small>
          </div>

          <div className="progress" style={{ height: "8px" }}>
            <div
              className="progress-bar bg-success"
              role="progressbar"
              style={{ width: `${confidence}%` }}
              aria-valuenow={confidence}
              aria-valuemin="0"
              aria-valuemax="100"
            />
          </div>
        </div>

        <hr />

        <div className="d-flex justify-content-between align-items-center">
          <small className="text-muted">
            🕒 {new Date(item.timestamp).toLocaleString()}
          </small>
        </div>
      </div>
    </div>
  );
}