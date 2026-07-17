export default function PredictionCard({ prediction }) {
  const confidence = Number(prediction.confidence).toFixed(2);

  return (
    <div className="card border-0 shadow-lg rounded-4 mt-4 overflow-hidden">
      <div className="card-header bg-success text-white py-3">
        <div className="d-flex justify-content-between align-items-center flex-wrap gap-2">
          <div>
            <h3 className="mb-1 fw-bold">
              🌿{" "}
              {prediction.disease
                .replaceAll("__", ": ")
                .replaceAll("_", " ")}
            </h3>
            <small>AI Prediction Result</small>
          </div>

          <span className="badge bg-light text-success fs-6 px-3 py-2 rounded-pill">
            {confidence}%
          </span>
        </div>
      </div>

      <div className="card-body p-4">

        {/* Plant */}
        <div className="mb-4">
          <h5 className="fw-bold mb-2">🌱 Plant</h5>
          <p className="text-muted mb-0">{prediction.plant_type}</p>
        </div>

        {/* Confidence */}
        <div className="mb-4">
          <div className="d-flex justify-content-between mb-2">
            <strong>Prediction Confidence</strong>
            <strong>{confidence}%</strong>
          </div>

          <div className="progress" style={{ height: "10px" }}>
            <div
              className="progress-bar bg-success"
              role="progressbar"
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>

        <div className="row g-4">

          <div className="col-md-6">
            <div className="border rounded-4 p-3 h-100">
              <h5 className="fw-bold text-success">
                📝 Description
              </h5>
              <p className="text-muted mb-0">
                {prediction.description}
              </p>
            </div>
          </div>

          <div className="col-md-6">
            <div className="border rounded-4 p-3 h-100">
              <h5 className="fw-bold text-warning">
                💊 Treatment
              </h5>
              <p className="mb-0">
                {prediction.treatment}
              </p>
            </div>
          </div>

          <div className="col-md-6">
            <div className="border rounded-4 p-3 h-100">
              <h5 className="fw-bold text-primary">
                🛡 Prevention
              </h5>
              <p className="mb-0">
                {prediction.prevention}
              </p>
            </div>
          </div>

          <div className="col-md-6">
            <div className="border rounded-4 p-3 h-100">
              <h5 className="fw-bold text-success">
                🌾 Fertilizer Recommendation
              </h5>
              <p className="mb-0">
                {prediction.fertilizer}
              </p>
            </div>
          </div>

        </div>
      </div>

      <div className="card-footer bg-light text-center">
        <small className="text-muted">
          ⚡ Prediction generated using the MobileNetV2 AI model.
        </small>
      </div>
    </div>
  );
}