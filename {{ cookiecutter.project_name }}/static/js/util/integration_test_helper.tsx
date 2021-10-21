import React, { ComponentType, FunctionComponent } from "react"
import { mount, ReactWrapper } from "enzyme"
import sinon, { SinonSandbox, SinonStub } from "sinon"
import { createMemoryHistory, MemoryHistory, Update, State } from "history"
import { Provider } from "react-redux"
import { Provider as ReduxQueryProvider } from "redux-query-react"
import { Router } from "react-router"
import { Action } from "redux"

import { ReduxState } from "../reducers"
import configureStore, { Store } from "../store/configureStore"
import { getQueries } from "../lib/redux_query"

import * as networkInterfaceFuncs from "../store/network_interface"

export default class IntegrationTestHelper {
  browserHistory: MemoryHistory
  sandbox: SinonSandbox
  actions: Array<Action>
  handleRequestStub: SinonStub
  currentLocation: Update<State> | null
  scrollIntoViewStub: SinonStub
  wrapper?: ReactWrapper | null
  // just roll with it :)
  realWarn: any

  constructor() {
    this.sandbox = sinon.createSandbox({})
    this.actions = []

    this.scrollIntoViewStub = this.sandbox.stub()
    window.HTMLDivElement.prototype.scrollIntoView = this.scrollIntoViewStub
    window.HTMLFieldSetElement.prototype.scrollIntoView = this.scrollIntoViewStub
    this.browserHistory = createMemoryHistory()
    this.currentLocation = null
    this.wrapper = null
    this.browserHistory.listen(url => {
      this.currentLocation = url
    })

    // we return "no match" here as a sentinel default response
    // basically, if this is returned it's an indication that mocks
    // weren't set up correctly for the URL and HTTP verb which
    // handleRequestStub is being called with.
    this.handleRequestStub = this.sandbox.stub().returns("no match")
    this.sandbox
      .stub(networkInterfaceFuncs, "makeRequest")
      .callsFake((url, method, options) => ({
        execute: callback => {
          let response = this.handleRequestStub(url, method, options)
          // if response is "no match" then no call to `.withArgs` has
          // been sufficient to match the current URL and method combo.
          // in that case, we'll log to `console.error` the method and
          // url and thereby fail the test.
          if (response === "no match") {
            console.error(`unmatched ${method} request made to ${url}`)
            response = {
              body:   {},
              status: 200
            }
          }
          const err = null
          const resStatus = response.status ?? 0
          const resBody = response.body ?? undefined
          const resText = response.text ?? undefined
          const resHeaders = response.header ?? undefined

          callback(err, resStatus, resBody, resText, resHeaders)
        },
        abort: () => {
          throw new Error("Aborts currently unhandled")
        }
      }))
    this.realWarn = console.warn
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    console.warn = () => {}
  }

  mockRequest(
    url: string,
    method: "GET" | "POST" | "PATCH",
    responseBody: unknown,
    code: number
  ): void {
    this.handleRequestStub.withArgs(url, method).returns({
      body:   responseBody,
      status: code
    })
  }

  /**
   * Convenience method for mocking out a GET request
   *
   * pass the API url you want to mock and the object which should be
   * returned as the request body!
   */
  mockGetRequest(url: string, body: unknown): void {
    this.mockRequest(url, "GET", body, 200)
  }

  /**
   * Convenience method for mocking out a POST request
   */
  mockPostRequest(url: string, body: unknown): void {
    this.mockRequest(url, "POST", body, 201)
  }

  /**
   * Convenience method for mocking out a PATCH request
   */
  mockPatchRequest(url: string, body: unknown): void {
    this.mockRequest(url, "PATCH", body, 200)
  }

  cleanup(unmount = true): void {
    this.actions = []
    this.sandbox.restore()

    if (this.wrapper && unmount) {
      this.wrapper.unmount()
      delete this.wrapper
      this.wrapper = null
    }
    console.warn = this.realWarn
  }

  /**
   * Configure the integration test renderer!
   *
   * Takes a component, some defaultProps, and a defaultState for
   * the Redux store and returns a render function which can be used
   * to render the component and then make assertions and so on about it.
   *
   * Usage example:
   *
   * ```ts
   * const render = helper.configureRenderer(
   *   MyComponent, { prop: 'default value' }
   * )
   * const { wrapper, store } = await render()
   * ```
   */
  configureRenderer(
    Component: ComponentType<any> | FunctionComponent<any>,
    defaultProps = {},
    defaultState?: ReduxState
  ) {
    return async (
      extraProps = {},
      beforeRenderActions = [],
      perRenderDefaultState?: ReduxState
    ): Promise<{
      wrapper: ReactWrapper
      store: Store
    }> => {
      const store = configureStore(defaultState ?? perRenderDefaultState)
      beforeRenderActions.forEach(action => store.dispatch(action))

      const wrapper = mount(
        <Provider store={store}>
          <ReduxQueryProvider queriesSelector={getQueries}>
            <Router history={this.browserHistory}>
              <Component {...defaultProps} {...extraProps} />
            </Router>
          </ReduxQueryProvider>
        </Provider>
      )
      this.wrapper = wrapper
      wrapper.update()
      return { wrapper, store }
    }
  }
}

export type TestRenderer = ReturnType<
  IntegrationTestHelper["configureRenderer"]
>
