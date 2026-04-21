export default function Button({ children, onClick, disabled, type = "button" }) {
  return (
    <button className="btn" type={type} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
