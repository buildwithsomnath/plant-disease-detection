import { useState } from "react";

export default function ImageUploader({ onImageSelect }) {
  const [preview, setPreview] = useState(null);

  const handleChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setPreview(URL.createObjectURL(file));

    onImageSelect(file);
  };

  return (
    <div
      style={{
        marginTop: 30,
      }}
    >
      <input
        type="file"
        accept="image/*"
        onChange={handleChange}
      />

      {preview && (
        <div style={{ marginTop: 20 }}>
          <img
            src={preview}
            alt="Preview"
            width="350"
            style={{
              borderRadius: 10,
            }}
          />
        </div>
      )}
    </div>
  );
}