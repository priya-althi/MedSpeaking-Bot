const LanguageSelector = ({ lang, setLang }) => (
  <select value={lang} onChange={(e) => setLang(e.target.value)}>
  <option value="en">English</option>
  <option value="hi">Hindi</option>
  <option value="te">Telugu</option>
  <option value="ta">Tamil</option>
  <option value="kn">Kannada</option>
  <option value="ml">Malayalam</option>
  <option value="mr">Marathi</option>
  <option value="bn">Bengali</option>
  <option value="gu">Gujarati</option>
  <option value="pa">Punjabi</option>
  <option value="ur">Urdu</option>
  <option value="or">Odia</option>
  <option value="as">Assamese</option>
</select>

);

export default LanguageSelector;
