import React from 'react';
import './App.css';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <img src='/static/img/transpiron.png' className="App-logo" alt="logo"/>
        <br/>
        <a
          className="App-link"
          href="https://transpiron.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          django-react-app-boilerplate
        </a>
        <br/>
        <p><small>Try making some simple changes to src/App.js and save to reload</small></p>
      </header>
    </div>
  );
}

export default App;
