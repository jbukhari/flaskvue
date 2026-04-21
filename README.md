# flaskvue
Lightweight custom template for a [Flask](https://flask.palletsprojects.com/en/stable/) app serving a REST API and a [Vue 3](https://vuejs.org/guide/introduction.html) front end. In this paradigm, the Vue app consumes the API in order to communicate asychrounously with the backend.

The Flask app uses [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) to build the API and API documentation. Flask-RESTX and [Pydantic](https://pydantic.dev/docs/) are used to validate data. User authorization and state management are handled by [Flask-Login](https://flask-login.readthedocs.io/en/latest/).

The Vue app is static JavaScript that is deployed directly to the frontend without a build step. [Pinia](https://pinia.vuejs.org/introduction.html) is used for reactive state management. The Vue components call the API using `fetch` requests to interact with the backend. 

The Vue app is intended to be a [single-page application (SPA)](https://developer.mozilla.org/en-US/docs/Glossary/SPA). The app loads one "main" component, and all the other components that make up the app are expected to be children of the main component. This template provides three pre-built components: one each for header, sidebar, and content. Components can share reactive data using Pinia. A generic Pinia data store is pre-built into this template. 
