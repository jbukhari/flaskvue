# flaskvue

[GitHub template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository#about-template-repositories) implementing a web stack consisting of a [Flask](https://flask.palletsprojects.com/en/stable/) app that serves a [REST API](https://developer.mozilla.org/en-US/docs/Glossary/REST) and a [Vue 3](https://vuejs.org/guide/introduction.html) app as the front end. The Vue app consumes the API in order to communicate asynchronously with the back end.

The app in this template runs as-is by installing the requirements into a Python virtual environment and starting the Flask app in the standard way. ~~A [Dockerfile](https://docs.docker.com/reference/dockerfile/) is provided for building deployment containers~~ (not implemented yet).

### Flask
The Flask app uses [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) to build the API and API documentation. Flask-RESTX and [Pydantic](https://pydantic.dev/docs/) are used to validate input and return data.

The Flask app serves the Vue app via a standard [Jinja2](https://pypi.org/project/Jinja2/) HTML template, where the Vue app is embedded in the `<script>` element. The HTML is rendered with the API URL as a variable, which the Vue app can use to make asynchronous API requests. ~~[Flask-Login](https://flask-login.readthedocs.io/en/latest/) handles authorizing requests to the API from the back end~~ (not implemented yet).

~~[Pytest](https://docs.pytest.org/en/stable/) tests for testing the API routes are provided. A [GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions workflow) file is set up to automatically run the tests on all pull requests and changes to the main branch~~ (not implemented yet). 

### Vue
As discussed, the Vue app is deployed directly to the front end [without a build step](https://vuejs.org/guide/extras/ways-of-using-vue.html#standalone-script).

The Vue app is set up as a [single-page application (SPA)](https://developer.mozilla.org/en-US/docs/Glossary/SPA). A "main" component and three subcomponents for page header, sidebar, and content are provided. Components can share reactive state data using a pre-built [Pinia](https://pinia.vuejs.org/introduction.html) data store. Components can make asynchronous calls to the API using `fetch`.

The Vue app employs the Vue [Options API](https://vuejs.org/guide/introduction.html#options-api) in order to impose a structure that can be rapidly adapted to the use case of the app being developed. [Composition API](https://vuejs.org/guide/extras/composition-api-faq) can be mixed in seamlessly if desired by the developer.

### Database optional
The app runs without connecting to a database, ~~but in order to enable the user authorization system, the developer must supply an environment variable containing read/write credentials for a database that [Pymongo](https://pypi.org/project/pymongo/) can interface with such as [MongoDB](https://www.mongodb.com/docs/), [FerretDB](https://docs.ferretdb.io/),  [AWS DocumentDB](https://aws.amazon.com/documentdb/), or [Azure Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db#tabs-pill-bar-oc15bd_tab3)~~ (not implemented yet).

---

<img width="1351" height="766" alt="image" src="https://github.com/user-attachments/assets/aeb500a8-505d-4077-9b88-e64838b37481" />
