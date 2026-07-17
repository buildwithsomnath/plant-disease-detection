import { useState } from "react";
import api from "../api/api";
import PredictionCard from "../components/PredictionCard";

export default function Home() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const handlePredict = async () => {
    if (!image) return alert("Please select an image.");

    const formData = new FormData();
    formData.append("image", image);

    try {
      setLoading(true);

      const response = await api.post("/predict/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data.prediction);
    } catch (error) {
      console.log(error);
      alert("Prediction Failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-3 py-md-5 px-3 px-md-4">
      {/* Hero Section */}
      <div className="text-center mb-4 mb-md-5">
        <h1 className="display-5 fw-bold text-success">
          🌿 Plant Disease Detection
        </h1>

        <p className="lead text-muted mx-auto">
          Upload a plant leaf image and let our AI model identify diseases with
          high accuracy while providing treatment and prevention
          recommendations.
        </p>
      </div>

      {/* Upload Card */}
      <div className="card border-0 shadow-lg rounded-4">
        <div className="card-body p-3 p-md-5">
          <h3 className="fw-bold mb-4">📤 Upload Leaf Image</h3>

          <input
            type="file"
            accept="image/*"
            className="form-control"
            onChange={handleImageChange}
          />

          {preview && (
            <div className="text-center mt-4">
              <img
                src={preview}
                alt="preview"
                className="img-fluid rounded-4 shadow"
                style={{
                  maxWidth: "350px",
                  maxHeight: "350px",
                  objectFit: "cover",
                }}
              />
            </div>
          )}

          <div className="text-center mt-4">
            <button
              className="btn btn-success btn-lg px-5 w-100 w-md-auto"
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? "Predicting..." : "Predict Disease"}
            </button>
          </div>
        </div>
      </div>

      {/* Prediction */}
      {result && (
        <div className="mt-4 mt-md-5">
          <PredictionCard prediction={result} />
        </div>
      )}

      {/* AI Model Information */}
      <div className="card border-0 shadow-lg rounded-4 my-4 my-md-5">
        <div className="card-body p-3 p-md-5">
          <h2 className="fw-bold text-success mb-4">🤖 AI Model Information</h2>

          <p className="text-muted">
            Our system uses deep learning models trained on the PlantVillage
            dataset to detect diseases from plant leaf images. MobileNetV2 was
            selected for deployment due to its excellent accuracy and fast
            inference time.
          </p>

          <div className="row g-4 mt-2">
            <div className="col-lg-6">
              <div className="card h-100 border-success">
                <div className="card-body">
                  <h4 className="fw-bold mb-3">📷 Input Details</h4>

                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">
                      <strong>Dataset:</strong> PlantVillage
                    </li>

                    <li className="list-group-item">
                      <strong>Classes:</strong> 38 Diseases
                    </li>

                    <li className="list-group-item">
                      <strong>Image Size:</strong> 224 × 224
                    </li>

                    <li className="list-group-item">
                      <strong>Image Format:</strong> JPG, JPEG, PNG
                    </li>

                    <li className="list-group-item">
                      <strong>Framework:</strong> TensorFlow / Keras
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
