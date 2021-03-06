# Lokey recruitment task

This repo contains my solution for recruitment task at Lokey.

## Task requirements:
- Use Quasar CLI
- Use compositionApi as well as defineComponent and setup()
- Typescript

## Task functionality:
Create simple solution with one view to perform CRUD operations. The view should contain **q-table** to list all **Articles** which can be edited and deleted. Above the table should be a small **q-btn**, which will open a popup to add a new **Article** and refresh table. CUD operations should also show a small alert with information about opetion success of fail. Use existing [API](https://github.com/radoo11/recruitment_task).

Add "Release Date" to **Article** model and create/update GET endpoint to fetch only **Articles** from given year by parameter.

## Important notes:
In frontend app in *axios_config.ts* I changed **BASE_URL** to `http://localhost:5000/api/` instead of `/api/` which caused that frontend app was trying to fetch from `http://localhost:8080` which was invalid because port *8080* was reserved for frontend while port *5000* is the default port for backend app in Flask.