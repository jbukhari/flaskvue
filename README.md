# flaskvue
Lightweight web stack employing a [Flask](https://flask.palletsprojects.com/en/stable/) app to serve a [REST API](https://developer.mozilla.org/en-US/docs/Glossary/REST) with a [Vue 3](https://vuejs.org/guide/introduction.html) app as the frontend. The Vue app consumes the API in order to communicate asynchronously with the backend.

### Flask
The Flask app uses [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) to build the API and API documentation. Flask-RESTX and [Pydantic](https://pydantic.dev/docs/) are used to validate input and return data.

The Flask app serves the Vue app via a standard [Jinja2](https://pypi.org/project/Jinja2/) HTML template, where the Vue app is embedded as standard JavaScript. The HTML is rendered with the API URL as a variable, which the Vue app can use to make API requests. [Flask-Login](https://flask-login.readthedocs.io/en/latest/) handles authorizing requests to the API from the backend.

### Vue
The Vue app is JavaScript deployed without a build step directly to the frontend via the previously mentioned HTML. [Pinia](https://pinia.vuejs.org/introduction.html) is used for reactive state management. The Vue components call the API using `fetch` requests to interact with the backend. Flask-Login handles authorizing the API requests.

The Vue app is intended to be a [single-page application (SPA)](https://developer.mozilla.org/en-US/docs/Glossary/SPA). The app loads one "main" component, and all the other components that make up the app are expected to be children of the main component. This template provides three pre-built components for page header, sidebar, and content. Components can share reactive data using Pinia. A generic Pinia data store is pre-built into this template.

The Vue app employs the Vue [Options API](https://vuejs.org/guide/introduction.html#options-api) in order to impose a structure that can be rapidly adapted to the use case of the app being developed.

### database
In order to enable the authorization user system, the developer must supply an environment variable containing read/write credentials for a database that [Pymongo](https://pypi.org/project/pymongo/) can interface with such as [MongoDB](https://www.mongodb.com/docs/), [FerretDB](https://docs.ferretdb.io/),  [AWS DocumentDB](https://aws.amazon.com/documentdb/), or [Azure Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db#tabs-pill-bar-oc15bd_tab3).

---

<img width="1351" height="766" alt="image" src="https://github.com/user-attachments/assets/aeb500a8-505d-4077-9b88-e64838b37481" />
