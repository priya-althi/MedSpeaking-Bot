const AgeInput = ({ age, setAge }) => (
  <input
    type="number"
    placeholder="Your age"
    value={age}
    min="1"
    max="120"
    onChange={(e) => setAge(e.target.value)}
  />
);

export default AgeInput;