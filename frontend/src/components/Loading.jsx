export default function Loading() {
  return (
    <div
      style={{
        marginTop: 40,
        textAlign: "center",
      }}
    >
      <div
        style={{
          width: 50,
          height: 50,
          border: "6px solid #ddd",
          borderTop: "6px solid green",
          borderRadius: "50%",
          margin: "auto",
          animation: "spin 1s linear infinite",
        }}
      />

      <h3>Predicting Disease...</h3>

      <style>
        {`
        @keyframes spin{
          from{
            transform:rotate(0deg);
          }
          to{
            transform:rotate(360deg);
          }
        }
        `}
      </style>
    </div>
  );
}