import { useEffect } from "react";

function App() {
  useEffect(() => {
    fetch("https://careerbuddyai-6.onrender.com")
      .then(res => res.json())
      .then(data => console.log(data));
  }, []);

  return <h1>Hello World from React</h1>;
}

export default App;