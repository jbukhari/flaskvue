# flaskvue

[GitHub template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository#about-template-repositories) implementing a full web stack designed for rapid prototyping.

Stack:
* [Flask](https://flask.palletsprojects.com/en/stable/)
* [Vue 3](https://vuejs.org/guide/introduction.html)
* [MongoDB](https://www.mongodb.com/docs/) or other [Pymongo](https://pypi.org/project/pymongo/)-compatible database

Built in features:
* API with schema validation ([Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) and [Pydantic](https://pydantic.dev/docs/))
* custom database object-document mapper
* user authentication system ([Flask-Login](https://flask-login.readthedocs.io/en/latest/) and MongoDB)
* back end tests ([Pytest](https://docs.pytest.org/en/stable/))
* front end state management ([Pinia](https://pinia.vuejs.org/introduction.html))
* switchable JavasScript module code source (remote vs local)

### Architecture
The Flask app serves the Vue app via a standard [Jinja2](https://pypi.org/project/Jinja2/) HTML template, where the Vue app is embedded in the `<script>` element. The Vue app is deployed directly to the front end [without a build step](https://vuejs.org/guide/extras/ways-of-using-vue.html#standalone-script).

The Vue app is set up as a [single-page application (SPA)](https://developer.mozilla.org/en-US/docs/Glossary/SPA). A "main" component and three subcomponents for page header, sidebar, and content are provided. Components can share reactive state data using a pre-built [Pinia](https://pinia.vuejs.org/introduction.html) data store. Components can make asynchronous calls to the API using `fetch`.

The Vue app employs the Vue [Options API](https://vuejs.org/guide/introduction.html#options-api) in order to provide a consistent structure that can be rapidly adapted to the use case of the app being developed. [Composition API](https://vuejs.org/guide/extras/composition-api-faq) can be mixed in seamlessly if desired by the developer.

### Database
The app can run without connecting to a database, but in order to enable the user authentication system, the developer must supply an environment variable containing read/write credentials for a database that [Pymongo](https://pypi.org/project/pymongo/) can interface with such as [MongoDB](https://www.mongodb.com/docs/), [FerretDB](https://docs.ferretdb.io/),  [AWS DocumentDB](https://aws.amazon.com/documentdb/), or [Azure Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db#tabs-pill-bar-oc15bd_tab3)

---

<img width="1351" height="766" alt="image" src="https://github.com/user-attachments/assets/aeb500a8-505d-4077-9b88-e64838b37481" />
