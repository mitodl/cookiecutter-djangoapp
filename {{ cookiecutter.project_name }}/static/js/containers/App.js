import React from "react"
import { Route } from "react-router"

export default class App extends React.Component {
  render() {
    return (
      <div className="app">
        <Route path="/" component={<div>Hello cookiecutter!</div>} />
      </div>
    )
  }
}
