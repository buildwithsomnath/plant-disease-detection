import { useEffect, useState } from "react";
import api from "../api/api";

export default function DiseaseInfo() {
  const [diseases, setDiseases] = useState([]);

  useEffect(() => {
    const fetchDiseases = async () => {
      try {
        const response = await api.get("/diseases/");
        setDiseases(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchDiseases();
  }, []);

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h1 className="fw-bold">🌿 Disease Information</h1>
        <p className="text-muted">
          Learn about plant diseases, their causes, symptoms, prevention, and treatment.
        </p>
      </div>

      <div className="row g-4">
        {diseases.map((disease) => (
          <div className="col-lg-6" key={disease.id}>
            <div className="card border-0 shadow-lg rounded-4 h-100">
              <div className="card-body p-4">
                <h3 className="card-title fw-bold text-success mb-4">
                  🌱{" "}
                  {disease.disease_name
                    .replaceAll("__", ": ")
                    .replaceAll("_", " ")}
                </h3>

                <div className="mb-3">
                  <span className="badge bg-success mb-2"><b>Description</b></span>
                  <p className="text-muted mb-0">{disease.description}</p>
                </div>

                <div className="mb-3">
                  <span className="badge bg-warning text-dark mb-2"><b>Symptoms</b></span>
                  <p className="mb-0">{disease.symptoms}</p>
                </div>

                <div className="mb-3">
                  <span className="badge bg-danger mb-2"><b>Causes</b></span>
                  <p className="mb-0">{disease.causes}</p>
                </div>

                <div className="mb-3">
                  <span className="badge bg-primary mb-2"><b>Prevention</b></span>
                  <p className="mb-0">{disease.prevention}</p>
                </div>

                <div className="mb-3">
                  <span className="badge bg-info text-dark mb-2"><b>Treatment</b></span>
                  <p className="mb-0">{disease.treatment}</p>
                </div>

                <div>
                  <span className="badge bg-secondary mb-2">
                    <b>Fertilizer Recommendation</b>
                  </span>
                  <p className="mb-0">{disease.fertilizer}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}