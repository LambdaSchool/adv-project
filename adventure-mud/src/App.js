import React, { Component } from 'react';
import './App.css';
import Login from './components/Login/Login';
import Authenticate from "./components/Authenticate/Authenticate";

class App extends Component {
  constructor() {
    super();
    this.state = {
      username: ""
    };
  }

  componentDidMount() {
    const user = localStorage.getItem("user");
    this.setState({ username: user });
  }
  render() {
    return (
      <div className="App">
        <Login />
      </div>
    );
  }
}

export default Authenticate(App);
